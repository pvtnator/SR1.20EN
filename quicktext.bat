set /p id=name: 
python ./translateCharacters.py apply talk Mod_Talk %id%
RD "..\Succubus Rhapsodia Mod Translated\Mod\Mod_Talk" /S /Q
xcopy "..\Succubus Rhapsodia ver1.19_mod_translated\Mod\Mod_Talk" "..\Succubus Rhapsodia Mod Translated\Mod\Mod_Talk" /E /H /I /Y