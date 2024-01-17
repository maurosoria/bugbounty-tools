#/usr/bin/env bash
import json
import os
import sys

"""
ChatGPT4 prompt:
- Create a Python script named extract_js_map.py. 
- The script should read a .js.map file, extract JavaScript source files contained within it, and save them in a new directory. 
- The directory should be named after the base filename of the .js.map file. 
- Include error handling for invalid files and clear instructions for usage. 
- Add detailed comments for each function and section of the script. 
- The script is intended for use in web development and bug bounty hunting.
"""

def extract_js_sources(map_file_path):
    """
    Extracts JavaScript source files from a .js.map file and saves them in a directory.

    Args:
    map_file_path (str): Path to the .js.map file.

    Returns:
    None
    """
    try:
        # Extract base filename without extension
        base_name = os.path.splitext(os.path.basename(map_file_path))[0]

        # Create a directory for extracted files
        output_dir = base_name + "_sources"
        if not os.path.exists(output_dir):
            os.mkdir(output_dir)

        # Read and parse the .js.map file
        with open(map_file_path, 'r') as file:
            map_data = json.load(file)

        # Check if sources and sourcesContent are in the file
        if "sources" not in map_data or "sourcesContent" not in map_data:
            raise ValueError("Invalid .js.map file format")

        # Extract and save each source file
        for i, source in enumerate(map_data["sources"]):
            file_path = os.path.join(output_dir, os.path.basename(source))
            with open(file_path, 'w') as src_file:
                src_file.write(map_data["sourcesContent"][i])

        print("Extraction complete. Files saved in:", output_dir)

    except FileNotFoundError:
        print("Error: .js.map file not found.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON in .js.map file.")
    except OSError as e:
        print("OS error:", e)
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_js_map.py <path-to-.js.map-file>")
    else:
        extract_js_sources(sys.argv[1])