import os,sys
import re
import json
import requests
import shutil
from steamgrid import SteamGridDB, StyleType, MimeType

sgdb = SteamGridDB('')

services_map = { 
    'https://megadb.net/': 'MegaDB',
    'https://buzzheavier.com/': 'BuzzHeavier',
    'https://1fichier.com/': '1Fichier',
    'https://gofile.io/': 'Gofile'
}

# Clean folder names by removing special characters
def sanitize_folder_name(folder_name):
    return re.sub(r'[^\w\-_\. ]', '', folder_name)

def clean_game_title(title):
    return title.split(" Free")[0]

def get_download_link(download_service, download_links):
    for link in download_links:
        for service_url in services_map.keys():
            if service_url in link and services_map[service_url] == download_service:
                return link
    return None

def download_capsule_image(game_name):
    result = sgdb.search_game(game_name)
    if result:
        game = result[0]
        print(f"Downloading capsule for: {game.name} (ID: {game.id})")
        grids = sgdb.get_grids_by_gameid([game.id], mimes=[MimeType.PNG])
        if grids:
            first_grid = grids[0]
            image_url = first_grid.url
            image_response = requests.get(image_url)
            if image_response.status_code == 200:
                sanitized_name = sanitize_folder_name(game_name)
                output_dir = os.path.join('output', sanitized_name)
                os.makedirs(output_dir, exist_ok=True)
                image_path = os.path.join(output_dir, 'Capsule.png')
                with open(image_path, "wb") as img_file:
                    img_file.write(image_response.content)
                print(f"Downloaded {image_path}")
            else:
                print(f"Failed to download image from {image_url}")
        else:
            print(f"No grids found for {game_name}.")
    else:
        print(f"No game found for {game_name}.")

# Clean the output folder even if it contains files or directories
def clean_output_folder():
    output_path = 'output'
    if os.path.exists(output_path):
        response = input(f"The output folder '{output_path}' already exists. Do you want to clean it? (y/n): ")
        if response.lower() == 'y':
            # Recursively remove all files and folders in the output directory
            shutil.rmtree(output_path)
            os.makedirs(output_path)
            print(f"Cleaned the output folder: '{output_path}'.")
    else:
        os.makedirs(output_path)

with open('scripts\\DownloadWaitlist.json', 'r') as file:
    games = json.load(file)

clean_output_folder()

for game in games:
    title = clean_game_title(game['game_title'])
    download_service = game['download_service']
    download_link = get_download_link(download_service, game['download_link'])

    if download_link:
        print(f"Using download link: {download_link}")
        download_capsule_image(title)
    else:
        print(f"No valid download link found for {game['game_title']}.")

print('\n\n\nWe suggest you to start the script "ExportListAsTxt" to get all download links and import them to IDM\n\n\n')

input('Done, press any Key to qui the capsule downloader')
sys.exit(0)