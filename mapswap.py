import os
import re
import time
import sys
from pathlib import Path

if __name__ == "__main__":
    current_dir = Path.cwd()
    mod_dir = current_dir.parent / Path().resolve().name.replace("_patch","")
    translated_dir = current_dir.parent / Path().resolve().name.replace("patch","translated")
    data_dir = mod_dir / "Data"
    backup_dir = data_dir / "Original"
    map_dir = data_dir / "Map"
    t_data_dir = translated_dir / "Data"
    t_backup_dir = translated_dir / "Data" / "Original"
    t_map_dir = t_data_dir / "Map"
    savefile = "mapswap.txt"

    mode = sys.argv[1] if len(sys.argv)>1 else "swapin"

    index = 1
    MapToTemp = {}
    TempToMap = {}

    with open(savefile, encoding='utf-8') as swap:
        for line in swap:
            parts = line.strip().split(" = ")
            MapToTemp[parts[0]] = parts[1]
            TempToMap[parts[1]] = parts[0]

    if mode == "swapin":
        with open(savefile, "w", -1, 'utf-8') as s:
            for file in map_dir.rglob("*.rxdata"):
                if "Info" in file.as_posix():
                    continue
                relative = file.relative_to(map_dir)
                context = relative.as_posix()
                while str.format("Map{:03}.rxdata", index) in TempToMap:
                    index += 1
                if not context in MapToTemp:
                    MapToTemp[context] = str.format("Map{:03}.rxdata", index)
                    TempToMap[str.format("Map{:03}.rxdata", index)] = context
                    print(context+" = "+MapToTemp[context])
                index += 1
                s.write(context+" = "+MapToTemp[context]+"\n")

        for m in TempToMap.keys():
            backup_dir.mkdir(exist_ok=True)
            (backup_dir / m).write_bytes((data_dir / m).read_bytes())
            t_backup_dir.mkdir(exist_ok=True)
            (t_backup_dir / m).write_bytes((t_data_dir / m).read_bytes())
        print("Backup done")
        for m in MapToTemp.keys():
            (data_dir / MapToTemp[m]).write_bytes((map_dir / m).read_bytes())
        print("Replacement done")
    elif mode == "afterpatch":
        for m in TempToMap.keys():
            (t_map_dir / TempToMap[m]).write_bytes((t_data_dir / m).read_bytes())
        print("Copied to correct directories")
        for m in TempToMap.keys():
            (t_data_dir / m).write_bytes((t_backup_dir / m).read_bytes())
        print("Reverted the swap")
    elif mode == "revert":
        for m in TempToMap.keys():
            (data_dir / m).write_bytes((backup_dir / m).read_bytes())
        print("Reverted the swap")
