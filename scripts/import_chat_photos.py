"""Import existing single images and photo grids as local concept covers.

The source directory is supplied at import time. The final JPEGs and manifest
remain in the project, so the running website does not depend on chat files.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "assets/properties/city-photos"
MANIFEST = ROOT / "backend/concept_photo_manifest.json"
PORTFOLIO = ROOT / "backend/city_portfolio.json"

SHEETS = [
    ("exec-73364ec8-52af-44c1-85e2-a6e819091d3e.png", "heritage1"),
    ("exec-1d1e0cf8-4436-4743-92f6-7ca7f6fb282a.png", "family1"),
    ("exec-8350a147-1f9e-496a-94f6-1181c0c8672e.png", "heritage2"),
    ("exec-3fef2d7f-da46-4624-9e23-7b7eb1f86dc9.png", "cityloft1"),
    ("exec-3a017329-44c0-41eb-87ac-adb18a5b4802.png", "nature1"),
    ("exec-14f68d69-9180-4be6-990a-f01cf42295e3.png", "nature2"),
    ("exec-2024754a-f86c-4382-b20c-45607b9901b4.png", "cityloft2"),
    ("exec-80bf9b8c-585b-4388-8d27-5b552567c5a6.png", "compact1"),
    ("exec-569a0334-4384-467b-b64d-dc6c1e91b95b.png", "urban1"),
    ("exec-7ae14354-db0e-433b-b572-b863dcf8da7c.png", "compact2"),
    ("exec-d7b3a723-d98b-4834-b024-477e03a15608.png", "family2"),
    ("exec-1cedd026-09c3-4cd8-9cd4-f2ad9ddcb87e.png", "nature3"),
    ("exec-259953de-c14a-4095-b206-b04fcec26440.png", "heritage3"),
]
SPLITS = [
    ("exec-9624b522-c6a1-47d8-8c68-3617753106da.png", "scenic1"),
    ("exec-133754f2-8b1c-4960-8315-043fa5330428.png", "scenic2"),
]
INDIVIDUALS = [
    ("exec-31db8a39-cb20-4875-bcca-33f244558b9c.png", "stuttgart-loft"),
    ("exec-3fa2c75c-53f8-46f1-91be-4ca2139f8c7a.png", "stuttgart-attic"),
]
PREFERRED = {
    "Altbau": ("heritage", "urban"),
    "Stadtloft": ("cityloft", "urban"),
    "Ruhiges": ("nature", "heritage"),
    "Familienwohnung": ("family", "nature"),
    "Kompaktes": ("compact", "urban"),
    "Dachwohnung": ("urban", "heritage"),
    "Grünes": ("nature", "family"),
    "Arbeitsfreundliches": ("cityloft", "urban"),
}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_dir", type=Path)
    args = parser.parse_args()
    DEST.mkdir(parents=True, exist_ok=True)
    photographs: list[str] = []
    for filename, prefix in SHEETS + SPLITS + INDIVIDUALS:
        source = args.source_dir / filename
        if not source.is_file():
            raise SystemExit(f"Missing existing chat image: {source}")
        if prefix in {"heritage1", "family1", "stuttgart-loft", "stuttgart-attic"}:
            columns, rows = 1, 1
        else:
            columns, rows = (2, 1) if (filename, prefix) in SPLITS else (4, 4)
        with Image.open(source) as original:
            image = original.convert("RGB")
            for row in range(rows):
                for column in range(columns):
                    number = row * columns + column + 1
                    left = round(column * image.width / columns)
                    top = round(row * image.height / rows)
                    right = round((column + 1) * image.width / columns)
                    bottom = round((row + 1) * image.height / rows)
                    destination = DEST / f"{prefix}-{number:02d}.jpg"
                    image.crop((left, top, right, bottom)).save(destination, "JPEG", quality=88)
                    photographs.append(f"assets/properties/city-photos/{destination.name}")

    items = json.loads(PORTFOLIO.read_text(encoding="utf-8"))
    photo_map = {
        "demo-germany-stuttgart": "assets/properties/city-photos/stuttgart-loft-01.jpg",
        "demo-germany-stuttgart-2": "assets/properties/city-photos/heritage2-01.jpg",
        "demo-germany-stuttgart-3": "assets/properties/city-photos/stuttgart-attic-01.jpg",
        "demo-germany-stuttgart-4": "assets/properties/city-photos/heritage3-01.jpg",
    }
    usage = Counter(photo_map.values())
    by_city: dict[str, set[str]] = defaultdict(set)
    for item in items:
        if item["id"].startswith("demo-germany-stuttgart"):
            by_city["Stuttgart"].add(photo_map[item["id"]])
    for item in items:
        if item["id"] in photo_map or item["id"].startswith("demo-germany-berlin"):
            continue
        city = item["location"].split(" · ", 1)[0]
        preferences = next((tags for name, tags in PREFERRED.items() if item["name"].startswith(name)), ())
        choices = [p for p in photographs if p not in by_city[city] and not p.startswith("assets/properties/city-photos/stuttgart-")]
        choices.sort(key=lambda p: (usage[p], not p.rsplit("/", 1)[1].startswith(preferences), p))
        selected = choices[0]
        photo_map[item["id"]] = selected
        usage[selected] += 1
        by_city[city].add(selected)

    for item in items:
        image = photo_map.get(item["id"])
        if image:
            item["image"] = image
            item["image_alt"] = f"Fotorealistisches Beispielbild für die fiktive Wohnidee {item['name']}; kein Foto einer realen Unterkunft"
            item["image_label"] = "KI-Beispielfoto · fiktives Objekt"
        for fact in item.get("facts", []):
            if fact.get("id") == "style":
                for language, answer in fact.get("answers", {}).items():
                    fact["answers"][language] = answer.replace("Die Illustration", "Das Beispielbild").replace("The illustration", "The sample image")
    MANIFEST.write_text(json.dumps(photo_map, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    PORTFOLIO.write_text(json.dumps(items, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(photographs)} vorhandene Fotomotive importiert; {len(photo_map)} fiktive Objekte mit Fotobild verknüpft.")
    print(f"{sum(n > 1 for n in usage.values())} Fotos werden in verschiedenen Orten erneut verwendet; innerhalb eines Ortes keine Dopplung.")


if __name__ == "__main__":
    main()
