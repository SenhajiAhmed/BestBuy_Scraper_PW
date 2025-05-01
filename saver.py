import json
from typing import List, Dict

def save_to_json(data: List[Dict], filename: str = "specs.json"):
    formatted_data = []
    for product in data:
        formatted_product = {
            "url": product["url"],
            "specs": []
        }
        for section in product["sections"]:
            formatted_product["specs"].append({
                "section": section["section"],
                "details": section["details"]
            })
        formatted_data.append(formatted_product)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(formatted_data, f, indent=2, ensure_ascii=False)
    print(f"🔳 Saved {len(formatted_data)} product specs to '{filename}'")
