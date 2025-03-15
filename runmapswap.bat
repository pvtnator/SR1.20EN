python mapswap.py swapin
"..\rpgmt_cli_v4.5\rpgmt.exe" "..\Succubus Rhapsodia_mod" -p mapswap
python mapConditionReplace.py
xcopy "..\Succubus Rhapsodia_mod_translated\Mod\Mod_Data" "..\Succubus Rhapsodia_mod_translated\Data" /H /I /Y
python mapswap.py afterpatch
python mapswap.py revert
xcopy "..\Succubus Rhapsodia_mod_translated\Data" "..\Succubus Rhapsodia Mod Translated\Mod\Mod_Data" /H /C /I /Y
xcopy "..\Succubus Rhapsodia_mod_translated\Mod\Mod_Data" "..\Succubus Rhapsodia Mod Translated\Mod\Mod_Data" /H /I /Y