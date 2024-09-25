
# Cracked Games Setup Guide

This guide provides instructions for setting up your cracked games folder.

## Instructions

1. **Locate the Cracked Folder**
   - Inside, you'll find a little gift. Review how it's organized.

2. **Capsule Setup**
   - The `Capsule` file displays the game image.

3. **Executable Path**
   - The `exepath.txt` file should contain the name or the path to the game executable (EXE) relative to the game folder.

4. **Organizing Game Files**
   - Create a folder named "Game" and place all game files inside it.

5. **Adding New Games**
   - To add more games, create a new folder on the disk, for example, "Cracked". This will create a new category for your cracked games.
   - Inside this category, create a folder named after the game.

6. **Folder Structure**
   - Within the newly created game folder, create another folder called "Game" and extract or paste your game files there.

7. **Finding the Executable**
   - Locate the game’s executable (EXE) file:
     - If it’s in the main directory, copy the EXE name (e.g., `TheEscapists.exe`).
     - If it’s located in a subdirectory, note the path (e.g., `Data\FortniteGame\Fortnite.exe`).

8. **Creating the exepath.txt File**
   - Create a file named `exepath.txt` and paste the noted path into it. Ensure you only include the path relative to the game folder.

9. **Importing the Capsule**
   - For visuals, consider using images from [SteamGridDB](https://www.steamgriddb.com/).

## Example Structure

```
The Escapists 1
│   Capsule.jpg
│   exepath.txt
│
└───Game
    │   EULA.txt
    │   gog.ico
    │   goggame-1423221839.hashdb
    │   goggame-1423221839.ico
    │   goggame-1423221839.info
    │   goggame-1443778814.hashdb
    │   goggame-1443778814.ico
    │   ...
```

## Additional Notes

- The standalone EXE can be run from anywhere on your disk.
- To change the drive name when you plug in the disk, edit `autorun.inf` and `GameDisk.ini`.
- You can also change the icon if desired.