import json
import os
import time

# Constants
JSON_FILE = 'scripts\\DownloadWaitlist.json'  # Input JSON file
OUTPUT_FILE = 'exported_links.txt'    # Output text file

def export_links(json_file, output_file):
    # Load the JSON file
    try:
        with open(json_file, 'r') as file:
            data = json.load(file)
            print(f"Loaded JSON file successfully. Found {len(data)} entries.")
    except FileNotFoundError:
        print(f"File {json_file} not found!")
        return
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file {json_file}. Please check the file format.")
        return

    # Prepare the output
    output_lines = []
    all_links = []

    for game in data:
        game_title = game.get('game_title', 'Unknown Game')
        download_links = game.get('download_link', [])

        for link in download_links:
            output_lines.append(f"{game_title} ~ {link}")
            all_links.append(link)

    # Write to the output file
    with open(output_file, 'w') as file:
        file.write("\n".join(output_lines) + "\n\n")
        file.write(" ".join(all_links))  # Write all links in one paragraph

    print(f"Exported links to {output_file} successfully.")
    time.sleep(10)
    exit()

if __name__ == '__main__':
    export_links(JSON_FILE, OUTPUT_FILE)
