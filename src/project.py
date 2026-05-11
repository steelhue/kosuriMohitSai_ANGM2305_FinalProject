import math
import maya.cmds as cmds

def get_angle(vert_pos, center_x, center_z):
    pos = vert_pos[1]
    return math.atan2(pos[2] - center_z, pos[0] - center_x)


def sort_verts_clockwise(verts):
    vert_positions = []
    for vert in verts:
        pos = cmds.xform(vert, q=True, ws=True, t=True)
        vert_positions.append((vert, pos))

    center_x = sum(p[1][0] for p in vert_positions) / len(vert_positions)
    center_y = sum(p[1][1] for p in vert_positions) / len(vert_positions)
    center_z = sum(p[1][2] for p in vert_positions) / len(vert_positions)

    vert_positions.sort(key=lambda vp: get_angle(vp, center_x, center_z))

    return [vp[0] for vp in vert_positions]


def group_edges_by_corner(verts):
    vert_indices = []
    edges_group = []

    mesh_name = verts[0].split(".")[0]

    for vert in verts:
        idx = vert.split(".")[1]
        idx = idx.replace("vtx[", "").replace("]", "")
        vert_indices.append(idx)

    vert_A = vert_indices[0]
    vert_B = vert_indices[1]
    vert_C = vert_indices[2]
    vert_D = vert_indices[3]


    side_a = cmds.polySelect(mesh_name, shortestEdgePath=[int(vert_A), int(vert_B)])
    edges_group.append(side_a)


    side_b = cmds.polySelect(mesh_name, shortestEdgePath=[int(vert_B), int(vert_C)])
    edges_group.append(side_b)


    side_c = cmds.polySelect(mesh_name, shortestEdgePath=[int(vert_C), int(vert_D)])
    edges_group.append(side_c)


    side_d = cmds.polySelect(mesh_name, shortestEdgePath=[int(vert_D), int(vert_A)])
    edges_group.append(side_d)

    cmds.select(clear=True)
    return edges_group



def edges_to_curves(edges_group, mesh_name):
    curves_group = []

    for edges in edges_group:
        # Select all edges in this side
        cmds.select(clear=True)
        edge_components = [f"{mesh_name}.e[{e}]" for e in edges]
        cmds.select(edge_components)

        # Convert to curve
        result = cmds.polyToCurve(form=0, degree=1)
        curves_group.append(result[0])

        cmds.select(clear=True)

    return curves_group 


def main():
    cmds.selectPref(isp=False, trackSelectionOrder=True)
    verts = cmds.ls(orderedSelection=True)
    verts = cmds.ls(verts, flatten=True)
    if not verts:
        cmds.warning("No verts selected.")
        return
    verts = sort_verts_clockwise(verts)
    print(verts)
    mesh_name = verts[0].split(".")[0]
    edges_group = group_edges_by_corner(verts)
    curves_group = edges_to_curves(edges_group, mesh_name)

    filled_obj_name = f"{mesh_name}_fill"

    patch_nurbs = cmds.boundary(curves_group[0:], ch=False, n=filled_obj_name)
    cmds.delete(curves_group)

    patch_poly = cmds.nurbsToPoly(patch_nurbs, constructionHistory=False, format=3, polygonType=1, uType=3, vType=3)
    filled_obj_name = patch_poly[0]
    cmds.delete(patch_poly, constructionHistory=True)

    combined = cmds.polyUnite(mesh_name, filled_obj_name, n=mesh_name)
    cmds.polyMergeVertex(combined[0], distance=0.001, constructionHistory=False)
    
    cmds.delete(combined, constructionHistory=True)
    cmds.delete(patch_nurbs)


if __name__ == "__main__":
    main()
