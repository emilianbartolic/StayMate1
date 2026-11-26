# StayMate AI — Stilkarte

**Version:** 1.0  
**Leitgedanke:** *Form follows function.*

## Projektkontext

StayMate AI ist ein Gästesupport-Agent für Ferienunterkünfte. Er verbindet technische Unterstützung (z. B. Check-in, WLAN, Parken und Host-Tickets) mit sozialer Unterstützung (z. B. Empathie, Deeskalation und situationsgerechte Kommunikation).

Das eigenständige Logo liegt als [staymate-logo.png](assets/staymate-logo.png) vor. Es verbindet ein abstrahiertes „S“ mit einer Sprechblase und einem kleinen Haus-/Türsymbol: Agent, Kommunikation und Unterkunft in einem Zeichen.

Wir sind die Auftraggeber: Die Stilkarte beschreibt, wie der Agent für Gäste und Gastgeber verständlich, vertrauenswürdig und handlungsorientiert sichtbar wird.

## Zielgruppen

- **Gäste:** möchten schnell eine verlässliche und freundliche Antwort erhalten.
- **Gastgeber:** möchten eskalierte Anliegen priorisieren, bearbeiten und nachvollziehen können.

## Hauptaufgabe und Hauptaktion

- **Hauptaufgabe:** technische und soziale Gästefragen bearbeiten.
- **Hauptaktion:** Frage senden.
- **Host-Aktion:** Host informieren oder Ticket als bearbeitet markieren.

## Visuelles Muster

Wir kombinieren zwei beobachtete Muster aus den geprüften Vorlagen:

1. Eine klare öffentliche Kommunikation mit Kontakt-/Inbox-Funktion.
2. Ein fokussiertes internes Dashboard mit Status, Kennzahlen und Listen.

Für StayMate bedeutet das:

- Gastansicht: Chat, Vorschlagsfragen und sichtbarer Agenten-Trace.
- Hostansicht: offene Tickets, Priorität, Status und Host Advisor.
- Die wichtigste Information steht immer vor erweiterten Funktionen.

Die Vorlagen dienten nur als Referenz für Struktur und Muster, nicht als Quelle für Texte, Marken oder Medien: [Real Estate Agent Site](https://lovable.dev/templates/websites/services/real-estate-agent-site) und [Budget Dashboard](https://lovable.dev/templates/apps/internal-tools/budget-pulse-budget-vs-actual-dashboard-template).

## Bewusste Nicht-Übernahme

Wir übernehmen keine Video-Hero-Fläche, Parallax-Animationen oder dekorative Scroll-Effekte. Diese Elemente passen zur Markenpräsentation einer Immobilienseite, würden aber beim direkten Gästesupport vom Hauptweg ablenken.

Wir übernehmen außerdem keine Budget-/Finanzsprache aus dem Dashboard-Muster. Stattdessen sprechen wir über Anliegen, Tickets, Prioritäten und Host-Entscheidungen.

## Farbpalette

| Rolle | Farbe | Verwendung |
|---|---|---|
| Primär | `#172F52` Dunkelblau | Navigation, Host-Bereich, Vertrauen |
| Aktion | `#2E6EE7` Blau | Primärbutton, aktive Agentenfunktion, Links |
| Fläche | `#F8F7F4` Warmweiß | ruhiger Seitenhintergrund, Kartenflächen |

Grün und Amber dürfen ausschließlich als funktionale Statushinweise verwendet werden, z. B. „sicher beantwortet“ oder „Host-Entscheidung nötig“. Sie sind keine zusätzlichen Markenfarben.

## Typografie

```css
font-family: Inter, ui-sans-serif, system-ui, -apple-system, sans-serif;
```

Die Systemschrift bleibt gut lesbar für kurze Gastnachrichten, längere soziale Antworten und kompakte Dashboard-Daten. Überschriften sind klar und eher kompakt; Fließtext verwendet ausreichend Zeilenhöhe.

## Buttonregel

Pro Ansicht gibt es genau eine primäre Aktion:

- Gastansicht: **Frage senden**
- Host-Dashboard: **Als bearbeitet markieren**
- Eskalierter Fall: **Host informieren**

Sekundäre Aktionen wie „Antwortentwurf kopieren“, „Filter“ oder „Details anzeigen“ sind visuell zurückgenommen. Keine gleichrangige Gruppe aus mehreren auffälligen Buttons.

## Bildregel

Bilder werden nur eingesetzt, wenn sie Orientierung oder Vertrauen schaffen:

- geprüfte Aufnahme der Unterkunft
- optional ein neutrales Gastgeberprofilbild
- keine dekorativen Stockbilder im Chat
- keine Airbnb-Medien, fremden Texte oder Marken ungeprüft kopieren

Die Agentenfunktion steht im Vordergrund; Bilder dürfen die Frage-Antwort-Aufgabe nicht überdecken.

## Bildauswahl für die erste Umsetzung

Die folgenden Bildreferenzen passen zur ruhigen, vertrauensvollen Unterkunftsatmosphäre. Sie stammen nicht aus den Lovable-Vorlagen und sollen vor Verwendung anhand der jeweiligen Lizenz- und Attribution-Hinweise geprüft werden.

| Einsatz | Bildreferenz | Verwendung |
|---|---|---|
| Unterkunfts-Header | [Bright and airy living room](https://unsplash.com/photos/a-bright-and-airy-living-room-with-modern-decor-ZuHIek5xn_I) | Ein einzelnes, breites Bild für Unterkunft und Vertrauen; nicht im Chat wiederholen. |
| Detail-/Orientierungsbild | [Modern interior hallway](https://unsplash.com/photos/modern-interior-hallway-with-warm-lighting-and-furniture-VRzUyuHy8p0) | Optional bei Check-in-/Zugangsinfos, falls es die Orientierung unterstützt. |
| Visuelles Hintergrundmotiv | [Blue and white abstract background](https://unsplash.com/photos/a-white-and-blue-abstract-background-with-lines-JiBmiyU9mCc) | Sehr sparsam für eine leere Dashboard-Fläche oder eine Abschnittskarte. |
| Soziales Vertrauenssignal | [Smiling person in warm light](https://unsplash.com/photos/a-woman-smiles-in-soft-warm-light-fBRoULRI3Vw) | Nur als neutrales Profil-/Host-Bild verwenden, wenn die Person und die Nutzung freigegeben sind. |

**Bildbehandlung:** 16:9 für Unterkunftsaufnahmen, abgerundete Ecken mit 12 px, keine Text-Overlays auf wichtigen Bilddetails, dezente Helligkeitsanpassung statt starker Filter. Pro Ansicht höchstens ein großes Bild.

**Lizenzhinweis:** Die verlinkten Ergebnisse sind auf den jeweiligen Unsplash-Seiten als „Free to use under the Unsplash License“ ausgewiesen; vor Veröffentlichung trotzdem die aktuelle Lizenzseite, Urheberangabe und eventuelle Personen-/Model-Rechte prüfen. Die Bildseiten sind nur Auswahlreferenzen und werden nicht automatisch heruntergeladen oder in das Projekt kopiert.

## Fortgeschrittene Optionen

Fortgeschrittene Funktionen bleiben auffindbar, ohne den Hauptweg zu überladen:

- Agenten-Trace unterhalb des Chats
- Quellen und verwendete Unterkunftsfakten im Transparenzbereich
- Host Advisor im Dashboard
- Prioritäten, Filter und Statistiken in sekundären Bereichen

## UI-Mikrocopy

Die Sprache ist freundlich, direkt und transparent. Der Agent behauptet keine Sicherheit, wenn eine Host-Entscheidung nötig ist.

**Beispiel:**

> „Das kann ich nicht automatisch verbindlich zusagen. Ich habe deine Anfrage zur Prüfung an den Gastgeber weitergeleitet.“

## Gestaltungsprüfung

Vor jeder neuen Oberfläche prüfen:

- Ist die nächste sinnvolle Aktion sofort erkennbar?
- Erklärt die Ansicht, was der Agent gerade tut?
- Sind technische Fakten und soziale Kommunikation verständlich getrennt?
- Werden kritische Fälle sichtbar an den Host übergeben?
- Bleiben erweiterte Funktionen verfügbar, ohne den Hauptweg zu stören?
