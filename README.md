# Succubus Rhapsodia translation project.
Mostly edited MTL using a combination of many tools and some basic understanding of Japanese.
If you encounter issues, please read below so you understand what are relevant bugs to report.
In general, please report game logic bugs (from a fresh save).
If you want translations to be improved, look at the help section below.

### Original work by Dreamania. The official game is required to apply this patch.

## This is the branch for the modded version of the game. Refer to the [mod wiki](https://wikiwiki.jp/scrp/) for more info.

## Progress
### What's done
- Most content up to Silver City
- Settings, common UI elements
- Many of the new combat texts
- Character specific combat dialog (MTL with some of them edited)

### Work in progress
- There's still a lot to do

## Installation Instructions
You can find the latest release version from the releases page (usually on the right side).
The releases are provided as .atc files.
To install, [AttachéCase4](https://hibara.org/software/attachecase/) is required to decrypt it.
Make sure to turn on [drag and drop password](https://hibara.org/software/attachecase/help/settings/#settings-password-file),
then drag and drop the .atc file to AttachéCase4 window and drag and drop the icon.ico from the game folder to the password field.
This is to avoid providing game data files directly, and to be consistent with the rest of the game's modding scene.
Alternatively, you can just setup the patching according to instructions below.

## Patching/editing Instructions
If you wish to do the patching yourself or edit, follow these instructions.
For the modded version, it's a lot more complex...
If you just want to play, you're likely better off downloading the release version according to the instructions above.
This project uses RPGMaker Trans https://rpgmakertrans.bitbucket.io/index.html
In addition, some python scripts. Make sure to have up to date Python installed (3.5+ is fine I think)

1. Have unmodified 1.20 version of the game, and make a copy of it
2. Download the version of the mod described in modnotes.txt
3. For one of the copies, install the mod normally. This will be the final output directory
   for the translated game, so name the folder accordingly (e.g. "Succubus Rhapsodia Mod Translated")
4. For the other copy, otherwise install the mod normally, but put contents of Mod_Data into the Data folder,
   the contents of Mod_Scripts to System/mod_scripts and contents of Mod_Talk to System/talk.
   Name this folder for example "Succubus Rhapsodia ver1.20_mod"
5. This repository should co-exist in the same directory as the game folders,
   called "Succubus Rhapsodia ver1.20_mod_patch" or whatever matches the folder name of the previous step.
6. With RPGMaker Trans, choose the .exe of the game in "Succubus Rhapsodia ver1.20_mod", 
   This should generate a folder with "_translated" appended to its name, containing the translated game.
7. Edit the .bat files in the repository so the folder names match yours.
8. After running RPGMaker Trans, run "rundata.bat". Also run "runscript.bat" and "runtext.bat"
   when first patching or when there are updates to said files.
9. Because there are over 999 maps, RPGMaker Trans can't do them all at once.
   For the rest of the maps, there's another branch for the repository, "mapswap"
   This really isn't convenient but you have to swap to that, run "swap1in.bat",
   then run RPGMaker Trans, then run "swap2afterpatch.bat". This puts the maps from the subfolders
   to the main folder, patches them, then assigns them back into the subfolders.

As patching all the talk files takes a while, "quicktext.bat" allows you to enter a part of the
name of the directory and only patch directories that contain that text.