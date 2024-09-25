import os
import shutil
import zipfile
import rarfile
import tempfile
from tqdm import tqdm
import configparser

def find_game_disk():
    disks = []
    for drive in range(ord('D'), ord('Z') + 1):
        drive_letter = f"{chr(drive)}:\\"
        if os.path.exists(drive_letter) and os.path.isfile(os.path.join(drive_letter, "GameDisk.ini")):
            config = configparser.ConfigParser()
            config.read(os.path.join(drive_letter, "GameDisk.ini"))
            if config.has_section('DiskInfo') and config.has_option('DiskInfo', 'DiskName'):
                disk_name = config.get('DiskInfo', 'DiskName')
                disks.append((drive_letter, disk_name))
    return disks

def extract_with_progress(archive, path):
    if isinstance(archive, zipfile.ZipFile):
        members = archive.namelist()
    elif isinstance(archive, rarfile.RarFile):
        members = archive.namelist()
    else:
        raise ValueError("Unsupported archive type")
    
    for member in tqdm(members, desc="Extracting"):
        archive.extract(member, path)

def extract_and_organize(archive_path, target_dir=None):
    archive_path = archive_path.strip('"')
    
    if not os.path.exists(archive_path):
        print(f"The specified file does not exist: {archive_path}")
        return

    tempdown_dir = os.path.join(os.path.dirname(archive_path), "tempdown")
    os.makedirs(tempdown_dir, exist_ok=True)

    try:
        if archive_path.lower().endswith('.zip'):
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                extract_with_progress(zip_ref, tempdown_dir)
        elif archive_path.lower().endswith('.rar'):
            with rarfile.RarFile(archive_path, 'r') as rar_ref:
                extract_with_progress(rar_ref, tempdown_dir)
        else:
            print("Unsupported archive format. Please use ZIP or RAR.")
            return
    except Exception as e:
        print(f"Error extracting the archive: {str(e)}")
        return

    contents = os.listdir(tempdown_dir)
    if '_CommonRedist' not in contents or len([f for f in contents if os.path.isdir(os.path.join(tempdown_dir, f)) and f != '_CommonRedist']) != 1:
        print("The archive doesn't have the expected structure.")
        return

    game_folder = next(f for f in contents if os.path.isdir(os.path.join(tempdown_dir, f)) and f != '_CommonRedist')

    for file in os.listdir(tempdown_dir):
        if file.endswith(('.txt', '.url')):
            os.remove(os.path.join(tempdown_dir, file))

    os.rename(os.path.join(tempdown_dir, game_folder), os.path.join(tempdown_dir, "Game"))

    if target_dir is None:
        target_dir = os.path.join(os.path.dirname(archive_path), game_folder)
    
    try:
        shutil.move(tempdown_dir, target_dir)
        print(f"Extraction complete. Game files are in the folder: {target_dir}")
    except Exception as e:
        print(f"Error moving files to target directory: {str(e)}")

def list_exe_files(game_path, exepath_file):
    exe_files = [f for f in os.listdir(game_path) if f.endswith('.exe')]
    with open(exepath_file, 'w') as f:
        for exe in exe_files:
            f.write(exe + '\n')
    return exe_files

if __name__ == "__main__":

    archive_path = input("Please enter the path to your ZIP or RAR file: ")
    
    connected_disks = find_game_disk()
    
    if connected_disks:
        print("Game disk(s) detected:")
        for i, (drive_letter, disk_name) in enumerate(connected_disks, 1):
            print(f"{i}. {disk_name} ({drive_letter})")
        
        choice = input("Do you want to transfer the extracted files to a game drive? (y/n): ").lower()
        
        if choice == 'y':
            if len(connected_disks) == 1:
                selected_drive = connected_disks[0][0]
            else:
                disk_choice = int(input("Enter the number of the disk you want to use: ")) - 1
                selected_drive = connected_disks[disk_choice][0]
            
            subfolder_name = input("Please enter the subfolder name where you want the game saved (e.g., 'Games'): ")

            subfolder_path = os.path.join(selected_drive, subfolder_name)
            if not os.path.exists(subfolder_path):
                os.makedirs(subfolder_path)
            
            game_folder = os.path.splitext(os.path.basename(archive_path))[0]
            target_dir = os.path.join(subfolder_path, game_folder)
            
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            
            print(f"Files will be extracted to: {target_dir}")
            extract_and_organize(archive_path, target_dir)

            capsule_image_path = input("Please enter the path to the Capsule Image (e.g., game thumbnail): ").strip('"')
            if os.path.exists(capsule_image_path):
                shutil.copy(capsule_image_path, os.path.join(target_dir, "Capsule.png"))
                print(f"Capsule Image saved as: {os.path.join(target_dir, 'Capsule.png')}")
            else:
                print("Capsule image not found. Skipping the image step.")

            game_exe_path = os.path.join(target_dir, "Game")
            exepath_file = os.path.join(target_dir, "exepath.txt")
            
            if os.path.exists(game_exe_path):
                exe_files = list_exe_files(game_exe_path, exepath_file)
                if exe_files:
                    print(f"Executable files found and listed in: {exepath_file}")
                    os.startfile(exepath_file)
                    print("Please open 'exepath.txt' and only keep the main executable file required to run the game.")
                else:
                    print("No executable files (.exe) found in the game directory.")
            else:
                print(f"Game directory not found: {game_exe_path}")
            
        else:
            extract_and_organize(archive_path)
    else:
        print("No game disks detected. Extracting to the default location.")
        extract_and_organize(archive_path)
