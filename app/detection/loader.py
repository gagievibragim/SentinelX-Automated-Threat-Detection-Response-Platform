from pathlib import Path
import yaml

def load_rules(path: str) -> list[dict]:
    rules = []
    for file in sorted(Path(path).glob("*.yml")):
        with file.open("r", encoding="utf-8") as fh:
            rules.append(yaml.safe_load(fh))
    return rules
