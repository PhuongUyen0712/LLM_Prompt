import json
import re

# =======================
# 1️⃣ Load dataset & output
# =======================
with open("selected_dialogues.json", "r", encoding="utf-8") as f:
    dataset = json.load(f)

# Dữ liệu thật nằm trong key "dialogues"
dialogues = dataset["dialogues"] if isinstance(dataset, dict) else dataset

with open("barem_results_full.json", "r", encoding="utf-8") as f:
    results = json.load(f)

print(f"🧩 Tổng số hội thoại trong dataset: {len(dialogues)}")

# =======================
# 2️⃣ Hàm parse JSON từ raw_output
# =======================
def extract_json_objects(text):
    text = re.sub(r"```json|```", "", text).strip()
    try:
        data = json.loads(text)
        if isinstance(data, list):
            return data
        else:
            return [data]
    except Exception:
        pass

    # Nếu không load được toàn bộ, tách thủ công từng {...}
    objs = []
    matches = re.findall(r"\{[\s\S]*?\}", text)
    for m in matches:
        try:
            objs.append(json.loads(m))
        except:
            continue
    return objs

# =======================
# 3️⃣ Parse toàn bộ batch
# =======================
parsed = []
for batch in results:
    objs = extract_json_objects(batch["raw_output"])
    print(f"→ Batch {batch['batch_id']}: tìm thấy {len(objs)} object JSON")
    parsed.extend(objs)

print(f"\n🧾 Tổng số JSON parse được từ output: {len(parsed)}")

# =======================
# 4️⃣ So khớp thứ tự dialogue_id
# =======================
expected_ids = [d["dialogue_id"] for d in dialogues]

if len(expected_ids) == len(parsed):
    print("✅ Không thiếu hội thoại nào!")
else:
    diff = len(expected_ids) - len(parsed)
    print(f"⚠️ Thiếu {diff} hội thoại!")

    # Vì mỗi batch giữ nguyên thứ tự, nên thiếu cuối cùng
    missing = expected_ids[len(parsed):]
    print("🕳️ Thiếu các dialogue_id sau:", missing)
