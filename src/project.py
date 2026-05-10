import maya.cmds as cmds


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

    cmds.select(clear=True)
    side_a = cmds.polySelect(mesh_name, shortestEdgePath=[int(vert_A), int(vert_B)])
    edges_group.append(side_a)

    cmds.select(clear=True)
    side_b = cmds.polySelect(mesh_name, shortestEdgePath=[int(vert_B), int(vert_C)])
    new_side_b = []
    for edge in side_b:
        if edge not in side_a:
            new_side_b.append(edge)
    edges_group.append(new_side_b)

    cmds.select(clear=True)
    side_c = cmds.polySelect(mesh_name, shortestEdgePath=[int(vert_C), int(vert_D)])
    edges_group.append(side_c)

    cmds.select(clear=True)
    side_d = cmds.polySelect(mesh_name, shortestEdgePath=[int(vert_D), int(vert_A)])
    new_side_d = []
    for edge in side_d:
        if edge not in side_a:
            new_side_d.append(edge)
    edges_group.append(new_side_d)

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
    verts = cmds.ls(selection=True, flatten=True)
    if not verts:
        cmds.warning("No verts selected.")
        return

    mesh_name = verts[0].split(".")[0]
    edges_group = group_edges_by_corner(verts)
    print(edges_group)

    curves_group = edges_to_curves(edges_group, mesh_name)
    print(curves_group)


if __name__ == "__main__":
    main()
