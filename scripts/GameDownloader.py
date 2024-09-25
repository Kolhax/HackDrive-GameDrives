




import sys
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton,
    QComboBox, QMessageBox, QLabel, QLineEdit,
    QScrollArea, QDialog, QHBoxLayout, QCheckBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

def grab_hyperlinks(url="https://steamrip.com/games-list-page/",appendstart="https://steamrip.com",appendend=""):
    try:
        # Fetch the webpage content
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad responses
    except requests.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return []

    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all hyperlinks
    links = []
    for a in soup.find_all('a', href=True):
        link_info = {
            'text': a.get_text(strip=True),
            'url': appendstart + a['href'] + appendend
        }
        links.append(link_info)

    return links



def save_to_json(data, filename):    
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Function to scrape URLs
def scrape_urls(base_url):
    try:
        response = requests.get(base_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)

        prefixes = [
            'https://megadb.net/',
            'https://buzzheavier.com/',
            'https://1fichier.com/',
            'https://gofile.io/'
        ]

        return [
            urljoin(base_url, link['href'])
            for link in links
            if any(urljoin(base_url, link['href']).startswith(prefix) for prefix in prefixes)
        ]
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return []


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HackDrive - Free Game Downloader")
        self.setGeometry(600, 600, 600, 600)
        self.initUI()
        self.load_gamelist()
        self.waitlist_dialog = None

    def initUI(self):
        layout = QVBoxLayout()
        self.setup_banner(layout)
        self.setup_search_bar(layout)
        self.setup_scroll_area(layout)
        self.setup_buttons(layout)
        self.setStyleSheet("background-color: #222222; color: white;")
        self.setLayout(layout)

    def setup_banner(self, layout):
        banner_layout = QHBoxLayout()
        self.banner = QLabel(self)
        self.banner.setPixmap(QPixmap("scripts\\banner.png").scaled(200, 100, aspectRatioMode=Qt.KeepAspectRatio))
        banner_layout.addStretch()
        banner_layout.addWidget(self.banner)
        banner_layout.addStretch()
        layout.addLayout(banner_layout)

    def setup_search_bar(self, layout):
        self.search_bar = QLineEdit(self)
        self.search_bar.setPlaceholderText("Search for a game...")
        self.search_bar.setStyleSheet("background-color: #444444; color: white; padding: 5px; border-radius: 3px;")
        self.search_bar.textChanged.connect(self.on_search)
        layout.addWidget(self.search_bar)

    def setup_scroll_area(self, layout):
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)
        layout.addWidget(self.scroll_area)

    def setup_buttons(self, layout):
        buttons_layout = QHBoxLayout()

        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.on_submit)
        self.apply_button_styles(self.submit_button)

        self.waitlist_button = QPushButton("View Waitlist", self)
        self.waitlist_button.clicked.connect(self.view_waitlist)
        self.apply_button_styles(self.waitlist_button)

        buttons_layout.addWidget(self.submit_button)
        buttons_layout.addWidget(self.waitlist_button)
        layout.addLayout(buttons_layout)

    def apply_button_styles(self, button):
        button.setStyleSheet("background-color: #888888; color: white; padding: 5px; border-radius: 3px;")

    def load_gamelist(self):
        with open('scripts\\gamelist.json') as f:
            self.gamelist = json.load(f)
        self.update_game_list(self.gamelist)

    def update_game_list(self, games):
        self.clear_game_list()
        for game in games:
            game_button = QPushButton(game['text'], self)
            game_button.clicked.connect(lambda checked, g=game: self.handle_service_selection(g))
            game_button.setStyleSheet("background-color: #444444; color: white; padding: 5px; border-radius: 3px; height: 30px;")
            self.scroll_layout.addWidget(game_button)

    def clear_game_list(self):
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()

    def on_search(self):
        search_text = self.search_bar.text().lower()
        filtered_games = [game for game in self.gamelist if search_text in game['text'].lower()]
        self.update_game_list(filtered_games)

    def on_submit(self):
        pass  # Implement functionality as needed

    def handle_service_selection(self, game):
        found_urls = scrape_urls(game['url'])
        if not found_urls:
            QMessageBox.warning(self, "Warning", "No valid URLs found. Please check the entered URL.")
            return

        available_services = self.extract_services(found_urls)
        if not available_services:
            QMessageBox.warning(self, "Warning", "No valid download services found from the URLs.")
            return

        self.show_service_selection_dialog(game, available_services, found_urls)

    def show_service_selection_dialog(self, game, available_services, found_urls):
        service_dialog = QDialog(self)
        service_dialog.setWindowTitle("Select Download Service")
        service_dialog.setFixedSize(300, 200)

        layout = QVBoxLayout(service_dialog)
        service_combo = QComboBox(service_dialog)
        service_combo.addItems(["Select a service"] + available_services)
        service_combo.setStyleSheet("background-color: #444444; color: white; border-radius: 3px; padding: 5px;")
        layout.addWidget(service_combo)

        confirm_button = QPushButton("Confirm", service_dialog)
        confirm_button.setStyleSheet("background-color: #888888; color: white; padding: 5px; border-radius: 3px;")
        layout.addWidget(confirm_button)

        confirm_button.clicked.connect(lambda: self.finalize_download_selection(game, service_combo.currentText(), found_urls, service_dialog))
        service_dialog.exec_()

    def extract_services(self, found_urls):
        services_map = {
            'https://megadb.net/': 'MegaDB',
            'https://buzzheavier.com/': 'BuzzHeavier',
            'https://1fichier.com/': '1Fichier',
            'https://gofile.io/': 'Gofile'
        }

        return list({services_map[prefix] for url in found_urls for prefix in services_map if url.startswith(prefix)})

    def finalize_download_selection(self, game, selected_service, found_urls, dialog):
        if selected_service == "Select a service":
            QMessageBox.warning(self, "Warning", "Please select a valid download service.")
            return

        download_data = {
            "game_title": game["text"],
            "download_service": selected_service,
            "download_link": found_urls
        }
        self.save_to_waitlist(download_data)
        QMessageBox.information(self, "Success", "Download information saved successfully!")
        dialog.accept()

    def save_to_waitlist(self, download_data):
        try:
            with open('scripts\\DownloadWaitlist.json', 'r') as f:
                waitlist = json.load(f)
        except FileNotFoundError:
            waitlist = []

        if any(item['game_title'] == download_data['game_title'] and item['download_service'] == download_data['download_service'] for item in waitlist):
            QMessageBox.warning(self, "Warning", "This game is already in the waitlist.")
            return

        waitlist.append(download_data)
        with open('scripts\\DownloadWaitlist.json', 'w') as f:
            json.dump(waitlist, f, indent=4)

        QMessageBox.information(self, "Success", "Download information saved successfully!")

    def view_waitlist(self):
        if self.waitlist_dialog is not None:
            self.waitlist_dialog.close()

        self.waitlist_dialog = QDialog(self)
        self.waitlist_dialog.setWindowTitle("Download Waitlist")
        self.waitlist_dialog.setFixedSize(600, 300)

        layout = QVBoxLayout(self.waitlist_dialog)

        try:
            with open('scripts\\DownloadWaitlist.json', 'r') as f:
                waitlist = json.load(f)
        except FileNotFoundError:
            waitlist = []

        if not waitlist:
            layout.addWidget(QLabel("No items in the waitlist.", self.waitlist_dialog))
        else:
            self.add_waitlist_checkboxes(waitlist, layout)

        # Layout for buttons
        buttons_layout = QHBoxLayout()
        
        # Remove Selected button
        remove_button = QPushButton("Remove Selected", self.waitlist_dialog)
        remove_button.setStyleSheet("background-color: #888888; color: white; padding: 5px; border-radius: 3px;")
        remove_button.clicked.connect(self.remove_selected_items)
        buttons_layout.addWidget(remove_button)

        # Start getallcaptures.py button
        start_button = QPushButton("Start Get All Captures", self.waitlist_dialog)
        start_button.setStyleSheet("background-color: #888888; color: white; padding: 5px; border-radius: 3px;")
        start_button.clicked.connect(self.start_getallcaptures)
        buttons_layout.addWidget(start_button)

        layout.addLayout(buttons_layout)

        self.waitlist_dialog.exec_()

    def start_getallcaptures(self):
        import subprocess
        import sys

        # Determine the appropriate command based on the operating system
        if sys.platform.startswith('win'):
            # On Windows, use 'cmd' with '/c' to execute the command and close the terminal after execution
            command = ['cmd', '/c', 'start', 'cmd', '/c', 'py', 'scripts\\getallcaptures.py']
        else:
            # On Linux, use 'gnome-terminal' with '--' and '-e' to run the command and close the terminal after execution
            command = ['gnome-terminal', '--', '-e', 'python3 scripts\\getallcaptures.py']

        # Start the process in a new terminal window
        print("Executing command:", command)
        subprocess.Popen(command)




    def load_waitlist(self):
        try:
            with open('scripts\\DownloadWaitlist.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def add_waitlist_checkboxes(self, waitlist, layout):
        self.checkboxes = []
        for item in waitlist:
            checkbox = QCheckBox(f"Game: {item['game_title']} | Service: {item['download_service']}", self.waitlist_dialog)
            checkbox.setStyleSheet("background-color: #444444; color: white; padding: 5px;")
            self.checkboxes.append((checkbox, item))
            layout.addWidget(checkbox)

    def remove_selected_items(self):
        if not self.checkboxes:
            return
        
        for checkbox, item in self.checkboxes:
            if checkbox.isChecked():
                self.remove_from_waitlist(item['game_title'], item['download_service'])
                self.checkboxes.remove((checkbox, item))
                checkbox.deleteLater()  # Remove the checkbox from the layout

    def remove_from_waitlist(self, game_title, download_service):
        try:
            with open('scripts\\DownloadWaitlist.json', 'r') as f:
                waitlist = json.load(f)
        except FileNotFoundError:
            waitlist = []

        # Filter out the item to remove
        waitlist = [item for item in waitlist if not (item['game_title'] == game_title and item['download_service'] == download_service)]

        with open('scripts\\DownloadWaitlist.json', 'w') as f:
            json.dump(waitlist, f, indent=4)

        QMessageBox.information(self, "Success", "Selected items removed from the waitlist!")


def filter_unwanted_games(games):
    unwanted_start = [
        {"text": "Menu", "url": "https://steamrip.com#"},
        {"text": "Games List", "url": "https://steamrip.com/"},
        {"text": "Search for", "url": "https://steamrip.com#"},
        {"text": "", "url": "https://steamrip.com/"},
        {"text": "Home", "url": "https://steamrip.com/"},
        {"text": "Categories", "url": "https://steamrip.com#"},
        {"text": "Action", "url": "https://steamrip.com/category/action/"},
        {"text": "Adventure", "url": "https://steamrip.com/category/adventure/"},
        {"text": "Anime", "url": "https://steamrip.com/category/anime/"},
        {"text": "Horror", "url": "https://steamrip.com/category/horror/"},
        {"text": "Indie", "url": "https://steamrip.com/category/indie/"},
        {"text": "Multiplayer", "url": "https://steamrip.com/category/multiplayer/"},
        {"text": "Open World", "url": "https://steamrip.com/category/open-world/"},
        {"text": "Racing", "url": "https://steamrip.com/category/racing/"},
        {"text": "Shooters", "url": "https://steamrip.com/category/shooting/"},
        {"text": "Simulation", "url": "https://steamrip.com/category/simulation/"},
        {"text": "Sports", "url": "https://steamrip.com/category/sports/"},
        {"text": "Strategy", "url": "https://steamrip.com/category/strategy/"},
        {"text": "Virtual Reality", "url": "https://steamrip.com/category/vr/"},
        {"text": "Top Games", "url": "https://steamrip.com/top-games/"},
        {"text": "Recent Updates", "url": "https://steamrip.com/updated-games/"},
        {"text": "Games List", "url": "https://steamrip.com/games-list/"},
        {"text": "FAQ", "url": "https://steamrip.com#"},
        {"text": "All FAQs", "url": "https://steamrip.com/faq/"},
        {"text": "How to Run Games", "url": "https://steamrip.com/steps-for-games/"},
        {"text": "Discord", "url": "https://steamrip.com//discord.gg/WkyjpA3Ua9"},
        {"text": "Switch skin", "url": "https://steamrip.com#"},
        {"text": "Search for", "url": "https://steamrip.com#"}
    ]

    unwanted_end = [
        {"text": "About", "url": "https://steamrip.com/about/"},
        {"text": "Request Games", "url": "https://steamrip.com/request-games/"},
        {"text": "Privacy Policy", "url": "https://steamrip.com/privacy-policy/"},
        {"text": "Terms & Conditions", "url": "https://steamrip.com/terms-and-conditions/"},
        {"text": "Contact Us", "url": "https://steamrip.com/contact-us/"},
        {"text": "Reddit", "url": "https://steamrip.com//www.reddit.com/r/SteamRip/"},
        {"text": "Discord", "url": "https://steamrip.com//discord.gg/WkyjpA3Ua9"},
        {"text": "Back to top button", "url": "https://steamrip.com#go-to-tie-body"},
        {"text": "Close", "url": "https://steamrip.com#"},
        {"text": "Close", "url": "https://steamrip.com#"},
        {"text": "Close", "url": "https://steamrip.com#"}
    ]

    # Convert the unwanted lists to a set for faster lookup
    unwanted_set = {f"{item['text']}|{item['url']}" for item in unwanted_start + unwanted_end}

    # Filter out unwanted games
    filtered_games = [
        game for game in games 
        if f"{game['text']}|{game['url']}" not in unwanted_set
    ]
    return filtered_games

# Main application execution
if __name__ == "__main__":
    hyperlinks = grab_hyperlinks()
    
    if hyperlinks:
        cleanhyperlinks = filter_unwanted_games(hyperlinks)
        save_to_json(cleanhyperlinks, 'scripts\\gamelist.json')
        print(f"Extracted {len(hyperlinks)} Games and saved to 'scripts\\gamelist.json'.")
    else:
        print("No hyperlinks found or an error occurred.")



    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

