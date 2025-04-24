python ./translateCharacters.py apply mod_scripts Mod_Scripts
RD "..\Succubus Rhapsodia Mod Translated\Mod\Mod_Scripts" /S /Q
xcopy "..\Succubus Rhapsodia_mod_translated\Mod\Mod_Scripts" "..\Succubus Rhapsodia Mod Translated\Mod\Mod_Scripts" /E /H /I /Y
pause