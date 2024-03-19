import xml.etree.ElementTree as ET
import json
import tkinter as tk
from tkinter import filedialog
import math


def extract_svg_attributes(svg_file):
    tree = ET.parse(svg_file)
    root = tree.getroot()

    width = math.floor(float(root.get('width')))
    height = math.floor(float(root.get('height')))
    viewbox_values = root.get('viewBox').split()
    viewbox = " ".join(str(math.floor(float(val))) for val in viewbox_values)

    return width, height, viewbox


def get_d_and_transform(svg_file):
    tree = ET.parse(svg_file)
    root = tree.getroot()

    d = None
    transform = None

    for elem in root.iter():
        if elem.get('id') == "layer1":
            count = 0
            for child in elem:
                if child.tag == "{http://www.w3.org/2000/svg}path":
                    count += 1
                    if count == 2:  # Find the second path element
                        d = child.get('d')
                        transform = child.get('transform')
                        break
            break

    return d, transform


def save_to_json(width, height, viewbox, x, y, d, transform, json_file, puzzle_size):
    try:
        with open(json_file, 'r') as f:
            json_data = json.load(f)
    except FileNotFoundError:
        json_data = {"puzzle4x4": {"pieces": []}}

    pieces = json_data["puzzle4x4"]["pieces"]
    piece_id = f"piece{len(pieces) + 1}"

    json_data["puzzle4x4"]["pieces"].append({
        "item": len(pieces),
        "id": piece_id,
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "viewbox": viewbox,
        "path": d,
        "transform": transform
    })

    # Vytvoření názvu puzzle v JSON souboru na základě velikosti puzzle
    puzzle_name = f"puzzle{puzzle_size}x{puzzle_size}"
    if puzzle_name not in json_data:
        json_data[puzzle_name] = {"pieces": []}

    with open(json_file, 'w') as f:
        json.dump(json_data, f, indent=2)


def select_svg_files():
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(title="Vyberte SVG soubory", filetypes=[("SVG files", "*.svg")])
    return file_paths


def calculate_puzzle_size(num_images):
    # Výpočet velikosti puzzle podle počtu obrázků
    return int(math.sqrt(num_images))


if __name__ == "__main__":
    svg_files = select_svg_files()
    json_file = 'output.json'

    num_images = len(svg_files)
    puzzle_size = calculate_puzzle_size(num_images)

    for svg_file in svg_files:
        width, height, viewbox = extract_svg_attributes(svg_file)
        x = 0
        y = 0
        d, transform = get_d_and_transform(svg_file)
        save_to_json(width, height, viewbox, x, y, d, transform, json_file, puzzle_size)
