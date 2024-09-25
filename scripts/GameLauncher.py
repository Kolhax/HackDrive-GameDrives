import os
import json
import configparser
import shutil
import tkinter as tk
from tkinter import ttk, messagebox, Canvas, Frame, Scrollbar
from PIL import Image, ImageTk

GAMES_JSON_FILE = 'scripts\\saved_disks.json'

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

def save_game_list_to_json(game_list):
    with open(GAMES_JSON_FILE, 'w') as json_file:
        json.dump(game_list, json_file, indent=4)

def load_game_list_from_json():
    if os.path.exists(GAMES_JSON_FILE):
        with open(GAMES_JSON_FILE, 'r') as json_file:
            return json.load(json_file)
    return {}

def copy_capsule_image(src, dest):
    try:
        shutil.copyfile(src,dest)
    except Exception as e:
        print(f"Failed to copy {src}: {e}")

class GameLauncherApp:
    def __init__(self, root, game_list):
        self.root = root
        self.root.title("HackDrive - Game Launcher FULL")
        self.game_list = game_list
        self.selected_launcher = None
        self.games = []
        self.style = ttk.Style()
        self.root.configure(bg='#2E2E2E')
        self.style.configure('TLabel', background='#2E2E2E', foreground='#FFFFFF')
        self.style.configure('TButton', background='#3E3E3E', foreground='#FFFFFF')
        self.style.configure('TCombobox', background='#3E3E3E', foreground='#FFFFFF')
        self.root.geometry("750x700")

        # Add banner image
        banner_image_path = 'scripts\\banner.png'  # Change this to your actual banner image path
        banner_image = Image.open(banner_image_path)
        banner_image = banner_image.resize((200, 100), Image.LANCZOS) 
        self.banner_photo = ImageTk.PhotoImage(banner_image)
        self.banner_label = tk.Label(root, image=self.banner_photo, bg='#2E2E2E')
        self.banner_label.pack()

        # Create top frame for comboboxes
        self.top_frame = Frame(root, bg='#2E2E2E')
        self.top_frame.pack(pady=20)

        # Drive selection combobox
        self.drive_combobox = ttk.Combobox(self.top_frame, values=self.get_connected_drives(), state="readonly", font=('Helvetica', 12))
        self.drive_combobox.grid(row=0, column=0, padx=10, pady=10)
        self.drive_combobox.bind("<<ComboboxSelected>>", self.load_launchers)

        # Launcher selection combobox
        self.launcher_combobox = ttk.Combobox(self.top_frame, state="readonly", font=('Helvetica', 12))
        self.launcher_combobox.grid(row=0, column=1, padx=10, pady=10)
        self.launcher_combobox.bind("<<ComboboxSelected>>", self.load_games)

        # Add buttons for starting other scripts
        self.download_button = tk.Button(self.top_frame, text="Download Free Games", command=self.start_download_script, bg='#3E3E3E', fg='#FFFFFF', font=('Helvetica', 8), padx=10, pady=5)
        self.download_button.grid(row=1, column=0, padx=10, pady=10)

        self.find_drive_button = tk.Button(self.top_frame, text="Which Drive Do I Connect for This Game?", command=self.start_find_drive_script, bg='#3E3E3E', fg='#FFFFFF', font=('Helvetica', 8), padx=10, pady=5)
        self.find_drive_button.grid(row=1, column=1, padx=10, pady=10)

        # Create a canvas for the games display and a vertical scrollbar
        self.canvas = Canvas(root, bg='#2E2E2E')
        self.scrollbar = Scrollbar(root, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Configure the canvas to work with the scrollbar
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a frame inside the canvas to hold the game entries
        self.games_frame = Frame(self.canvas, bg='#2E2E2E')
        self.canvas.create_window((0, 0), window=self.games_frame, anchor="nw")

        # Configure the scroll region of the canvas
        self.games_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def start_download_script(self):
        import subprocess
        import sys

        # Determine the appropriate command based on the operating system
        if sys.platform.startswith('win'):
            # On Windows, use 'cmd' with '/c' to execute the command in a new terminal and close it afterwards
            command = ['cmd', '/c', 'py', 'scripts\\GameDownloader.py']
        else:
            # On Linux, using 'gnome-terminal' with the '--' argument to run the Python script
            command = ['gnome-terminal', '--', 'python3', 'scripts\\GameDownloader.py']

        # Start the process in a new terminal window
        print("Executing command:", command)
        subprocess.Popen(command)


    def start_find_drive_script(self):
        import subprocess
        import sys

        # Determine the appropriate command based on the operating system
        if sys.platform.startswith('win'):
            # On Windows, use 'cmd' with '/c' to execute the command and close the terminal afterwards
            command = ['cmd', '/c', 'python', 'scripts\\finder.py']
        else:
            # On Linux, using 'gnome-terminal' with the '--' argument to run the Python script
            command = ['gnome-terminal', '--', 'python3', 'scripts\\finder.py']

        # Start the process in a new terminal window
        print("Executing command:", command)
        subprocess.Popen(command)


    def get_connected_drives(self):
        """Returns a list of connected drives based on scripts\\games_list.json and includes disconnected drives."""
        connected_disks = find_game_disk()
        connected_disk_names = {disk_name: drive_letter for drive_letter, disk_name in connected_disks}
        
        # Load existing game list from JSON
        available_disks = {name: letter for name, letter in self.game_list.items() if name in connected_disk_names}
        
        # Add disconnected drives at the end
        disconnected_disks = [f"{name} (disconnected)" for name in self.game_list.keys() if name not in connected_disk_names]
        
        return list(available_disks.keys()) + disconnected_disks
    
    def load_launchers(self, event):
        selected_drive = self.drive_combobox.get()
        if selected_drive in self.game_list:
            self.launcher_combobox['values'] = list(self.game_list[selected_drive].keys())
            self.launcher_combobox.set('')
    
    def load_games(self, event):
        self.selected_launcher = self.launcher_combobox.get()
        selected_drive = self.drive_combobox.get()
        
        if selected_drive in self.game_list and self.selected_launcher in self.game_list[selected_drive]:
            self.games = self.game_list[selected_drive][self.selected_launcher]
            
            # Clear previous game entries
            for widget in self.games_frame.winfo_children():
                widget.destroy()
            
            row, col = 0, 0
            for game_name, capsule_path, exepath in self.games:
                game_frame = Frame(self.games_frame, bg='#2E2E2E')
                game_frame.grid(row=row, column=col, padx=10, pady=10)

                # Load capsule image
                if capsule_path:
                    try:
                        capsule_image = Image.open(capsule_path)
                        capsule_image = capsule_image.resize((120, 180), Image.LANCZOS)
                        capsule_photo = ImageTk.PhotoImage(capsule_image)
                        capsule_label = tk.Label(game_frame, image=capsule_photo, bg='#2E2E2E')
                        capsule_label.image = capsule_photo  # Keep a reference
                        capsule_label.pack()
                    except Exception as e:
                        capsule_label = ttk.Label(game_frame, text="Image Load Error", font=('Helvetica', 10))
                        capsule_label.pack()
                else:
                    capsule_label = ttk.Label(game_frame, text="No Cover", font=('Helvetica', 10))
                    capsule_label.pack()

                # Play button
                play_button = tk.Button(game_frame, text="Play", command=lambda p=exepath: self.start_game(p),
                                        bg='#3E3E3E', fg='#FFFFFF', font=('Helvetica', 12), padx=10, pady=5)
                play_button.pack(pady=5)

                col += 1
                if col >= 5:  # Adjust the number of columns as needed
                    col = 0
                    row += 1
                             
    def start_game(self, exepath_file):
        try:
            with open(exepath_file, 'r') as f:
                executable_relative_path = f.read().strip()
            base_path = os.path.dirname(exepath_file)
            full_executable_path = os.path.join(base_path, 'Game', executable_relative_path)
            if os.path.exists(full_executable_path):
                os.startfile(full_executable_path)
            else:
                raise FileNotFoundError(f"Executable not found: {full_executable_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def update_game_list_with_new_disks(game_list):
    disks = find_game_disk()
    
    # Create a set of found disk names for easy checking
    found_disk_names = {disk_name for _, disk_name in disks}
    
    for drive_letter, disk_name in disks:
        if disk_name not in game_list:
            game_list[disk_name] = {}
        launchers = game_list[disk_name]
        excluded_dirs = ["$RECYCLE.BIN", "System Volume Information", "_MODS INSTALLATION RESERVED FOLDER"]
        
        for item in os.listdir(drive_letter):
            if os.path.isdir(os.path.join(drive_letter, item)) and item not in excluded_dirs:
                games = []
                launcher_path = os.path.join(drive_letter, item)
                
                for root, dirs, files in os.walk(launcher_path):
                    if 'exepath.txt' in files:
                        game_name = os.path.basename(root)
                        exepath_file = os.path.join(root, 'exepath.txt')
                        
                        try:
                            with open(exepath_file, 'r') as f:
                                executable_relative_path = f.read().strip()
                                
                            capsule_path = os.path.join(root, 'Capsule.jpg')
                            
                            if os.path.exists(capsule_path):
                                dest_capsule_name = f"{disk_name}_{item}_{game_name}.jpg"
                                dest_capsule_path = os.path.join("scripts\\capsule_copies", dest_capsule_name)
                                os.makedirs(os.path.dirname(dest_capsule_path), exist_ok=True)
                                copy_capsule_image(capsule_path, dest_capsule_path)
                                
                            games.append((game_name, capsule_path if os.path.exists(capsule_path) else None, executable_relative_path))
                        
                        except Exception as e:
                            print(f"Error processing game '{game_name}': {e}")
                
                launchers[item] = games
    
    # Mark disks as disconnected if they are not found in current disks
    for disk_name in list(game_list.keys()):
        if disk_name not in found_disk_names:
            game_list[disk_name] = {"status": "disconnected"}

def main():
    # Ensure the capsule_copies directory exists
    if not os.path.exists("scripts\\capsule_copies"):
        os.makedirs("scripts\\capsule_copies")

    # Load existing game list or create a new one
    game_list = load_game_list_from_json()

    # Update game list with new disks
    update_game_list_with_new_disks(game_list)

    # Save updated game list to JSON
    save_game_list_to_json(game_list)

    # Create the main application window
    root = tk.Tk()
    app = GameLauncherApp(root, game_list)
    print('Started, look your taskbar if you dont see it :D')
    root.mainloop()

if __name__ == "__main__":
    main()
