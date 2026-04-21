"""
LUGOWARE 프로세스 프리셋 일괄 수정 스크립트
- flush_into_infill, flush_into_support, ensure_vertical_shell_thickness,
  precise_z_height, filter_out_gap_fill → 제거
- support_base_pattern → "default"
- outer_wall_acceleration → "6000"
- initial_layer_acceleration → "2000"
- initial_layer_travel_acceleration → "6000"
- line_width → "105%"
- inner_wall_line_width → "110%"
- detect_thin_wall → "0"

3곳 동기화: resources/, build/OrcaSlicer/resources/, %APPDATA%/system/
"""
import json
import os
import sys
import shutil

REMOVE_KEYS = [
    "flush_into_infill",
    "flush_into_support",
]

SET_VALUES = {
    "support_base_pattern": "default",
    "outer_wall_acceleration": "6000",
    "initial_layer_acceleration": "2000",
    "initial_layer_travel_acceleration": "6000",
    "line_width": "105%",
    "inner_wall_line_width": "110%",
    "detect_thin_wall": "0",
    "precise_outer_wall": "0",
    "ensure_vertical_shell_thickness": "none",
    "precise_z_height": "0",
    "filter_out_gap_fill": "0",
}

ROOT = r"D:\Claude\Slicer\OrcaSlicer-for-LUGOWARE"
LOCATIONS = [
    os.path.join(ROOT, "resources", "profiles", "LUGOWARE", "process"),
    os.path.join(ROOT, "build", "OrcaSlicer", "resources", "profiles", "LUGOWARE", "process"),
    os.path.join(os.environ.get("APPDATA", ""), "LugowareOrcaSlicer", "system", "LUGOWARE", "process"),
]

def modify_file(path):
    if not path.endswith(".json"):
        return False
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"  SKIP (parse err): {path}: {e}")
        return False

    changed = False
    for k in REMOVE_KEYS:
        if k in data:
            del data[k]
            changed = True
    for k, v in SET_VALUES.items():
        if data.get(k) != v:
            data[k] = v
            changed = True

    if changed:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    return changed

def main():
    total_files = 0
    total_changed = 0
    for loc in LOCATIONS:
        if not os.path.isdir(loc):
            print(f"[SKIP] {loc} (not exist)")
            continue
        print(f"[DIR] {loc}")
        for name in sorted(os.listdir(loc)):
            if not name.endswith(".json"):
                continue
            p = os.path.join(loc, name)
            total_files += 1
            if modify_file(p):
                total_changed += 1
                print(f"  OK   {name}")
            else:
                print(f"  --   {name} (no change)")
    print()
    print(f"Total files: {total_files}, changed: {total_changed}")

if __name__ == "__main__":
    main()
