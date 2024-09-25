import os
import configparser
import tkinter as tk
from tkinter import ttk, messagebox, Canvas, Frame, Scrollbar
from PIL import Image, ImageTk
import sys

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller."""
    try:
        # PyInstaller stores data files in a temporary folder when run
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def find_game_disk():
    game_disk_letter, disk_name = None, None
    
    # Get the drive letter where the script is running
    current_drive = os.path.splitdrive(os.getcwd())[0]
    
    # Construct the path to GameDisk.ini in the current drive
    ini_path = os.path.join(current_drive, "GameDisk.ini")
    
    if os.path.exists(ini_path) and os.path.isfile(ini_path):
        game_disk_letter = current_drive
        config = configparser.ConfigParser()
        config.read(ini_path)
        
        # Correctly access the 'DiskInfo' section and 'DiskName' key
        if config.has_section('DiskInfo') and config.has_option('DiskInfo', 'DiskName'):
            disk_name = config.get('DiskInfo', 'DiskName')
    
    return game_disk_letter, disk_name

class GameLauncherApp:
    def __init__(self, root, drive_letter, disk_name):
        self.root = root
        self.root.title("HackDrive - Game Launcher Portable")
        self.drive_letter = drive_letter
        self.disk_name = disk_name
        self.launchers = self.find_launchers()
        self.selected_launcher = None
        self.games = []

        self.style = ttk.Style()
        self.root.configure(bg='#2E2E2E')  
        self.style.configure('TLabel', background='#2E2E2E', foreground='#FFFFFF')
        self.style.configure('TButton', background='#3E3E3E', foreground='#FFFFFF')
        self.style.configure('TCombobox', background='#3E3E3E', foreground='#FFFFFF')

        self.root.geometry("800x660")

        # Add banner image
        # Add banner image
        banner_image_path = resource_path('banner.png')  # Update with your actual path
        try:
            with open(banner_image_path, 'rb') as file:
                banner_image = Image.open(file)
                banner_image.load()  # Force loading of image
                banner_image = banner_image.resize((200, 100), Image.LANCZOS)  # Adjust size if needed
                self.banner_photo = ImageTk.PhotoImage(banner_image)
        except Exception as e:
            print(f"Error loading banner image: {e}")
            self.banner_photo = None  # Handle case when the image can't be loaded

        self.banner_label = tk.Label(root, image=self.banner_photo, bg='#2E2E2E')
        self.banner_label.pack()

        self.disk_name_label = ttk.Label(root, text=f"Disk Name: {self.disk_name}", font=('Helvetica', 16))
        self.disk_name_label.pack(pady=20)

        self.launcher_label = ttk.Label(root, text="Select Launcher:", font=('Helvetica', 14))
        self.launcher_label.pack(pady=10)

        self.launcher_combobox = ttk.Combobox(root, values=self.launchers, state="readonly", font=('Helvetica', 12))
        self.launcher_combobox.pack(pady=10)
        self.launcher_combobox.bind("<<ComboboxSelected>>", self.load_games)

        # Create a canvas for scrolling
        self.canvas = Canvas(root, bg='#2E2E2E')
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = Scrollbar(root, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Create a frame inside the canvas
        self.games_frame = Frame(self.canvas, bg='#2E2E2E')
        
        # Create a window in the canvas for the frame
        self.canvas.create_window((0, 0), window=self.games_frame, anchor="nw")

        # Bind the frame resize event to update the scrollregion
        self.games_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    def find_launchers(self):
        launchers = []
        excluded_dirs = ["$RECYCLE.BIN", "System Volume Information"]

        for item in os.listdir(self.drive_letter):
            if os.path.isdir(os.path.join(self.drive_letter, item)) and item not in excluded_dirs:
                launchers.append(item)
        return launchers

    def load_games(self, event):
        self.selected_launcher = self.launcher_combobox.get()
        self.games = self.find_games(self.selected_launcher)

        # Clear existing game frames
        for widget in self.games_frame.winfo_children():
            widget.destroy()
        
        row, col = 0, 0
        for game_name, capsule_path, exepath in self.games:
            game_frame = Frame(self.games_frame, bg='#2E2E2E')
            game_frame.grid(row=row, column=col, padx=10, pady=10)
            
            if capsule_path:
                capsule_image = Image.open(capsule_path)
                capsule_image = capsule_image.resize((120, 180), Image.LANCZOS)
                capsule_photo = ImageTk.PhotoImage(capsule_image)
                capsule_label = tk.Label(game_frame, image=capsule_photo, bg='#2E2E2E')
                capsule_label.image = capsule_photo  
                capsule_label.pack()
            else:
                capsule_label = ttk.Label(game_frame, text="No Cover", font=('Helvetica', 10))
                capsule_label.pack()

            play_button = tk.Button(game_frame, text="Play", command=lambda p=exepath: self.start_game(p),
                                    bg='#3E3E3E', fg='#FFFFFF', font=('Helvetica', 12), padx=10, pady=5)
            play_button.pack(pady=5)

            col += 1
            if col == 5:  # Move to the next row after 5 columns
                col = 0
                row += 1

    def find_games(self, launcher):
        games = []
        launcher_path = os.path.join(self.drive_letter, launcher)

        for root, dirs, files in os.walk(launcher_path):
            if 'exepath.txt' in files:
                game_name = os.path.basename(os.path.dirname(root))
                exepath = os.path.join(root, 'exepath.txt')
                capsule_path = os.path.join(root, 'Capsule.jpg')
                games.append((game_name, capsule_path if os.path.exists(capsule_path) else None, exepath))

        return games

    def start_game(self, exepath_file):
        with open(exepath_file, 'r') as f:
            executable_path = f.read().strip()

        full_executable_path = os.path.join(os.path.dirname(exepath_file), 'Game', executable_path)

        if os.path.exists(full_executable_path):
            os.startfile(full_executable_path)
            print(f"[New Task!] -> (StartGame): {executable_path}")
        else:
            messagebox.showerror("Error", f"Executable not found: {full_executable_path}")

def main():
    game_disk_letter, disk_name = find_game_disk()
    
    if not game_disk_letter:
        messagebox.showerror("Error", "Current disk is not Gamedrive or dosent have GameDisk.ini on its root dir!")
        return

    root = tk.Tk()
    app = GameLauncherApp(root, game_disk_letter, disk_name)
    root.mainloop()

if __name__ == "__main__":
    main()
