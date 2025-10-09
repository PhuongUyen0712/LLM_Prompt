import json
import re
from pathlib import Path

# === Đường dẫn file ===
input_path = Path("barem_results_full.json")
output_path = Path("barem_results_parsed.json")

# === Hàm hỗ trợ ===
def extract_json_objects(text):
    """Tách các block JSON từ text có thể chứa nhiều định dạng."""
    # Xóa các khối ```json ... ``` nếu có
    text = re.sub(r"```json|```", "", text).strip()
    objs = []
    try:
        parsed = json.loads(text)
        if isinstance(parsed, list):
            return parsed
        elif isinstance(parsed, dict):
            return [parsed]
    except:
        pass

    # Nếu là nhiều block JSON trong text
    matches = re.findall(r"\{[\s\S]*?\}", text)
    for m in matches:
        try:
            objs.append(json.loads(m))
        except:
            continue
    return objs


# === Bắt đầu parse ===
print(f"📂 Đang đọc file: {input_path}")
data = json.load(open(input_path, "r", encoding="utf-8"))

parsed_all = []
total = 0
for batch in data:
    raw_output = batch.get("raw_output", "")
    batch_id = batch.get("batch_id", "?")
    objs = extract_json_objects(raw_output)
    print(f"→ Batch {batch_id}: tìm thấy {len(objs)} object JSON")
    for o in objs:
        total += 1
        parsed_all.append(o)

# === Xuất file ===
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(parsed_all, f, indent=2, ensure_ascii=False)

print(f"\n✅ Hoàn tất! Đã parse {total} đối tượng JSON từ {len(data)} batch.")
print(f"📁 File xuất: {output_path.resolve()}")
