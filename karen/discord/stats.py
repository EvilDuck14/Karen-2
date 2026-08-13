import json
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_PATH = Path(str(PROJECT_ROOT) + "/data/stats.json")
os.makedirs(DATA_PATH.parent, exist_ok=True)
if not DATA_PATH.exists():
    with DATA_PATH.open("w", encoding="utf-8") as f:
        json.dump({}, f)

stats: dict[str, int]
with DATA_PATH.open("r", encoding="utf-8") as f:
    stats = json.load(f)
    print(type(stats))

async def logEval(comboSequence):
    comboString: str = ""

    for action in comboSequence:
        if action[0] != "[":
            comboString += action

    if not (comboString in stats.keys()):
        stats[comboString] = 0
    stats[comboString] = stats[comboString] + 1

    # write to json
    with DATA_PATH.open("w", encoding="utf-8") as f:
        f.write(json.dumps(stats, indent=4))