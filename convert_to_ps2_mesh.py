import json
import os
import sys
import argparse


def convert_json_to_ps2_c_mesh(input_json_path, output_c_path):
    print(f"[convert_to_ps2_mesh.py] Starting conversion from '{input_json_path}' to '{output_c_path}'...")

    if not os.path.exists(input_json_path):
        print(f"[convert_to_ps2_mesh.py] ERROR: Input file not found at '{input_json_path}'.")
        return False

    try:
        with open(input_json_path, 'r') as f:
            mesh_data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"[convert_to_ps2_mesh.py] ERROR: Input file '{input_json_path}' is not a valid JSON file. Details: {e}")
        return False
    except Exception as e:
        print(f"[convert_to_ps2_mesh.py] ERROR: An unexpected error occurred while reading '{input_json_path}': {e}")
        return False

    faces_count = mesh_data.get("faces_count", 0)
    faces = mesh_data.get("faces", [])
    vertex_count = mesh_data.get("vertex_count", 0)
    vertices = mesh_data.get("vertices", [])
    sts = mesh_data.get("sts", [])

    if not (faces and vertices and sts and faces_count > 0 and vertex_count > 0):
        print("[convert_to_ps2_mesh.py] ERROR: Missing or empty mesh data (faces, vertices, or sts) in JSON file. Conversion aborted.")
        return False


    if os.path.isdir(output_c_path):
        original_output_path = output_c_path
        output_c_path = os.path.join(output_c_path, "mesh_data.c")
        print(f"[convert_to_ps2_mesh.py] WARNING: Output path '{original_output_path}' is a directory. Automatically saving as '{output_c_path}'.")
    elif not output_c_path.lower().endswith(('.c', '.h')):
        print(f"[convert_to_ps2_mesh.py] WARNING: Output file '{output_c_path}' does not have a .c or .h extension. Proceeding anyway.")


    c_code_content = []
    c_code_content.append("/*")
    c_code_content.append("# _____     ___ ____     ___ ____")
    c_code_content.append("#  ____|   |    ____|   |        | |____|")
    c_code_content.append("# |     ___|   |____ ___|    ____| |    \\    PS2DEV Open Source Project.")
    c_code_content.append("#-----------------------------------------------------------------------")
    c_code_content.append(f"# Generated from 3D model data by {AUTHOR_NAME}")
    c_code_content.append("*/\n")

    c_code_content.append("#ifndef __GENERATED_MESH_DATA__")
    c_code_content.append("#define __GENERATED_MESH_DATA__\n")

    c_code_content.append(f"int faces_count = {faces_count};\n")
    c_code_content.append("/** \n * Array of vertex indexes.\n * 3 faces = 1 triangle \n */")
    c_code_content.append(f"int faces[{faces_count}] = {{")

    for i in range(0, faces_count, 3):
        line_start = "    "
        if i + 2 < faces_count:
            c_code_content.append(f"{line_start}{faces[i]}, {faces[i+1]}, {faces[i+2]},")
        else:
            remaining_indices = ", ".join(map(str, faces[i:]))
            c_code_content.append(f"{line_start}{remaining_indices}")
    c_code_content.append("};\n")

    c_code_content.append(f"int vertex_count = {vertex_count};\n")
    c_code_content.append(f"VECTOR vertices[{vertex_count}] = {{")

    for i, vert in enumerate(vertices):
        x, y, z = vert[0], vert[1], vert[2]
        line_end = "," if i < vertex_count - 1 else ""
        c_code_content.append(f"    {{ {x:.6f}f, {y:.6f}f, {z:.6f}f, 1.00f }}{line_end}")
    c_code_content.append("};\n")

    c_code_content.append("/** Texture coordinates */")
    c_code_content.append(f"VECTOR sts[{vertex_count}] = {{")

    for i, uv in enumerate(sts):
        s, t = uv[0], uv[1]
        line_end = "," if i < vertex_count - 1 else ""
        c_code_content.append(f"    {{ {s:.6f}f, {t:.6f}f, 1.00f, 0.00f }}{line_end}")
    c_code_content.append("};\n")

    c_code_content.append("#endif // __GENERATED_MESH_DATA__\n")

    try:
        output_dir = os.path.dirname(output_c_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"[convert_to_ps2_mesh.py] Created output directory: {output_dir}")

        with open(output_c_path, 'w') as f:
            f.write("\n".join(c_code_content))
        print(f"[convert_to_ps2_mesh.py] Successfully generated C mesh data to: {output_c_path}")
        return True
    except Exception as e:
        print(f"[convert_to_ps2_mesh.py] ERROR: Writing output C file failed: {e}")
        return False

def show_menu():
    print("\n" + "="*40)
    print(f" Welcome to PS2 Mesh Converter by Christopher Morales (kelsno)")
    print("="*40)
    print("\nSelect an option:")
    print("1. Convert JSON to PS2 C Mesh")
    print("2. Exit")
    print("="*40)

def main_interactive():
    while True:
        show_menu()
        choice = input("Enter your choice (1-2): ").strip()

        if choice == '1':
            input_json = input("Enter path to input JSON file: ").strip()
            output_c = input("Enter path for output C file: ").strip()

            if convert_json_to_ps2_c_mesh(input_json, output_c):
                print("\nConversion complete!")
            else:
                print("\nConversion failed. Please check the errors above.")
            input("\nPress Enter to continue...")
        elif choice == '2':
            sys.exit(0)
        else:
            print("\nInvalid choice. Please enter 1 or 2.")
            input("\nPress Enter to continue...")

if __name__ == "__main__":
    if len(sys.argv) == 3:
        print("[convert_to_ps2_mesh.py] Running in direct conversion mode (2 command-line arguments detected).")
        parser = argparse.ArgumentParser(
            description="Converts a JSON file containing mesh data into a C source file in the PS2DEV Template."
                        "\n"
                        "Usage: python3 convert_to_ps2_mesh.py <input_json_file> <output_c_file>"
        )
        parser.add_argument(
            "input_json_file",
            type=str,
            help="The full path to the input JSON file."
        )
        parser.add_argument(
            "output_c_file",
            type=str,
            help="The full path for the output C source file (mesh_data.c in your PS2Dev project)."
        )
        args = parser.parse_args()
        success = convert_json_to_ps2_c_mesh(args.input_json_file, args.output_c_file)
        if not success:
            sys.exit(1)
        sys.exit(0)
    else:
        if len(sys.argv) > 1:
            print("[convert_to_ps2_mesh.py] WARNING: Incorrect number of command-line arguments for direct mode.")
            print("[convert_to_ps2_mesh.py] Usage for direct mode: python convert_to_ps2_mesh.py <input_json_file> <output_c_file>")
        main_interactive()
