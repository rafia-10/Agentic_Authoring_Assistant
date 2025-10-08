from typing import List
import re

def parse_numbered_items(text: str) -> List[str]:
    items = []
    for m in re.finditer(r"^\s*\d+\s*[\.\)\-\:]+\s*(.+)$", text, flags=re.MULTILINE):
        items.append(m.group(1).strip())
    if not items:
        parts = re.split(r"[,;\n]", text)
        items = [p.strip() for p in parts if p.strip()]
    return items

