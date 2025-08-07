import maya.cmds as cmds
import maya.OpenMaya as om
import json
import os

def export_ps2_mesh_data(output_json_path):
    try:
        selection_list = om.MSelectionList()
        om.MGlobal.getActiveSelectionList(selection_list)

        if selection_list.isEmpty():
            cmds.warning("No object selected. Please select a mesh to export.")
            return

        mesh_dag_path = om.MDagPath()
        selection_list.getDagPath(0, mesh_dag_path)

        if not mesh_dag_path.hasFn(om.MFn.kMesh):
            cmds.error(f"Selected object '{mesh_dag_path.fullPathName()}' is not a mesh. Please select a polygon mesh.")
            return

        mesh_shape_name = mesh_dag_path.fullPathName()
        print(f"DEBUG: Selected mesh DAG path: {mesh_shape_name}")
        print(f"DEBUG: Selected object type: {cmds.nodeType(mesh_shape_name)}")

        mesh_fn = om.MFnMesh(mesh_dag_path)
        print(f"DEBUG: MFnMesh created successfully for: {mesh_shape_name}")

        unique_vertex_data = []
        vertex_map = {}
        faces_indices = []

        all_maya_vertices = om.MFloatPointArray()
        mesh_fn.getPoints(all_maya_vertices, om.MSpace.kWorld)
        print(f"DEBUG: Retrieved {all_maya_vertices.length()} vertex positions.")

        all_maya_uvs_u = om.MFloatArray()
        all_maya_uvs_v = om.MFloatArray()
        mesh_fn.getUVs(all_maya_uvs_u, all_maya_uvs_v)
        print(f"DEBUG: Retrieved {all_maya_uvs_u.length()} UVs.")

        polygon_it = om.MItMeshPolygon(mesh_dag_path)
        print(f"DEBUG: Initialized MItMeshPolygon for: {mesh_shape_name}")

        while not polygon_it.isDone():
            face_vertex_ids = om.MIntArray()
            polygon_it.getVertices(face_vertex_ids)

            face_uv_indices = om.MIntArray()

            for i in range(face_vertex_ids.length()):

                uv_idx_util = om.MScriptUtil()
                uv_idx_ptr = uv_idx_util.asIntPtr()

                polygon_it.getUVIndex(i, uv_idx_ptr, "map1")

                uv_idx_for_this_face_vertex = uv_idx_util.asInt()
                face_uv_indices.append(uv_idx_for_this_face_vertex)


            if face_vertex_ids.length() != 3 or face_uv_indices.length() != 3:
                cmds.warning(f"Face {polygon_it.index()} is not a triangle or has mismatched vertex/UV count. "
                             "This script assumes the mesh is already triangulated. Skipping this face.")
                polygon_it.next()
                continue

            for i in range(face_vertex_ids.length()):
                current_vertex_id = face_vertex_ids[i]
                current_uv_index = face_uv_indices[i]


                pos = all_maya_vertices[current_vertex_id]
                x, y, z = pos.x, pos.y, pos.z

                u = all_maya_uvs_u[current_uv_index]
                v = all_maya_uvs_v[current_uv_index]


                vertex_key = (round(x, 6), round(y, 6), round(z, 6), round(u, 6), round(v, 6))

                if vertex_key not in vertex_map:
                    new_index = len(unique_vertex_data)
                    unique_vertex_data.append({
                        "position": [x, y, z],
                        "uv": [u, v]
                    })
                    vertex_map[vertex_key] = new_index

                faces_indices.append(vertex_map[vertex_key])

            polygon_it.next()

        print(f"DEBUG: Finished iterating through faces. Total unique vertices: {len(unique_vertex_data)}, Total face indices: {len(faces_indices)}")

        exported_vertices = []
        exported_sts = []
        for data_item in unique_vertex_data:
            exported_vertices.append(data_item["position"])
            exported_sts.append(data_item["uv"])

        output_data = {
            "faces_count": len(faces_indices),
            "faces": faces_indices,
            "vertex_count": len(exported_vertices),
            "vertices": exported_vertices,
            "sts": exported_sts
        }

        with open(output_json_path, 'w') as f:
            json.dump(output_data, f, indent=2)
        cmds.inViewMessage(msg=f"Mesh data exported successfully to: {output_json_path}", pos='midCenter', fadeStayTime=2, fadeOutTime=0.5)
        print(f"Mesh data exported successfully to: {output_json_path}")

    except Exception as e:
        cmds.error(f"An error occurred during export: {e}")
    finally:
        pass

# Replace with your desired output path.
# For Windows: C:/path/to/your/project/my_model_data.json
# For macOS/Linux: /path/to/your/project/my_model_data.json
# Ensure the directory exists before running the script.
output_file_path = "PATH HERE"
export_ps2_mesh_data(output_file_path)
