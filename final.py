# ============================================
# ✅ Stable Multi-Agent Debate Evaluation (Batch Mode)
# ============================================

import json
import math
import time
from tqdm import tqdm
import google.generativeai as genai
import re

# ==============================
# 1️⃣ CONFIGURATION
# ==============================

# API_KEY = "AIzaSyCoVcOf76dOq-oGam5BTUayqXCRSqsgZ-8"  # ⚠️ Replace with your real key

API_KEY="AIzaSyBfNwF7Jsd9ZoaPbuCjg8idxEpPr_8LocQ"
MODEL_NAME = "gemini-2.5-flash-lite"  # or "gemini-1.5-pro", "gemini-1.5-base", etc.

PROMPT_PATH = "barem.txt"
DATASET_PATH = "selected_dialogues.json"

MAX_BATCH_CALLS = 4
MAX_RETRIES = 3
RETRY_DELAY = 10  # seconds

# ==============================
# 2️⃣ INIT MODEL
# ==============================

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

# ==============================
# 3️⃣ LOAD DATA
# ==============================

with open(PROMPT_PATH, "r", encoding="utf-8") as f:
    base_prompt = f.read()

with open(DATASET_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

if isinstance(data, dict) and "dialogues" in data:
    dialogues = data["dialogues"]
else:
    dialogues = data

TOTAL = len(dialogues)
batch_size = math.ceil(TOTAL / MAX_BATCH_CALLS)
print(f"✅ Loaded {TOTAL} dialogues → {MAX_BATCH_CALLS} batches (≈{batch_size}/batch)")

# ==============================
# 4️⃣ HELPERS
# ==============================

def chunk_list(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def build_dialogue_text(turns):
    return "\n".join([f"{t['speaker']}: {t['text'].strip()}" for t in turns])


def build_batch_prompt(batch, base_prompt):
    parts = [base_prompt, "\n\n=== Evaluate the following dialogues ==="]
    for i, item in enumerate(batch, start=1):
        dtext = build_dialogue_text(item["turns"])
        parts.append(f"\n\n--- Dialogue #{i} (ID: {item['dialogue_id']}) ---\n{dtext}")
    parts.append(
        "\n\nReturn ONLY a valid JSON array (no commentary) "
        "with one object per dialogue following this schema:\n"
        "{'dialogue_id': int, 'referee_final': {'OverallExperience': 20|40|60|80|100}, ... }"
    )
    return "\n".join(parts)


def try_parse_json(text):
    """Safely parse JSON array or fallback to single object."""
    text = text.strip()
    if text.startswith("```"):
        text = text.strip("`").strip()
        if text.lower().startswith("json"):
            text = text[4:].strip()
    try:
        return json.loads(text)
    except Exception:
        # find first [ ... ]
        if "[" in text and "]" in text:
            sub = text[text.find("[") : text.rfind("]") + 1]
            try:
                return json.loads(sub)
            except Exception:
                pass
        if "{" in text and "}" in text:
            sub = text[text.find("{") : text.rfind("}") + 1]
            try:
                return json.loads(sub)
            except Exception:
                pass
    return None


def safe_generate(prompt):
    for attempt in range(MAX_RETRIES):
        try:
            resp = model.generate_content(prompt)
            return resp.text.strip()
        except Exception as e:
            print(f"⚠️ Retry {attempt+1}/{MAX_RETRIES} after error: {e}")
            time.sleep(RETRY_DELAY)
    return None


# ==============================
# 5️⃣ MAIN LOOP
# ==============================

results_summary = []
results_full = []

batches = list(chunk_list(dialogues, batch_size))
print(f"🚀 Starting evaluation in {len(batches)} batches...")

for batch_id, batch in enumerate(batches, start=1):
    print(f"\n=== Processing batch {batch_id}/{len(batches)} ({len(batch)} dialogues) ===")
    prompt = build_batch_prompt(batch, base_prompt)

    output_text = safe_generate(prompt)
    if not output_text:
        print(f"❌ Batch {batch_id} failed — no response.")
        continue

    parsed = try_parse_json(output_text)
    if parsed is None:
        print(f"⚠️ Batch {batch_id}: Could not parse JSON. Saving raw output.")
        results_full.append({"batch_id": batch_id, "raw_output": output_text})
        continue

    if isinstance(parsed, dict):
        parsed = [parsed]

    for obj in parsed:
        if not isinstance(obj, dict):
            continue
        did = obj.get("dialogue_id")
        overall = None
        if "referee_final" in obj:
            overall = obj["referee_final"].get("OverallExperience")
        elif "OverallExperience" in obj:
            overall = obj["OverallExperience"]

        avg = next((d["average_score"] for d in batch if d["dialogue_id"] == did), None)
        results_summary.append({
            "dialogue_id": did,
            "average_score": avg,
            "model_score": overall
        })
        results_full.append(obj)

# ==============================
# 6️⃣ SAVE RESULTS
# ==============================

with open("results_summary.json", "w", encoding="utf-8") as f:
    json.dump(results_summary, f, indent=2, ensure_ascii=False)

with open("results_full.json", "w", encoding="utf-8") as f:
    json.dump(results_full, f, indent=2, ensure_ascii=False)

print("\n✅ DONE! Saved results to:")
print(" - results_summary.json")
print(" - results_full.json")
