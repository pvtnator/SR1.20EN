# Succubus Rhapsodia translation project.
Mostly edited MTL using a combination of many tools and some basic understanding of Japanese.
If you encounter issues, please read below so you understand what are relevant bugs to report.
In general, please report game logic bugs (from a fresh save), but it's unnecessary to report untranslated lines.

### Original work by Dreamania. The official game is required to apply this patch.

## Progress
### What's done
- Main story (NPC texts in maps)
- UI elements (Skills, items, menus, systems, enemies)
- Most combat text (descriptions of skills and events in battle)
- Some character specific combat dialog

### Work in progress
- Character specific combat/map dialog (the .rb files in the talk folder)
- Translating rarer UI elements and combat text
- Succubus pronoun system
- Making texts that are generated from multiple parts more fluent
- Testing (there might still be bugs; inconsistent translations tend to cause bugs in how the game operates)
- Ensure main story is translated correctly (some parts have been difficult to translate, fluent Japanese speaker could help)
- Modify save files to match translations

### Future
Once the base game seems well enough, I will try to make a branch for the MOD.
If it is as I hope, most translations should carry over through RPGMaker Trans.
At that point, the priority would be UI, then story, and for the immense amount of
character specific text, probably devise a method to auto machine translate them...

## Instructions
This project uses RPGMaker Trans https://rpgmakertrans.bitbucket.io/index.html
In addition, some python scripts. Make sure to have up to date Python installed (3.5+ is fine I think)

1. Have unmodified 1.20 version of the game (game logic mods are ok, like changing FPS etc.)
2. With RPGMaker Trans, choose the .exe of the game, and have this repository in a folder next to the game, with "_patch" appended to the folder name
   (e.g. Succubus Rhapsodia 1.20 is the game folder, Succubus Rhapsodia 1.20_patch contains this repository)
   This should generate a folder with "_translated" appended to its name, containing the translated game.
3. Run the python script "mapConditionReplace.py". It should print several character names. This is replacing some inline strings in maps where it checks
   if you have certain characters in your party to match the translation. The modified maps will be in the Mods folder of the translated game
4. Run the python script "translateCharacters.py". It should print some common terms and their translations. This is applying translations to the
   character specific .rb files in the talk folder and putting the modified files into the mod folder of the translated game.
   This includes translating some common terms that are used for control logic (these must match the rest of the game)
   This also includes character specific dialog. These translations are defined in the characters.txt file.
5. After updates, if anything in the patch folder was changed, RPGMaker Trans must be run. If maps that contain checks of character names were changed,
   mapConditionReplace.py must be run again. If characters.txt was modified, translateCharacters.py must be run again.

Note that as things are, this won't modify your saves, and your saves contain some strings, which would lead to discrepency and then bugs.
In other words, it's best to start a new save after applying this mod, although it may work to certain extent, or you could manually modify your saves to match.
Note also that when you load a save, the current map is loaded from the save and changes won't be applied until you re-enter that map.

## Help
If you want to help, consider the points under "Work in progress". However, if you wish to start translating, make sure you understand
what the correct formatting is, and if the translated strings are used elsewhere, especially for control logic, make sure it's consistent.
For combat text, various formatting of text exists. The locations of whitespaces may vary depending on needs, and it might be inconsistent without a good reason too.
In any case, this area is tricky, so take care.
You must also take care with text wrapping. It's easy to make it overflow. Though perhaps automatic adjusting of font or extending text boxes could be applied later.
The easiest thing for anyone to start working on is the characters.txt. Maybe pick a character you like and translate all the lines! 
Note that I'm not sure yet how to handle the pronouns/name system yet. In many cases, it may be best not to use the myname and target variables.
