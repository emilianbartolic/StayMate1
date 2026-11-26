"""Provider integration readiness without pretending that credentials are live."""
from __future__ import annotations

import os


def integration_status() -> list[dict]:
    return [
        {
            "provider": "Booking.com Demand API · Unterkunftssuche",
            "connected": bool(os.environ.get("BOOKING_DEMAND_API_KEY") and os.environ.get("BOOKING_DEMAND_AFFILIATE_ID")),
            "adapter_available": True,
            "status": "configured" if os.environ.get("BOOKING_DEMAND_API_KEY") and os.environ.get("BOOKING_DEMAND_AFFILIATE_ID") else "partner_access_required",
            "requirements": [
                "Freigeschalteter Booking.com Managed Affiliate Partnerzugang",
                "API-Key und Affiliate-ID; Geheimnisse bleiben nur im Backend",
                "Partnerzugang, der Inseratsfotos und benötigte Detailfelder liefert",
            ],
            "secret_configured": bool(os.environ.get("BOOKING_DEMAND_API_KEY") and os.environ.get("BOOKING_DEMAND_AFFILIATE_ID")),
            "scope": "Angebote und Verfügbarkeit abfragen; keine Buchung, Zahlung oder Hostnachricht",
        },
        {
            "provider": "Airbnb",
            "connected": False,
            "adapter_available": False,
            "status": "partner_access_required",
            "requirements": [
                "Zugang zu einem genehmigten Airbnb-API-Programm bzw. Software-Partnerkonto",
                "Offizielle API-Anmeldedaten und freigegebener Integrationsumfang",
                "Autorisierte Verbindung des jeweiligen Gastgeberkontos und Inserats",
                "Implementierung und Abnahme der passenden API-Funktionen",
            ],
            "secret_configured": bool(os.environ.get("AIRBNB_API_CLIENT_ID") and os.environ.get("AIRBNB_API_CLIENT_SECRET")),
        },
        {
            "provider": "Booking.com",
            "connected": False,
            "adapter_available": False,
            "status": "connectivity_partner_onboarding_required",
            "requirements": [
                "Aufnahme als Booking.com Connectivity Partner",
                "API-Token-Maschinenkonto und passende Rechte für jedes verbundene Objekt",
                "Ausdrückliche Freigabe des Gastgebers für die benötigten Verbindungstypen",
                "Implementierung, Zertifizierung und produktive Freischaltung der Endpunkte",
            ],
            "secret_configured": bool(os.environ.get("BOOKING_API_TOKEN") and os.environ.get("BOOKING_PARTNER_ID")),
        },
    ]
