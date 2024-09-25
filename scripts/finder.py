import os
import tkinter as tk
from tkinter import ttk, Canvas, Frame, Scrollbar, messagebox
from PIL import Image, ImageTk

# Directory containing capsule images
CAPSULE_COPIES_DIR = 'scripts\\capsule_copies'

class CapsuleSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HackDrive - Game Disk Finder")
        self.style = ttk.Style()
        self.root.configure(bg='#2E2E2E')
        self.style.configure('TLabel', background='#2E2E2E', foreground='#FFFFFF')
        self.root.geometry("750x700")

        # Add banner image
        banner_image_path = 'scripts\\banner.png'  # Change this to your actual banner image path
        banner_image = Image.open(banner_image_path)
        banner_image = banner_image.resize((200, 100), Image.LANCZOS)  # Adjust size if needed
        self.banner_photo = ImageTk.PhotoImage(banner_image)
        self.banner_label = tk.Label(root, image=self.banner_photo, bg='#2E2E2E')
        self.banner_label.pack()

        # Search entry
        self.search_entry = ttk.Entry(root, font=('Helvetica', 14))
        self.search_entry.pack(pady=20)
        self.search_entry.bind('<KeyRelease>', self.search_capsules)  # Bind KeyRelease for active search

        # Canvas for capsule display
        self.canvas = Canvas(root, bg='#2E2E2E')
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar = Scrollbar(root, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.capsule_frame = Frame(self.canvas, bg='#2E2E2E')
        self.canvas.create_window((0, 0), window=self.capsule_frame, anchor="nw")

        # Load capsule images into a dictionary
        self.image_dict = self.load_capsule_images()

        # Display all images at startup
        self.display_all_capsules()

    def load_capsule_images(self):
        image_dict = {}
        # Iterate through files in the capsule_copies directory
        for filename in os.listdir(CAPSULE_COPIES_DIR):
            if filename.endswith('.jpg') or filename.endswith('.png'):  # Check for image file types
                # Normalize game name by removing extension and replacing underscores with spaces
                game_name = filename[:-4].replace('_', ' ')  # Remove file extension
                image_path = os.path.join(CAPSULE_COPIES_DIR, filename)
                
                # Load image and resize
                try:
                    capsule_image = Image.open(image_path)
                    capsule_image = capsule_image.resize((120, 180), Image.LANCZOS)
                    image_dict[game_name] = (ImageTk.PhotoImage(capsule_image), filename)  # Store image and original filename
                except Exception as e:
                    print(f"Error loading image {image_path}: {e}")
        return image_dict

    def display_all_capsules(self):
        """Display all capsule images at startup."""
        row = 0
        for game_name, (capsule_photo, filename) in self.image_dict.items():
            self.add_capsule_to_display(game_name, capsule_photo, filename, row)
            row += 1

    def search_capsules(self, event):
        search_term = self.search_entry.get().strip().lower()
        
        # Clear previous capsule entries
        for widget in self.capsule_frame.winfo_children():
            widget.destroy()
        
        row = 0
        for game_name, (capsule_photo, filename) in self.image_dict.items():
            if search_term in game_name.lower():  # Match game name
                self.add_capsule_to_display(game_name, capsule_photo, filename, row)
                row += 1

    def add_capsule_to_display(self, game_name, capsule_photo, filename, row):
        """Helper function to add a capsule to the display."""
        # Create a frame for each game
        game_frame = Frame(self.capsule_frame, bg='#2E2E2E')
        game_frame.grid(row=row, column=0, padx=10, pady=10)

        # Display capsule image and bind click event
        capsule_label = tk.Label(game_frame, image=capsule_photo, bg='#2E2E2E')
        capsule_label.image = capsule_photo  # Keep a reference
        capsule_label.pack()
        capsule_label.bind('<Button-1>', lambda e: self.show_game_location(game_name, filename))  # Bind click event

        # Game name label
        game_name_label = ttk.Label(game_frame, text=game_name, font=('Helvetica', 10))
        game_name_label.pack()

    def show_game_location(self, game_name, filename):
        """Show a pop-up with the game location."""
        # Extract drive name and create the message
        drive_name, game_name = game_name.split(' ', 1)  # Replace with actual logic to determine the drive name if needed
        message = f"{game_name} is saved on the disk named \"{drive_name}\"."
        messagebox.showinfo("Game Location", message)

if __name__ == "__main__":
    root = tk.Tk()
    app = CapsuleSearchApp(root)
    root.mainloop()
