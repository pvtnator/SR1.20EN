# Succubus Rhapsodia translation project.
Largely manually translated line by line, albeit with the assistance of various MTL tools and consulting the Japanese modding community to support my basic level Japanese.
If you encounter issues, please read below so you understand what are relevant bugs to report.
In general, please report game logic bugs (from a save started with the translation applied).
If you want translations to be improved, look at the help section below.

### Original work by Dreamania. The official game is required to apply this patch.

## Progress
Basically, the game is fully translated. The only major part that would still require work is editing the combat dialog of regular enemies. 
It's based on GoogleTranslate with some automated fixes applied on top. The most common lines that showed up while testing have been edited, but a lot remains unedited.
This is currently being worked on and should be done soon.
Boss dialog is manually checked and edited.

## Installation Instructions
You can find the latest release version from the releases page (usually on the right side).  
The releases are provided as .atc files **or .zip files that include built-in AttachéCase4 decryption**, which should be easier for most.  

But if you get the .atc, [AttachéCase4](https://hibara.org/software/attachecase/) is required to decrypt it.
Make sure to turn on [drag and drop password](https://hibara.org/sof*ware/attachecase/help/settings/#settings-password-file),  
then drag and drop the .atc file to AttachéCase4 window and drag and drop the icon.ico from the game folder to the password field.  
This is to avoid providing game data files directly, and to be consistent with the rest of the game's modding scene.  
Alternatively, you can just setup the patching according to instructions below.  

## Patching Instructions
If you wish to do the patching yourself, follow these instructions.
If you just want to play, you're likely better off downloading the release version according to the instructions above.
This project uses RPGMaker Trans https://rpgmakertrans.bitbucket.io/index.html
In addition, some python scripts. Make sure to have up to date Python installed (3.5+ is fine I think)

1. Have unmodified 1.20 version of the game (game logic mods are ok, like changing FPS etc.)
2. With RPGMaker Trans, choose the .exe of the game, and have this repository in a folder next to the game, with "_patch" appended to the folder name
   (e.g. Succubus Rhapsodia 1.20 is the game folder, Succubus Rhapsodia 1.20_patch contains this repository)
   This should generate a folder with "_translated" appended to its name, containing the translated game.
3. Run the "runpatches.bat", which will execute "mapConditionReplace.py", and "runtalk.bat", which executes "translateCharacters.py"
   with python. If your python goes by "python3", try editing the .bat. You can also run those scripts directly yourself.
4. After updates, apply the patches in the same order. No need to delete the game or anything, normally at least.

Explanation: "mapConditionReplace.py" is replacing some inline strings in maps where it checks
if you have certain characters in your party to match the translation. The modified maps will be in the Mods folder of the translated game
"translateCharacters.py" is applying translations to the character specific .rb files in the talk folder and 
putting the modified files into the mod folder of the translated game.
This includes translating some common terms that are used for control logic (these must match the rest of the game)
This also includes character specific dialog. These translations are defined in the characters.txt file.

Note that as things are, this won't modify your saves, and your saves contain some strings, which would lead to discrepency and then bugs.
In other words, it's best to start a new save after applying this mod, although it may work to certain extent, or you could manually modify your saves to match.
Note also that when you load a save, the current map is loaded from the save and changes won't be applied until you re-enter that map.

## Help
While the base game is now almost fully manually translated, feel free to suggest/pull request improvements. There is likely some amount of nuance that I may have not translated as well as it could and there is always a good chance of mistakes here and there. The pronouns system also felt really difficult to translate so I'm open to ideas for that.
However, if you wish to start translating, make sure you understand what the correct formatting is, 
and if the translated strings are used elsewhere, especially for control logic, make sure it's consistent.
You must also take care with text wrapping. It's easy to make it overflow.
Note that #{myname} is not used, since in English there isn't much else to say than "I".
For #{target}, it will either have the character's name or some kind of nickname, 
but in Japanese, a lot of the time it's "you", so sentence structure needs to be edited in that regard.
If you want to use the autotranslate feature, you must install the python module pyperclip
by running "pip install pyperclip" in powershell
