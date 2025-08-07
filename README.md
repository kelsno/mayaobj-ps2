# PS2 DEV model converter
A Python tool that converts MAYA models to JSON --> which then makes a C file to use in ps2dev.

# MayaOBJ-JSON
This script converts your model into a JSON file that has selected Maya mesh's vertex positions, UVs, and triangle indices.

**MAKE SURE YOUR MODEL IS TRIANGULATED** 

<img width="1170" height="880" alt="Screenshot 2025-08-06 at 23 30 05" src="https://github.com/user-attachments/assets/4b1e506b-e2a3-4e6f-888a-0a0a5a23e910" />

## Usage

Head on over to the Python editor in MAYA.
<br>
<br>
Windows -> General Editors -> Script Editor
<br>
<br>
Copy and paste the script (MAYA2JSON.py) while selecting your model -- at line 125, make sure to set your directory you want your C file in -- and run it.
<br>
<br>
e.g.
```
output_file_path = "/Users/kel/my_game/"
export_ps2_mesh_data(output_file_path)
```

# JSON-PS2
This script converts the JSON file generated into a C file what you can use as a mesh data.

## Usage
Run this in terminal.
```
python3 convert_to_ps2_mesh.py <input_json_file> <output_c_file>
```
or use the GUI

<img width="691" height="475" alt="Screenshot 2025-08-06 at 23 59 05" src="https://github.com/user-attachments/assets/7dfa7b5f-aeef-48fb-9ff1-e50a8b632a09" />

# Credits
Christopher Morales Soriano (kelsno) &
PS2DEV
