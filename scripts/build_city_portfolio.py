"""Build clearly labelled city and Landkreis Böblingen sample concepts.

The generated apartment concepts are fictional product illustrations or
photographic visualizations. They are not offers and must never be presented as
real or bookable accommodations.
"""
from __future__ import annotations

import html
import json
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
IMAGE_DIR = ROOT / "assets" / "properties" / "city-concepts"
OUTPUT = ROOT / "backend" / "city_portfolio.json"

# Current German large cities (>100,000 residents) in the 2025 table.
# Source: https://de.wikipedia.org/wiki/Liste_der_Gro%C3%9Fst%C3%A4dte_in_Deutschland
CITIES_BY_STATE = {
    "Berlin": ["Berlin"],
    "Hamburg": ["Hamburg"],
    "Bayern": ["München", "Nürnberg", "Augsburg", "Regensburg", "Ingolstadt", "Würzburg", "Fürth", "Erlangen"],
    "Nordrhein-Westfalen": ["Köln", "Düsseldorf", "Dortmund", "Essen", "Duisburg", "Bochum", "Wuppertal", "Bielefeld", "Bonn", "Mönchengladbach", "Gelsenkirchen", "Aachen", "Münster", "Krefeld", "Oberhausen", "Hagen", "Hamm", "Mülheim an der Ruhr", "Leverkusen", "Solingen", "Herne", "Paderborn", "Neuss", "Recklinghausen", "Remscheid", "Bergisch Gladbach", "Siegen", "Moers", "Bottrop"],
    "Hessen": ["Frankfurt am Main", "Wiesbaden", "Kassel", "Darmstadt", "Offenbach am Main"],
    "Sachsen": ["Leipzig", "Dresden", "Chemnitz"],
    "Baden-Württemberg": ["Stuttgart", "Mannheim", "Karlsruhe", "Freiburg im Breisgau", "Heidelberg", "Pforzheim", "Heilbronn", "Ulm", "Reutlingen"],
    "Bremen": ["Bremen", "Bremerhaven"],
    "Niedersachsen": ["Hannover", "Braunschweig", "Oldenburg (Oldb)", "Osnabrück", "Göttingen", "Wolfsburg", "Salzgitter"],
    "Schleswig-Holstein": ["Kiel", "Lübeck"],
    "Sachsen-Anhalt": ["Magdeburg", "Halle (Saale)"],
    "Rheinland-Pfalz": ["Mainz", "Ludwigshafen am Rhein", "Koblenz", "Trier", "Kaiserslautern"],
    "Thüringen": ["Erfurt", "Jena"],
    "Mecklenburg-Vorpommern": ["Rostock"],
    "Brandenburg": ["Potsdam"],
    "Saarland": ["Saarbrücken"],
}

BOEBLINGEN_MUNICIPALITIES = [
    "Aidlingen", "Altdorf", "Böblingen", "Bondorf", "Deckenpfronn", "Ehningen",
    "Gärtringen", "Gäufelden", "Grafenau", "Herrenberg", "Hildrizhausen",
    "Holzgerlingen", "Jettingen", "Leonberg", "Magstadt", "Mötzingen",
    "Nufringen", "Renningen", "Rutesheim", "Schönaich", "Sindelfingen",
    "Steinenbronn", "Waldenbuch", "Weil der Stadt", "Weil im Schönbuch", "Weissach",
]

PALETTES = [
    ("#e9d9c7", "#839a83", "#cf9e79", "#466b58"),
    ("#dbe4e4", "#607f87", "#d8b36a", "#52725d"),
    ("#eee1d7", "#9c806f", "#7b9a91", "#566e62"),
    ("#d9d9e4", "#756b87", "#d59a87", "#607b67"),
    ("#e8e4d1", "#a38d5a", "#8eaaa0", "#536d57"),
    ("#dce2d3", "#6f8c70", "#ca8d72", "#4d6a57"),
    ("#e8dede", "#946f75", "#d2ac6d", "#5b7662"),
    ("#d7e4e8", "#6c899a", "#c59680", "#536f5b"),
    ("#ece0c8", "#a28159", "#87978c", "#4f7059"),
    ("#e2dce9", "#877797", "#c99983", "#58705b"),
    ("#e2e7db", "#728567", "#c4a568", "#526a58"),
    ("#e7d9d3", "#986f62", "#7b9e9a", "#4c6e5d"),
]

STYLES = [
    ("Altbau mit Erker", "hohe Fenster und warme Holztöne"),
    ("Helles Stadtloft", "offener Wohnbereich und klare Linien"),
    ("Ruhiges Zuhause", "weiche Farben und eine gemütliche Leseecke"),
    ("Familienwohnung", "großer Esstisch und flexibler Wohnraum"),
    ("Kompaktes Apartment", "clevere Ecken und ein kleiner Essplatz"),
    ("Dachwohnung", "schräge Decke und ein heller Rückzugsort"),
    ("Grünes Wohnen", "Pflanzen, Naturfarben und ein ruhiger Wohnbereich"),
    ("Arbeitsfreundliches Loft", "ein kleiner Schreibtisch am Fenster"),
]


def slug(value: str) -> str:
    value = value.lower().replace("ß", "ss").replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")


def svg_for(name: str, city: str, index: int, style: str) -> str:
    wall, accent, sofa, plant = PALETTES[index % len(PALETTES)]
    scene = index % len(STYLES)
    window_x = 84 + (index % 4) * 10
    sofa_y = 340 + (index % 3) * 9
    table_x = 516 + (index % 5) * 11
    desk = scene == 7
    loft = scene == 1
    caption = html.escape(name)
    city_text = html.escape(city)
    window = (
        f'<rect x="{window_x}" y="105" width="306" height="226" rx="8" fill="#b8d2d4" stroke="#fffaf4" stroke-width="15"/>'
        f'<path d="M{window_x+153} 110V326 M{window_x+5} 218H{window_x+301}" stroke="#fffaf4" stroke-width="9"/>'
        f'<path d="M{window_x+8} 279 Q{window_x+65} 230 {window_x+125} 277 T{window_x+300} 267V326H{window_x+8}Z" fill="#91ac91" opacity=".77"/>'
    )
    desk_svg = '<rect x="618" y="290" width="205" height="12" rx="6" fill="#9b7655"/><path d="M640 300V353 M799 300V353" stroke="#806044" stroke-width="8"/><rect x="672" y="249" width="72" height="37" rx="4" fill="#f2e7d7" stroke="#8c7865" stroke-width="3"/><rect x="691" y="356" width="104" height="8" rx="4" fill="#7c8b77"/>' if desk else ""
    loft_svg = '<path d="M74 453V75L470 38V453" fill="none" stroke="#a8957d" stroke-width="11" opacity=".55"/><path d="M77 84L469 48" stroke="#eee8dc" stroke-width="25"/>' if loft else ""
    plants = (
        f'<path d="M824 409V300 M824 332Q780 317 786 285Q817 293 824 318 M824 350Q866 326 868 294Q838 303 824 336 M824 370Q785 360 776 340Q807 337 824 356" stroke="{plant}" stroke-width="9" fill="none" stroke-linecap="round"/>'
        f'<path d="M797 410H851L844 451H804Z" fill="{accent}"/>'
    )
    rug = PALETTES[(index + 3) % len(PALETTES)][0]
    extra = f'<circle cx="{160 + (index*37)%650}" cy="{147 + (index*19)%82}" r="18" fill="#f7f0dd" opacity=".78"/><rect x="{172 + (index*17)%250}" y="{372 + (index%4)*7}" width="104" height="67" rx="5" fill="{accent}" opacity=".84"/>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="620" viewBox="0 0 960 620" role="img" aria-label="Illustration eines fiktiven Wohnkonzepts in {city_text}">
<defs><linearGradient id="light" x2="0" y2="1"><stop stop-color="{wall}"/><stop offset="1" stop-color="#faf7f0"/></linearGradient><linearGradient id="floor" x2="0" y2="1"><stop stop-color="#d6bc9a"/><stop offset="1" stop-color="#b8926b"/></linearGradient></defs>
<rect width="960" height="620" fill="#e8ece5"/><rect x="36" y="30" width="888" height="476" rx="19" fill="url(#light)"/><path d="M36 426H924V487Q924 506 905 506H55Q36 506 36 487Z" fill="url(#floor)"/>
{loft_svg}{window}<rect x="75" y="69" width="810" height="21" rx="10" fill="#f8f3eb" opacity=".85"/>
<rect x="416" y="173" width="119" height="78" rx="3" fill="#ead5b5"/><rect x="428" y="185" width="95" height="55" rx="2" fill="#f5ebd9"/><path d="M448 228L468 203L488 228Z" fill="{plant}"/><circle cx="506" cy="205" r="8" fill="{accent}"/>
<rect x="106" y="{sofa_y+34}" width="399" height="105" rx="27" fill="{sofa}"/><rect x="124" y="{sofa_y}" width="360" height="85" rx="24" fill="{sofa}"/><rect x="146" y="{sofa_y+13}" width="125" height="52" rx="18" fill="#f5eee3" opacity=".83"/><rect x="287" y="{sofa_y+12}" width="132" height="52" rx="18" fill="{wall}"/><path d="M127 {sofa_y+120}V{sofa_y+162} M483 {sofa_y+120}V{sofa_y+162}" stroke="#6d5946" stroke-width="12"/>
<ellipse cx="{table_x+105}" cy="445" rx="125" ry="32" fill="{rug}" opacity=".9"/><rect x="{table_x}" y="399" width="206" height="34" rx="13" fill="#a87d5c"/><path d="M{table_x+22} 432L{table_x+36} 478 M{table_x+185} 432L{table_x+171} 478" stroke="#795d46" stroke-width="9"/>
{extra}{plants}{desk_svg}
<path d="M590 74V120 M566 120H614L607 137H573Z" fill="#d8b765"/><circle cx="590" cy="140" r="22" fill="#fff0bd" opacity=".7"/>
<rect x="36" y="523" width="888" height="69" rx="14" fill="#fffdf8"/><text x="61" y="554" font-family="Arial,sans-serif" font-size="19" font-weight="700" fill="#314d3b">{caption}</text><text x="61" y="578" font-family="Arial,sans-serif" font-size="12" fill="#657468">Wohnkonzept · Musterbild · keine echte Unterkunft</text>
</svg>'''


def fact(fid: str, terms: list[str], de: str, en: str) -> dict:
    return {"id": fid, "terms": terms, "source": "Fiktives Musterkonzept", "answers": {"de": de, "en": en}}


def make_item(city: str, state: str, index: int, county: bool = False, variant: int = 0) -> dict:
    style, style_note = STYLES[(index + variant * 3) % len(STYLES)]
    specs = [(2, 46, 2), (3, 58, 2), (4, 72, 3), (5, 86, 3), (6, 98, 4)]
    spec = specs[(index + variant * 2) % len(specs)]
    guests, area, rooms = spec
    property_type = ("Apartment", "Ferienhaus", "Apartment", "Ferienhaus")[variant % 4]
    if city == "Berlin" and variant == 1:
        property_type = "Apartment"
    example_price = round(48 + guests * 9 + area * 0.58 + (index % 4) * 7)
    prefix = "boeblingen" if county else "germany"
    identifier = f"demo-{prefix}-{slug(city)}" + (f"-{variant + 1}" if variant else "")
    name = f"{style} · {city}"
    berlin_photo = {
        0: "assets/properties/city-concepts/demo-germany-berlin-altbau.png",
        1: "assets/properties/city-concepts/demo-germany-berlin-family.png",
    }
    image_rel = berlin_photo.get(variant) if city == "Berlin" else None
    image_rel = image_rel or f"assets/properties/city-concepts/{identifier}.svg"
    neighborhood = "Landkreis Böblingen" if county else state
    aliases = [slug(city).replace("-", " ")]
    if city == "München":
        aliases.append("Munchen")
    if city in {"Böblingen", "Mötzingen", "Schönaich", "Gärtringen", "Gäufelden"}:
        aliases.append(slug(city).replace("oe", "o").replace("ae", "a").replace("ue", "u").replace("ss", "ß"))
    if state == "Baden-Württemberg":
        aliases.append("Baden Wuerttemberg")
    if county:
        aliases.append("Landkreis Boeblingen")
    search_url = f"https://www.booking.com/searchresults.html?ss={quote(city, safe='')}"
    capacity = f"Das fiktive Musterkonzept ist für bis zu {guests} Personen gedacht; es ist kein konkretes Unterkunftsangebot." if guests != 1 else "Das fiktive Musterkonzept ist für eine Person gedacht; es ist kein konkretes Unterkunftsangebot."
    size = f"Als reine Entwurfsidee sind etwa {area} m² und {rooms} Zimmer skizziert. Das ist keine bestätigte Inseratsangabe."
    style_description = f"Illustratives {area}-m²-{property_type.lower()}-Wohnkonzept für {guests} Gäste in {city}: {style_note}. Fiktiv und nicht buchbar."
    price_note = f"Fiktiver Demo-Richtwert: etwa {example_price} € pro Nacht. Das ist kein echter Unterkunftspreis."
    check_in_time = ("14:00", "15:00", "16:00")[(index + variant) % 3]
    check_out_time = ("10:00", "11:00")[(index + variant) % 2]
    checkin_methods = ("eine Schlüsselbox", "einen digitalen Türcode", "einen Schlüsseltresor")
    checkin_method = checkin_methods[(index + variant) % len(checkin_methods)]
    demo_parking = (
        (
            "Im fiktiven Muster ist beispielhaft ein kostenloser Außenstellplatz vorgesehen. Das ist kein realer oder garantierter Parkplatz.",
            "The fictional sample includes one example free outdoor parking space. This is not real or guaranteed parking.",
        ),
        (
            "Für diese Wohnidee ist im Demo-Beispiel kein eigener Stellplatz vorgesehen. Öffentliche Parkmöglichkeiten sind nicht geprüft.",
            "This sample concept has no private parking space. Public parking has not been checked.",
        ),
        (
            "Das Muster zeigt beispielhaft öffentliche Straßenparkplätze; Verfügbarkeit und Kosten sind nicht geprüft oder garantiert.",
            "The sample concept suggests public street parking; availability and cost are not checked or guaranteed.",
        ),
    )[(index + variant) % 3]
    demo_work = (
        (
            "Als fiktive Beispielausstattung sind WLAN und ein kleiner Arbeitsplatz vorgesehen; beides ist keine reale Zusage.",
            "The fictional sample includes Wi-Fi and a small workspace; neither is a real-world guarantee.",
        ),
        (
            "WLAN ist als Demo-Ausstattung vorgesehen. Ein eigener Arbeitsplatz ist im Muster nicht dargestellt.",
            "Wi-Fi is included as sample equipment. The concept does not show a dedicated workspace.",
        ),
    )[(index + variant) % 2]
    demo_pets = (
        (
            "Die fiktive Beispielregel erlaubt Haustiere. Das ist keine echte Hausregel eines buchbaren Objekts.",
            "The fictional sample rule allows pets. This is not a real house rule for a bookable property.",
        ),
        (
            "Im fiktiven Beispiel sind Haustiere nicht vorgesehen. Das ist keine echte Hausregel eines buchbaren Objekts.",
            "Pets are not included in this fictional sample. This is not a real house rule for a bookable property.",
        ),
    )[(index + variant) % 2]
    demo_accessibility = (
        (
            "Der Demo-Entwurf ist beispielhaft stufenarm gedacht, aber nicht auf Barrierefreiheit geprüft oder dafür zugesichert.",
            "The sample is illustrated as having few steps, but it has not been assessed or certified for accessibility.",
        ),
        (
            "Barrierefreiheit ist für dieses fiktive Konzept nicht belegt; ein realer Zugang lässt sich daraus nicht ableiten.",
            "Accessibility is not established for this fictional concept; no real access conditions can be inferred.",
        ),
    )[(index + variant) % 2]
    layout = ["Wohnen & Essen", "Schlafen"] + (["Zusätzliches Zimmer"] if rooms >= 3 else []) + (["Weiteres Schlafzimmer"] if rooms >= 4 else []) + ["Bad"]
    features = [style_note, f"Entwurf: ca. {area} m² · {rooms} Zimmer", f"Idee für bis zu {guests} Gäste", f"Demo-Richtwert ca. {example_price} €/Nacht · nicht buchbar"]
    type_fact = fact("property_type", ["typ", "art der unterkunft", "haus", "apartment", "wohnung", "type"], f"Das ist ein fiktives {property_type.lower()}-Wohnkonzept. Es gibt kein entsprechendes buchbares Inserat.", f"This is a fictional {property_type.lower()} housing concept. There is no corresponding bookable listing.")
    answers = [
        type_fact,
        fact("example_price", ["preis", "kosten", "budget", "price", "cost"], price_note, f"Fictional demo reference: about EUR {example_price} per night. This is not a real accommodation price."),
        fact("capacity", ["gäste", "personen", "person", "bett", "schlaf", "people", "guest", "sleep"], capacity, f"The fictional sample concept is designed for up to {guests} people; it is not a real accommodation offer."),
        fact("size", ["größe", "fläche", "qm", "m²", "square", "sqm", "zimmer", "room"], size, f"As a design idea only, about {area} square metres and {rooms} rooms are sketched. This is not a verified listing detail."),
        fact("concept", ["echt", "wirklich", "verfügbar", "buchbar", "availability", "available", "real", "booking", "buchen", "preis", "price"], "Wichtig: Das ist eine fiktive StayMate-Wohnidee, keine echte Unterkunft und kein Inserat. Für echte Unterkünfte in dieser Stadt öffne die externe Stadtsuche; Preis und Verfügbarkeit prüfst du dort.", "Important: This is a fictional StayMate accommodation concept, not a real property or listing. Open the external city search for real stays; check price and availability there."),
        fact("style", ["ausstattung", "wlan", "park", "küche", "balkon", "terrasse", "feature", "amenit", "parking", "wifi", "kitchen"], f"Die Illustration zeigt nur ein Gestaltungsbeispiel ({style_note}). Einzelne Angaben zu Ausstattung und Aufenthalt sind als fiktive Demo-Fakten gekennzeichnet; sie sind keine realen Inseratsangaben.", f"The illustration is only a design example ({style_note}). Individual amenity and stay details are labelled as fictional sample facts; they are not real listing details."),
        fact("checkin", ["check-in", "check in", "checkin", "ankunft", "arrival", "arrive", "einchecken", "schlüssel", "schluessel", "key", "door code", "ab wann", "wann kann ich rein"], f"Fiktiver Demo-Richtwert: Check-in ab {check_in_time} Uhr über {checkin_method}. Das ist keine reale Zugangsinformation; ein früherer Check-in ist nicht zugesagt.", f"Fictional sample guideline: check-in from {check_in_time} via {checkin_method}. This is not real access information; early check-in is not promised."),
        fact("checkout", ["check-out", "check out", "checkout", "auschecken", "abreise", "departure", "leave", "bis wann"], f"Fiktiver Demo-Richtwert: Check-out bis {check_out_time} Uhr. Das ist keine reale Vorgabe; eine spätere Abreise ist nicht zugesagt.", f"Fictional sample guideline: check-out by {check_out_time}. This is not a real requirement; late check-out is not promised."),
        fact("parking", ["park", "parkplatz", "parkplätze", "stellplatz", "parken", "parking", "car park", "garage", "auto", "voiture", "coche", "parcheggio", "parkeren"], *demo_parking),
        fact("work", ["wlan", "wi-fi", "wifi", "internet", "arbeiten", "arbeit", "work", "workspace", "desk", "schreibtisch", "remote"], *demo_work),
        fact("pets", ["haustier", "haustiere", "hund", "hunde", "katze", "katzen", "pets", "pet", "dogs", "dog", "cats", "cat", "tiere"], *demo_pets),
        fact("accessibility", ["barrierefrei", "barrierefreiheit", "rollstuhl", "stufen", "treppe", "zugang", "accessible", "accessibility", "wheelchair", "steps"], *demo_accessibility),
        fact("sleeping", ["bett", "betten", "schlafplatz", "schlafplätze", "bed", "beds", "bedding", "bedroom", "schlafzimmer"], f"Die Wohnidee skizziert {rooms} Zimmer für bis zu {guests} Gäste. Eine konkrete Bettenzahl oder Bettenaufteilung ist im fiktiven Muster nicht festgelegt.", f"The sample concept sketches {rooms} rooms for up to {guests} guests. It does not specify an actual bed count or bed layout."),
        fact("kitchen", ["küche", "küchenzeile", "kochen", "kitchen", "cook", "cooking"], "Eine einfache Küche ist als fiktive Demo-Ausstattung vorgesehen; Geräte und tatsächliche Ausstattung sind nicht bestätigt.", "A basic kitchen is included as fictional sample equipment; appliances and real-world amenities are not confirmed."),
        fact("amenities", ["fernseher", "tv", "klimaanlage", "waschmaschine", "trockner", "handtuch", "handtücher", "bettwäsche", "towels", "linen", "air conditioning", "washing machine", "dryer"], "Dieses Ausstattungsdetail ist im fiktiven Musterkonzept nicht festgelegt. Es gibt kein echtes Inserat, in dem es bestätigt werden könnte.", "This amenity is not specified in the fictional sample concept. There is no real listing in which it could be confirmed."),
        fact("booking_policy", ["storno", "stornierung", "stornieren", "cancel", "cancellation", "erstattung", "refund", "buchen", "buchung", "reservierung", "reservation", "deposit", "kaution"], "Für diese fiktive Wohnidee gibt es keine Buchung, Stornierungsbedingungen, Kaution oder Erstattung; sie ist kein buchbares Angebot.", "This fictional concept has no booking, cancellation terms, deposit or refund policy; it is not bookable."),
        fact("location", ["lage", "wo", "stadt", "ort", "location", "where", "city"], f"Das Wohnkonzept wurde zur Orientierung dem Suchort {city} ({neighborhood}) zugeordnet. Es gibt keine konkrete Adresse oder reale Unterkunft.", f"This sample concept is associated with {city} ({neighborhood}) for search orientation. It has no real address or accommodation."),
    ]
    return {
        "id": identifier, "name": name, "type": property_type, "source_type": "Wohnidee · fiktives Konzept",
        "location": f"{city} · {neighborhood}", "regions": [city, *aliases, neighborhood, state, "Deutschland"],
        "state": state, "county": "Landkreis Böblingen" if county else None,
        "guests": guests, "area": area, "rooms": rooms, "example_price_per_night": example_price,
        "check_in": f"Fiktiver Demo-Richtwert ab {check_in_time} Uhr",
        "check_out": f"Fiktiver Demo-Richtwert bis {check_out_time} Uhr", "image": image_rel,
        "image_alt": (
            f"Fotorealistische KI-Visualisierung eines fiktiven {property_type.lower()} in {city}; kein Inseratsfoto"
            if city == "Berlin" and variant in berlin_photo else
            f"Individuelle StayMate-Konzeptillustration eines fiktiven {property_type.lower()} in {city}"
        ),
        "image_label": "KI-Visualisierung · kein Inseratsfoto" if city == "Berlin" and variant in berlin_photo else "Demo-Visualisierung · kein Inseratsfoto",
        "source_url": None,
        "source_label": "", "search_url": search_url,
        "search_label": f"Echte Unterkünfte in {city} suchen",
        "checked": None, "demo_only": True, "availability_checked": False,
        "description": style_description,
        "difference": "Fiktive Gestaltungsidee zur Orientierung. Bild, Wohnfläche und Ausstattung sind keine echten Inseratsangaben.",
        "features": features, "layout": layout, "facts": answers,
        "_image_svg": None if city == "Berlin" and variant in berlin_photo else svg_for(name, city, index * 5 + variant, style),
    }


def main() -> None:
    IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    all_cities = [(city, state) for state, cities in CITIES_BY_STATE.items() for city in cities]
    assert len(all_cities) == 79, f"Expected 79 large cities, got {len(all_cities)}"
    assert len(set(city for city, _ in all_cities)) == 79, "Duplicate city in large-city list"
    assert len(BOEBLINGEN_MUNICIPALITIES) == 26
    items: list[dict] = []
    for index, (city, state) in enumerate(all_cities):
        # Larger cities get different portfolio sizes (2–4 concepts); each
        # location has its own names, source facts, floor-plan sketch and image.
        for variant in range(2 + index % 3):
            items.append(make_item(city, state, index, variant=variant))
    offset = len(items)
    for i, place in enumerate(BOEBLINGEN_MUNICIPALITIES):
        items.append(make_item(place, "Baden-Württemberg", offset + i, county=True))
    for item in items:
        image = item.pop("_image_svg")
        if image:
            (ROOT / item["image"]).write_text(image, encoding="utf-8")
    OUTPUT.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Generated {len(items)} image concepts: {len(all_cities)} large cities with 2–4 options each + {len(BOEBLINGEN_MUNICIPALITIES)} Böblingen district towns.")


if __name__ == "__main__":
    main()
