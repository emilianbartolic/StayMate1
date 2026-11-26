"""Booking.com Demand API adapter for real, city-filtered accommodation offers.

Credentials are read only from the backend process environment. No property
content is fabricated when the provider is unavailable.
"""
from __future__ import annotations

import json
import os
import re
import time
import unicodedata
from datetime import date
from threading import Lock
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))


class BookingProviderError(RuntimeError):
    """A safe-to-report provider setup or request error."""


_cache_lock = Lock()
_city_cache: tuple[float, list[dict[str, Any]]] | None = None
_constants_cache: tuple[float, dict[str, Any]] | None = None
_offer_cache: dict[str, tuple[float, list[dict[str, Any]]]] = {}


def configured() -> bool:
    return bool(os.environ.get("BOOKING_DEMAND_API_KEY") and os.environ.get("BOOKING_DEMAND_AFFILIATE_ID"))


def _norm(value: Any) -> str:
    text = unicodedata.normalize("NFKD", str(value or "")).encode("ascii", "ignore").decode().casefold()
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def _translated(value: Any, default: str = "") -> str:
    if isinstance(value, str):
        return value
    if not isinstance(value, dict):
        return default
    for language in ("de", "en-gb", "en-us", "en"):
        if value.get(language):
            return str(value[language])
    return next((str(item) for item in value.values() if isinstance(item, str) and item), default)


class BookingDemandClient:
    def __init__(self) -> None:
        self.api_key = os.environ.get("BOOKING_DEMAND_API_KEY", "")
        self.affiliate_id = os.environ.get("BOOKING_DEMAND_AFFILIATE_ID", "")
        self.base_url = os.environ.get("BOOKING_DEMAND_API_BASE", "https://demandapi.booking.com/3.3").rstrip("/")

    def _post(self, endpoint: str, body: dict[str, Any]) -> dict[str, Any]:
        request = Request(
            self.base_url + endpoint,
            data=json.dumps(body).encode("utf-8"),
            method="POST",
            headers={
                "Authorization": "Bearer " + self.api_key,
                "X-Affiliate-Id": self.affiliate_id,
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        )
        try:
            with urlopen(request, timeout=30) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            if exc.code in (401, 403):
                raise BookingProviderError("Der Booking.com-Partnerzugang ist ungültig oder noch nicht für diese API freigeschaltet.") from exc
            if exc.code == 429:
                raise BookingProviderError("Die Live-Suche ist gerade ausgelastet. Bitte versuche es gleich erneut.") from exc
            raise BookingProviderError("Der Unterkunftsanbieter hat die Anfrage gerade nicht verarbeitet.") from exc
        except (URLError, TimeoutError, json.JSONDecodeError, OSError) as exc:
            raise BookingProviderError("Die Verbindung zum Unterkunftsanbieter ist gerade nicht verfügbar.") from exc
        if not isinstance(payload, dict):
            raise BookingProviderError("Der Unterkunftsanbieter hat eine ungültige Antwort geliefert.")
        return payload

    def cities(self) -> list[dict[str, Any]]:
        global _city_cache
        now = time.monotonic()
        with _cache_lock:
            cached = _city_cache
        if cached and cached[0] > now:
            return cached[1]
        cities: list[dict[str, Any]] = []
        page = None
        for _ in range(30):
            body: dict[str, Any] = {"country": "de", "languages": ["de", "en-gb"], "rows": 1000}
            if page:
                body["page"] = page
            result = self._post("/common/locations/cities", body)
            cities.extend(result.get("data", []))
            page = (result.get("metadata") or {}).get("next_page")
            if not page:
                break
        with _cache_lock:
            _city_cache = (now + 21600, cities)
        return cities

    def resolve_city(self, city_name: str) -> dict[str, Any]:
        aliases = {"frankfurt": "frankfurt am main", "koln": "cologne", "munchen": "munich", "nurnberg": "nuremberg"}
        target = _norm(city_name)
        target = aliases.get(target, target)
        matches = []
        for item in self.cities():
            names = item.get("name") or {}
            normalized = {_norm(value) for value in names.values() if isinstance(value, str)}
            if target in normalized:
                matches.append(item)
        if not matches and len(target) >= 4:
            partials = []
            for item in self.cities():
                names = item.get("name") or {}
                normalized = {_norm(value) for value in names.values() if isinstance(value, str)}
                if any(name.startswith(target + " ") or target.startswith(name + " ") for name in normalized):
                    partials.append(item)
            if len(partials) == 1:
                matches = partials
        if not matches:
            raise BookingProviderError(f"Für {city_name} konnte kein eindeutiger Anbieter-Ort gefunden werden.")
        # Multiple translated or nearby city records are possible; prefer one
        # whose German display name matches the guest's original input.
        matches.sort(key=lambda item: _norm((item.get("name") or {}).get("de")) != _norm(city_name))
        return matches[0]

    def constants(self) -> dict[str, Any]:
        global _constants_cache
        now = time.monotonic()
        with _cache_lock:
            cached = _constants_cache
        if cached and cached[0] > now:
            return cached[1]
        result = self._post("/accommodations/constants", {
            "constants": ["accommodation_types", "accommodation_facilities", "room_facilities"],
            "languages": ["de", "en-gb"],
        }).get("data", {})
        with _cache_lock:
            _constants_cache = (now + 86400, result)
        return result

    @staticmethod
    def _type_ids(constants: dict[str, Any], requested_type: str) -> list[int]:
        wanted = _norm(requested_type)
        if not wanted or any(word in wanted for word in ("beides", "egal", "offen")):
            return []
        if "haus" in wanted or "house" in wanted:
            terms = ("holiday home", "vacation home", "ferienhaus", "cottage", "villa", "chalet")
        elif "apartment" in wanted or "wohnung" in wanted:
            terms = ("apartment", "ferienwohnung", "aparthotel", "apartment")
        else:
            return []
        found = []
        for item in constants.get("accommodation_types", []):
            label = _norm(_translated(item.get("name")))
            if any(term in label for term in terms):
                found.append(item.get("id"))
        return [int(item) for item in found if isinstance(item, int)]

    @staticmethod
    def _photo_url(value: Any) -> str | None:
        candidates: list[str] = []
        def visit(node: Any) -> None:
            if isinstance(node, str):
                if node.startswith("https://") and ("bstatic.com" in node or re.search(r"\.(?:jpe?g|png|webp)(?:\?|$)", node, re.I)):
                    candidates.append(node)
            elif isinstance(node, dict):
                for child in node.values():
                    visit(child)
            elif isinstance(node, list):
                for child in node:
                    visit(child)
        visit(value)
        return candidates[0] if candidates else None

    @staticmethod
    def _occupancy(rooms: list[dict[str, Any]]) -> int | None:
        capacities = []
        for room in rooms:
            value = room.get("max_occupancy") or room.get("occupancy")
            if isinstance(value, int):
                capacities.append(value)
            elif isinstance(value, dict):
                total = value.get("total")
                if isinstance(total, (int, float)):
                    capacities.append(int(total))
                else:
                    numbers = [value.get(key) for key in ("adults", "children") if isinstance(value.get(key), (int, float))]
                    if numbers:
                        capacities.append(int(sum(numbers)))
        return max(capacities) if capacities else None

    @staticmethod
    def _bedrooms(rooms: list[dict[str, Any]]) -> int | None:
        count = sum(1 for room in rooms if room.get("is_bedroom") is True)
        if count:
            return count
        count = sum(1 for room in rooms if "bedroom" in _norm(_translated(room.get("name"))) or "schlafzimmer" in _norm(_translated(room.get("name"))))
        return count or None

    @staticmethod
    def _area(rooms: list[dict[str, Any]]) -> int | None:
        values = []
        for room in rooms:
            value = room.get("size") or room.get("area")
            if isinstance(value, (int, float)):
                values.append(value)
            elif isinstance(value, dict):
                values.extend(v for k, v in value.items() if k in {"square_meters", "value", "sqm"} and isinstance(v, (int, float)))
        return round(max(values)) if values else None

    def search_offers(
        self,
        *,
        city_name: str,
        checkin: date | None,
        checkout: date | None,
        guests: int,
        requested_type: str = "",
        max_price: float | None = None,
        children: list[int] | None = None,
    ) -> dict[str, Any]:
        if not self.api_key or not self.affiliate_id:
            return {"configured": False, "offers": [], "message": "Echte Live-Angebote benötigen einen Booking.com-Partnerzugang."}
        city = self.resolve_city(city_name)
        city_id = city["id"]
        constants = self.constants()
        type_ids = self._type_ids(constants, requested_type)
        names_by_type = {item.get("id"): _translated(item.get("name"), "Unterkunft") for item in constants.get("accommodation_types", [])}
        facilities = {item.get("id"): _translated(item.get("name")) for item in constants.get("accommodation_facilities", [])}
        query_key = json.dumps([city_id, checkin.isoformat() if checkin else None, checkout.isoformat() if checkout else None, guests, requested_type, max_price, children or []], ensure_ascii=False)
        now = time.monotonic()
        with _cache_lock:
            cached = _offer_cache.get(query_key)
        if cached and cached[0] > now:
            return {"configured": True, "city": _translated(city.get("name"), city_name), "offers": cached[1], "availability_checked": bool(checkin and checkout), "cached": True}

        available_by_id: dict[int, dict[str, Any]] = {}
        if checkin and checkout:
            search_body: dict[str, Any] = {
                "city": city_id,
                "booker": {"country": "de", "platform": "desktop"},
                "checkin": checkin.isoformat(),
                "checkout": checkout.isoformat(),
                "guests": {"number_of_adults": max(1, guests - len(children or [])), "number_of_rooms": 1},
                "currency": "EUR",
                "rows": 100,
                "sort": {"by": "price", "direction": "ascending"},
                "extras": ["products", "extra_charges"],
                "filters": {"dormitories": "exclude"},
            }
            if children:
                search_body["guests"]["children"] = children
                search_body["guests"]["number_of_adults"] = max(1, guests - len(children))
            if type_ids:
                search_body["filters"]["accommodation_types"] = type_ids
            if max_price:
                search_body["filters"]["price"] = {"maximum": max_price}
            result = self._post("/accommodations/search", search_body)
            for item in result.get("data", []):
                if isinstance(item.get("id"), int):
                    available_by_id[item["id"]] = item
            property_ids = list(available_by_id)
            if not property_ids:
                return {"configured": True, "city": _translated(city.get("name"), city_name), "offers": [], "availability_checked": True, "message": "Für diese Reisedaten wurden keine verfügbaren Angebote gemeldet."}
            detail_body = {"accommodations": property_ids[:100], "extras": ["description", "photos", "rooms", "facilities", "policies"], "languages": ["de", "en-gb"]}
        else:
            detail_body = {"city": city_id, "extras": ["description", "photos", "rooms", "facilities", "policies"], "languages": ["de", "en-gb"], "rows": 100}
            if type_ids:
                detail_body["accommodation_types"] = type_ids

        details = self._post("/accommodations/details", detail_body).get("data", [])
        offers: list[dict[str, Any]] = []
        for detail in details:
            prop_id = detail.get("id")
            listing = available_by_id.get(prop_id, {})
            room_data = detail.get("rooms") or []
            name = _translated(detail.get("name"), "Unterkunft")
            type_name = names_by_type.get(detail.get("accommodation_type"), "Unterkunft")
            description = _translated((detail.get("description") or {}).get("text"), "Beschreibung beim Anbieter ansehen.")
            photo = self._photo_url(detail.get("photos"))
            # The guest finder promises images for every displayed offer. If
            # the partner feed does not provide a licensed property photo,
            # leave that record out instead of substituting an unrelated image.
            if not photo:
                continue
            facility_names = [facilities.get(item.get("id")) for item in detail.get("facilities", []) if facilities.get(item.get("id"))]
            room_names = [_translated(room.get("name")) for room in room_data if _translated(room.get("name"))]
            address = _translated((detail.get("location") or {}).get("address"), "")
            location = _translated(city.get("name"), city_name)
            rating = detail.get("rating") or {}
            price_obj = listing.get("price") or {}
            total_obj = price_obj.get("total") or price_obj.get("display") or {}
            total = total_obj.get("booker_currency") or total_obj.get("accommodation_currency")
            nights = (checkout - checkin).days if checkin and checkout else None
            detail_url = detail.get("url")
            if isinstance(detail_url, dict):
                detail_url = detail_url.get("web")
            url_value = listing.get("url") or detail_url
            if not isinstance(url_value, str) or not url_value.startswith("https://www.booking.com/"):
                continue
            # Booking.com's room entries describe bookable room types, not a
            # property's floor plan or bedroom count. Keep their names as
            # provider data and leave physical room count unknown.
            image = photo
            offer = {
                "id": f"booking-{prop_id}", "provider_id": prop_id,
                "name": name, "type": type_name, "sourceType": "Booking.com",
                "sourceUrl": url_value, "sourceLabel": "Auf Booking.com ansehen",
                "checked": date.today().isoformat(), "location": location + (f" · {address}" if address else ""),
                "regions": [_norm(location), "deutschland"], "guests": self._occupancy(room_data),
                "capacityBasis": "Maximale Belegung eines Raumangebots laut Anbieter" if self._occupancy(room_data) else None,
                "searchedGuests": guests, "area": None, "rooms": None,
                "roomTypes": room_names[:12] or None,
                "image": image, "alt": f"Originalfoto des Angebots {name} auf Booking.com" if image else f"Für {name} sind keine Fotos im Anbieterfeed enthalten",
                "imageLabel": "Originalfoto · Booking.com" if image else "Kein Foto im Anbieterfeed",
                "features": facility_names[:12], "difference": "Anbieterangaben laut Booking.com; Details und Bedingungen vor der Buchung prüfen.",
                "layout": None, "description": description,
                "availabilityChecked": bool(checkin and checkout), "priceTotal": total,
                "currency": (listing.get("currency") or {}).get("booker") or "EUR", "nights": nights,
                "rating": rating.get("review_score"), "ratingCount": rating.get("number_of_reviews"),
                "checkinFrom": ((detail.get("checkin_checkout_times") or {}).get("checkin_from")),
                "checkoutUntil": ((detail.get("checkin_checkout_times") or {}).get("checkout_from")),
                "demoOnly": False, "searchUrl": None,
                "knowledge": {
                    "property_id": f"booking-{prop_id}", "property_name": name,
                    "facts": {
                        "description": description,
                        "location": location + (f" · {address}" if address else ""),
                        "capacity": f"Anfrage für {guests} Gäste" + (f"; ein Raumangebot nennt bis zu {self._occupancy(room_data)} Gäste" if self._occupancy(room_data) else "; Belegung im Anbieterfeed nicht angegeben"),
                        "rooms": "Der Anbieterfeed weist keine verlässliche Schlafzimmerzahl aus.",
                        "room_types": ", ".join(room_names[:12]) or "Keine Raumtypen im Anbieterfeed angegeben.",
                        "area": "Wohnfläche im Anbieterfeed nicht angegeben.",
                        "features": ", ".join(facility_names) or "Ausstattung im Anbieterfeed nicht angegeben",
                        "checkin": ((detail.get("checkin_checkout_times") or {}).get("checkin_from")) or "nicht angegeben",
                        "checkout_from": ((detail.get("checkin_checkout_times") or {}).get("checkout_from")) or "nicht angegeben",
                        "price": f"Gesamtpreis im Anbieterfeed: {total} {((listing.get('currency') or {}).get('booker') or 'EUR')} für {nights} Nächte; bei flexiblen Daten beim Anbieter prüfen." if total and nights else "Preis und Termine beim Anbieter prüfen.",
                    },
                },
            }
            offers.append(offer)
        with _cache_lock:
            _offer_cache[query_key] = (now + 300, offers)
        return {"configured": True, "city": _translated(city.get("name"), city_name), "offers": offers, "availability_checked": bool(checkin and checkout)}
