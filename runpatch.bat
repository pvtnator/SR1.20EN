"..\rpgmt_cli_v4.5\rpgmt.exe" "..\Succubus Rhapsodia ver1.19_mod"
python mapConditionReplace.py
xcopy "..\Succubus Rhapsodia ver1.19_mod_translated\Data" "..\Succubus Rhapsodia Mod Translated\Mod\Mod_Data" /H /C /I /Y
xcopy "..\Succubus Rhapsodia ver1.19_mod_translated\Mod\Mod_Data" "..\Succubus Rhapsodia Mod Translated\Mod\Mod_Data" /H /I /Y