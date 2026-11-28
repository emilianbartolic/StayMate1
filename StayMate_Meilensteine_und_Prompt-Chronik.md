# StayMate AI – Meilensteine und Prompt-Chronik

Stand: 28. November 2026. Zeitangaben in Europe/Berlin. Dieses Dokument ist für das öffentliche Repository [StayMate1](https://github.com/emilianbartolic/StayMate1) vorbereitet und kann dort als einzelne Markdown-Datei hochgeladen werden.

**Projekt in einem Satz:** StayMate ist eine lokal laufende Demo eines KI-Agenten für Ferienunterkünfte. Er unterstützt die Wohnungssuche, beantwortet objektbezogene Gästefragen und übergibt unklare oder kritische Anliegen an einen Host.

## Überblick: Was wann gemacht wurde

| Datum | Meilenstein | Belegter Stand |
|---|---|---|
| 5.11.2026 | Projektidee und erste Demo | Airbnb-Gästesupport mit technischen und sozialen Antworten, Eskalation an Hosts; erste klickbare Website, Host-Dashboard, Stilkarte und Logo. |
| 12.11.2026 | Mehrere Unterkünfte und Agentenarchitektur | Drei Beispielobjekte mit getrennten Wissensbasen; FastAPI-Hub, SQLite-Memory, Browser und CLI, elf interne Fähigkeiten und Codex als Modelladapter. Im Chat gemeldet: 33/33 Skill-Objekt-Kombinationen und 10/10 Akzeptanzfälle bestanden. |
| 19.11.2026 | Arbeitsversion gesichert | Zwei Git-Commits: „Save StayMate working version“ und „Prepare StayMate for GitHub“. Spätere Änderungen im aktuellen Projektordner sind teilweise noch nicht eingecheckt. |
| bis 25.11.2026 | Wohnungssuche und Objekt-Chat | Geführte Suche, Empfehlung, Auswahl und Chat pro Objekt; 262 fiktive Wohnideen laut aktuellem README. Live-Booking-Suche nur mit Partnerzugang. |
| 25.–26.11.2026 | Prüfung und Korrekturen | Suchergebnisse bei engen Filtern ergänzt, Daten und Bilder geprüft, lokale Sicherheitsgrenzen verschärft. In Stuttgart wurde ein Anzeigeproblem der Startbilder behoben. Öffentlicher Mehrbenutzerbetrieb ist gesperrt. |
| 26.–28.11.2026 | Bild- und Repository-Klärung | Weitere Meldungen über fehlende Bilder in StayMate1/Bodensee-Suchergebnissen und Unterscheidung der zwei GitHub-Repositories. Aus dem auslesbaren Verlauf folgt keine bestätigte abschließende Behebung des StayMate1-Problems. |

Projektbelege: [README von StayMate1](https://github.com/emilianbartolic/StayMate1/blob/main/README.md), [Sicherheitsbericht](https://github.com/emilianbartolic/StayMate1/blob/main/trinity/SECURITY_REVIEW.md) und [Compliance-Status](https://github.com/emilianbartolic/StayMate1/blob/main/trinity/COMPLIANCE.md). Die Datumsangaben der Chat-Ereignisse stammen aus den Codex-Chats „Woche 5“, „Website des Agenten finden“ und „Fiktive Objekte auf echte Bilder prüfen“.

**Einordnung für die Bewertung:** Die dokumentierten Chat-Prüfungen belegen den damaligen lokalen Teststand. Der Professor kann Quellcode und Dokumentation auf GitHub lesen. Die vollständige KI-Funktion läuft nicht allein durch das Öffnen des Repositories im Browser; sie benötigt einen lokalen Backend-Start und eine eigene Codex-Anmeldung. Fiktive Wohnideen sind keine buchbaren Inserate. Das Prompt-Protokoll enthält Nutzeranfragen, keine internen Systemprompts oder Modellaufrufe.

## Prompt-Protokoll

Die folgenden Zeitstempel sind die Startzeiten der jeweiligen Chat-Turns. Wenn mehrere Nachrichten im selben Turn stehen, erhalten sie denselben Zeitstempel. Die Nutzertexte sind bis auf automatisch eingefügten App-Kontext und gekürzte Tracking-Parameter einer externen URL wörtlich wiedergegeben. Eine ältere Passage des Chats „Website des Agenten finden“ überschreitet das Ausleselimit; deshalb ist dieses Protokoll dort nicht vollständig.

### 05.11.26

**10:41:27 · Woche 5**

> Ich brauch verschiedene Ideen für einen Agenten den ich selber bauen soll

**10:42:28 · Woche 5**

> Uni

**10:43:33 · Woche 5**

> Ich möchte einen Agenten welcher für AirBNB geeignet ist und automatisch auf fragen antworten kann

**10:45:35 · Woche 5**

> https://www.airbnb.de/rooms/1491974553796684264 (Such- und Tracking-Parameter für die öffentliche Fassung gekürzt)

**10:48:51 · Woche 5**

> Ja bitte

**10:49:53 · Woche 5**

> arbeite weiter an dem projekt

**10:49:53 · Woche 5**

> wo könnte ich jetzt hier ein sprachmodell einsetzen

**10:54:20 · Woche 5**

> wie machen wir jetzt weiter bro

**10:58:47 · Woche 5**

> wie gut ist meine idee von 1-10 bro

**11:01:55 · Woche 5**

> mit host dashboard

**11:15:30 · Woche 5**

> wie bekomme ich aus dem chatbot ein sprachmodell rein

**11:15:30 · Woche 5**

> es muss ein sprachmodell enthalten sein

**11:18:58 · Woche 5**

> wie genau ist das sprachmodell jetzt enthalten

**11:19:42 · Woche 5**

> aktiviere es

**11:40:17 · Woche 5**

> erkläre mir das sprachmodell in meinem agenten

**11:40:49 · Woche 5**

> aber dann ist es doch ein chatbot

**11:47:38 · Woche 5**

> der agent muss deutlicher erkennbar sein

**11:57:19 · Woche 5**

> es soll einen technischen und sozialen teil geben und der Agent soll beide bereiche abdecken und wir sind nur der auftraggeber

**11:58:11 · Woche 5**

> Richtig

**12:10:03 · Woche 5**

> Hilf mir, aus zwei Website-Vorlagen eine einfache Stilkarte für mein bestehendes Projekt zu formulieren. Ich liefere die Links und Screenshots, die du tatsächlich sehen kannst. Frage fehlende Angaben ab und behaupte keinen Zugriff auf ungesehene Seiten. Zielgruppe: [einsetzen]. Hauptaufgabe: [einsetzen]. Hauptaktion: [einsetzen]. Beschreibe: 1 brauchbares Muster, 1 Sache die ich bewusst NICHT übernehme, Palette mit maximal drei Grundfarben, gut lesbare Systemschrift, Buttonregel, Bildregel. Leitgedanke: Form follows function. Fortgeschrittene Optionen bleiben auffindbar, ohne den Hauptweg zu überladen. Keine fremden Texte, Marken oder Medien ungeprüft kopieren. [https://lovable.dev/templates/websites/services/real-estate-agent-site](https://lovable.dev/templates/websites/services/real-estate-agent-site) , [https://lovable.dev/templates/apps/internal-tools/budget-pulse-budget-vs-actual-dashboard-template](https://lovable.dev/templates/apps/internal-tools/budget-pulse-budget-vs-actual-dashboard-template)

**12:10:56 · Woche 5**

> du hast die fragen schon beantwortet

**12:11:34 · Woche 5**

> erstelle die Stilkarte

**12:14:40 · Woche 5**

> wo sind die bilder und die verschiedenen farben das dies optisch schön aussieht

**12:17:04 · Woche 5**

> Hilf mir, aus zwei Website-Vorlagen eine einfache Stilkarte für mein bestehendes Projekt zu formulieren. Ich liefere die Links und Screenshots, die du tatsächlich sehen kannst. Frage fehlende Angaben ab und behaupte keinen Zugriff auf ungesehene Seiten. Zielgruppe: [einsetzen]. Hauptaufgabe: [einsetzen]. Hauptaktion: [einsetzen]. Beschreibe: 1 brauchbares Muster, 1 Sache die ich bewusst NICHT übernehme, Palette mit maximal drei Grundfarben, gut lesbare Systemschrift, Buttonregel, Bildregel. Leitgedanke: Form follows function. Fortgeschrittene Optionen bleiben auffindbar, ohne den Hauptweg zu überladen. Keine fremden Texte, Marken oder Medien ungeprüft kopieren. [https\://lovable.dev/templates/websites/services/real-estate-agent-site]\(https\://lovable.dev/templates/websites/services/real-estate-agent-site) , [https\://lovable.dev/templates/apps/internal-tools/budget-pulse-budget-vs-actual-dashboard-template]\(https\://lovable.dev/templates/apps/internal-tools/budget-pulse-budget-vs-actual-dashboard-template)

**12:17:48 · Woche 5**

> gib mir die stilkarte und suche passende bilder und alles

**12:22:36 · Woche 5**

> mache mir das vorgegebene design als bild

**12:24:52 · Woche 5**

> und genau soll als website welche anklickbar ist

**12:33:09 · Woche 5**

> Erstelle ein passendes logo dafür

### 12.11.26

**09:56:38 · Woche 5**

> mache es so das es nicht auf ein objekt abhängig ist

**10:03:11 · Woche 5**

> generiere die fehlende wissensbasis für mögliche fragen

**10:06:57 · Woche 5**

> gib mir die fertige app

**10:08:27 · Woche 5**

> hier ist jetzt nur ein objekt enthalten

**10:10:49 · Woche 5**

> die wissensbasis für die anderen objekte fehlt

**10:13:54 · Woche 5**

> wo ist die fertige app

**10:15:20 · Woche 5**

> der browsewr link hat wieder nur eine möglichkeit ich will alle mit der jeweils eigenen wissensbasis

**10:17:55 · Woche 5**

> [https://github.com/ProfEngel/KI-Literacy/blob/main/docs/TrinityAgenten_Leitfaden_LLM.md](https://github.com/ProfEngel/KI-Literacy/blob/main/docs/TrinityAgenten_Leitfaden_LLM.md) hier ist die aufgabe enthalten schaue ob alle punkte beinhaltet sind

**10:19:44 · Woche 5**

> alle punkte müssen enthalten sein

**10:25:05 · Woche 5**

> gib mir hier das fertige projekt

**10:26:22 · Woche 5**

> gib mir hier die vollständige ansicht welche alle punkte enthält

**10:28:13 · Woche 5**

> hier ist jetzt nur ein objekt enthalten

**10:30:18 · Woche 5**

> gkib mir hhier wieder die webansicht

**10:31:37 · Woche 5**

> sind jetzt alle anforderungen enthalten

**10:32:20 · Woche 5**

> es müssen alle anforderungen enthalten sein

**10:35:13 · Woche 5**

> der agent soll codex verwenden

**10:38:48 · Woche 5**

> codex muss verwendet werden so dass das meschliche von LLM übernommen wird

**10:45:09 · Woche 5**

> es sollen noch mehr skills enthalten sein welches das LLM Modell kann

**10:49:01 · Woche 5**

> gib mir hier die oberfläche um diese skills zu testen

**10:51:15 · Woche 5**

> ich möchte die oberfläche wie sie davor auch war

**10:51:57 · Woche 5**

> sind die skills in dieser oberfläche jetzt auch enthalten

**10:55:43 · Woche 5**

> die skills sollen in der weboberfläche enthalten sein und dabei soll das LLM Modell automatisch laufen und codex verwenden

**11:00:23 · Woche 5**

> Es sollen für alle objekte alle fragen beantwortet können und die skills sollen bei jedem Objekt verfügbar sein und es sollen alle skills funktionieren

**11:05:15 · Woche 5**

> In der Webansicht sollen alle Skills: Anliegen erkennen &#x20;
> 
> 1. Objektwissen abrufen &#x20;
> 2. Empathisch antworten &#x20;
> 3. Konflikte deeskalieren &#x20;
> 4. Mehrsprachig kommunizieren &#x20;
> 5. Gezielte Rückfragen stellen &#x20;
> 6. Technische Ersthilfe leisten &#x20;
> 7. Dringlichkeit bewerten &#x20;
> 8. An den Host übergeben &#x20;
> 9. Wissensbasis verbessern &#x20;
> 10. Gespräche zusammenfassen    enthalten sein und das LLM Modell soll automatisch funktionieren und die skills anwenden.

**11:15:01 · Woche 5**

> Die skills sollen nicht sichtbar sein sondern im hintergrund laufen. Hier fehlt das LLM Model welches die skills besitzt. Dieses Model soll mit codex arbeiten. Ich weiße nochmals ausdrücklich darauf hin das die Skills des LLM Modells für jedes der Objekte funktioniert. Prüfe jeden einzelnen Skill für jedes einzelne Objekt und achte darauf das diese funktionieren. Zum Beispiel soll in der Sprache in welcher der Gast fragt auch geantwortet werden. Das LLM Model soll den menschlichen Part mit Hilfe von Codex übernehmen.

**11:44:37 · Woche 5**

> gib mir mögliche fragen um die skills zu testen

**12:40:56 · Woche 5**

> gib mier hier nochmal die website

**12:41:18 · Woche 5**

> die website ist nicht erreichbar

### 25.11.26

**21:37:42 · Website des Agenten finden**

> Okay, sehr gut. Sind jetzt auch alle Objekte, wenn man danach weitergeht, wenn man sich für ein Objekt entschieden hat, kann man ja dann noch mal individuell befragen. Also wenn man das gebucht hat, individuell befragen in dem anderen Agenten stellen. Sind da auch alle Objekte enthalten und funktioniert es, dass man dann in den anderen Agenten wechseln kann?

**21:41:28 · Website des Agenten finden**

> Wenn bei den fiktiven Objekten Fragen gestellt werden, antwortet Codex dann auch auf diese Fragen und sind auch Check-in-Zeiten und Parkplätze und das Ganze hinterlegt, die halt Fragen, wie auch bei den anderen Objekten hinterlegt sind, dass die auch bei den fiktiven Objekten beantwortet werden können.

**21:48:48 · Website des Agenten finden**

> Codex soll immer antworten

**21:54:34 · Website des Agenten finden**

> gib mir jetzt hier die fertige seite

**22:00:32 · Website des Agenten finden**

> warum werden keine objekte am ende angezeigt

**22:10:36 · Website des Agenten finden**

> Wenn ich mir hier das Beispiel Bodensee ansehe, Bodensee angucke und alles eingebe, kommt am Ende trotzdem keine Treffer. Also ich brauche für alle Möglichkeiten muss es am Ende mindestens einen Treffer geben oder am besten noch mehrere Treffer, von denen man unterscheiden kann.

**22:20:48 · Website des Agenten finden**

> Also ich muss das ja morgen präsentieren. Dann kann ich ja nicht hier in ChatGPT in den Text reingehen, sondern da brauche ich ja, brauche ich da eine Website oder wie stelle ich das morgen dann am besten vor?

**22:28:04 · Website des Agenten finden**

> überprüfe nochmal das auch alles funktioniert und überall bilder und daten hinterlegt sind

**23:05:59 · Website des Agenten finden**

> führe bitte alle sicherheitschecks durch

**23:05:59 · Website des Agenten finden**

> Du bist ein Sicherheitsprüfer für KI-Agenten. Prüfe den nachfolgenden KI-Agenten anhand der drei Risikosäulen (private Daten, fremde Inhalte, Weg nach außen) sowie der OWASP Top 10 für Agenten (ASI01–ASI10) [0.6.2].\
> \
> Analysiere:\
> 1\. \*\*Datenflüsse & Angriffsflächen:\*\* Welche privaten Daten liest der Agent? Welche fremden/unvertrauenswürdigen Inhalte (E-Mails, Anhänge, Formulare, Webseiten, geteilte Dokumente, Kalender, andere Agenten) verarbeitet er? Welche Aktionen nach außen (Senden, API-Aufrufe, Links, Codeausführung, Datei-Export) sind möglich [0.6.2]?\
> 2\. \*\*Prompt Injection & Zielübernahme (ASI01):\*\* Wo können versteckte Anweisungen in gelesenen Daten das Ziel des Agenten überschreiben [0.6.1, 0.6.2]? Reicht eine reine Eingabefilterung nicht aus [0.6.1]?\
> 3\. \*\*Rechte, Werkzeuge & Identität (ASI02, ASI03, ASI09):\*\* Sind Lese- und Schreibrechte strikt getrennt [0.6.2]? Läuft der Agent mit minimalen Rechten (Least Privilege) statt Sammelkonten [0.6.2, 0.6.5]? Verlangen kritische/externe Aktionen klare menschliche Freigaben mit sichtbarem Empfänger und Inhalt [0.6.2, 0.6.5]?\
> 4\. \*\*Lieferkette, Code, Gedächtnis & Eskalation (ASI04–ASI08, ASI10):\*\* Sind MCP-Server, Plugins und Modelle abgesichert [0.6.2]? Läuft Code isoliert in einer Sandbox [0.6.1, 0.6.2]? Wie werden Gedächtnis/Kontext (z. B. RAG) und Endlosschleifen/Kosten begrenzt [0.6.2, 0.6.5, 0.6.8]? Gibt es Audit-Logs und einen Not-Aus [0.6.2]?\
> \
> Gib am Ende eine priorisierte Befundliste aus mit:\
> \- Risiko / betroffener Bereich\
> \- Konkretes Angriffsszenario\
> \- Dringlichkeit (Hoch / Mittel / Niedrig) & Aufwand\
> \- Konkrete Schutzmaßnahme (Architektur, Rechte, Freigabe oder Prompt/Guardrail)\
> \
> Hier sind die Details zum Agenten:\
> [SYSTEM-PROMPT, WERKZEUGE/TOOLS, ANGEBUNDENE DATENQUELLEN UND ABLAUF EINFÜGEN]\

**23:45:45 · Website des Agenten finden**

> behebe alle fehler

### 26.11.26

**00:46:39 · Website des Agenten finden**

> Wo sind jetzt die ganzen Bilder bei den fiktiven Wohnungen? Also die waren ja davor hinterlegt, aber jetzt gerade, wo ich bei Stuttgart getestet habe, gibt es keine Bilder. Also kein Startbild, dass ich die Wohnung sehen kann, das Apartment, das Objekt von diesen ganzen möglichen fiktiven Wohnungen.

**01:03:32 · Website des Agenten finden**

> ich möchte keine illustrationen sondern wie davor bilder

**01:03:32 · Website des Agenten finden**

> du musst doch keine bilder generieren sondern kannst die bereits generierten aus dem chat nehmen

**01:19:52 · Website des Agenten finden**

> haben jetzt alle objekte ein echtes bild?

**01:20:07 · Website des Agenten finden**

> was bedeutet das?

**08:32:04 · Fiktive Objekte auf echte Bilder prüfen**

> Ich habe die Staymate Seite jetzt über das Repository Staymate geöffnet und geguckt und dabei waren bei den fiktiven Objekten waren immer noch die Bilder nicht drin.

**08:32:04 · Fiktive Objekte auf echte Bilder prüfen**

> Ich habe die Seite auch aus dem, also ich möchte auch, dass es im Repository Staymate 1 ist und daraus habe ich es auch genommen und es war im Staymate 1 und hat nicht funktioniert. Also bitte lass das andere Staymate Repository in Ruhe. Es geht nur um das Staymate 1 Repository.

**08:32:04 · Fiktive Objekte auf echte Bilder prüfen**

> Antwort auf Rückfrage „Über welche genaue URL oder App hast du StayMate1 geöffnet? Bitte schick mir den Link zur Seite, auf der die Bilder fehlen.“: [http://127.0.0.1:8000](http://127.0.0.1:8000)

**08:32:04 · Fiktive Objekte auf echte Bilder prüfen**

> Antwort auf Rückfrage „Bei welchem fiktiven Objekt fehlen die Bilder in deiner Ansicht? Ein Objektname oder Screenshot reicht.“: bodensee

**08:32:04 · Fiktive Objekte auf echte Bilder prüfen**

> Antwort auf Rückfrage „Meinst du die Bildkacheln in den Bodensee-Suchergebnissen oder das Bild im Objekt-Chat „Haus am See“?“: Suchergebnisse

### 28.11.26

**12:11:50 · Fiktive Objekte auf echte Bilder prüfen**

> Ich habe ja verschiedene Repositories auf GitHub hochgeladen. Unter anderem habe ich das richtige Staymate 1 und dann habe ich noch ein anderes, auch mit Staymate. Wie kann ich das andere runternehmen?

