import maya.cmds as cmds

# group edges based on the angle
        # To do this, we need to get the vector of each edge and 
        # compare it to the next connected egde
    # if the edge is >= 90 to the other edge, group the edges
# convert the grouped edges to curves
# using the boundry tool, select the edges and make the mesh
# combine the meshes and apply merge by distance

def get_adjacent_boundry_edge(current_edge, visited_edge):
    verts = cmds.polyListComponentConversion(current_edge, toVertex=True)
    verts = cmds.ls(verts, flatten=True)

    for vert in verts:
        # Get all edges connected to this vertex
        connected_edges = cmds.polyListComponentConversion(vert, toEdge=True)
        connected_edges = cmds.ls(connected_edges, flatten=True)

        for edge in connected_edges:
            if edge == current_edge:
                continue
            if edge in visited_edge:
                continue

            # Only follow boundary edges (edges with 1 face connection)
            face_check = cmds.polyListComponentConversion(edge, toFace=True)
            face_check = cmds.ls(face_check, flatten=True)
            if len(face_check) == 1:
                return edge, vert  # return the next edge and the shared vertex

    return None, None


def get_connected_edges(vertex):
    mesh = vertex.split(".")[0]
    info = cmds.polyInfo(vertex, vertexToEdge=True)
    connected_edges = info[0].split(":")[1].split()
    # return len(connected_edges)
    return [f"{mesh}.e[{idx}]" for idx in connected_edges]


def group_edge_by_corner():
    selected = cmds.ls(selection=True, flatten=True)
    if not selected:
        cmds.warning("No Edges Selected")
        return[]
    
    start_edge = selected[0]

    all_group = []
    current_group = []
    visited_edges = set()

    current_edge = start_edge

    while True:
        visited_edges.add(current_edge)

        verts = cmds.polyListComponentConversion(current_edge, toVertex=True)
        verts = cmds.ls(verts, flatten=True)

        for vert in verts:
            if vert in [v for group in all_group for v in group]:
                continue
            if vert in current_group:
                continue

            connected_edges = get_connected_edges(vert)

            boundary_edges = []
            for e in connected_edges:
                info = cmds.polyInfo(e, ef=True)
                face_indices = info[0].split(":")[1].split()
                if len(face_indices) == 1:
                    boundary_edges.append(e)

            valence = len(boundary_edges)          
            if valence >= 4:                       
                if current_group:
                    current_group.append(vert)
                    all_group.append(current_group)
                current_group = [vert]
            else:
                current_group.append(vert)         

        next_edge, _ = get_adjacent_boundry_edge(current_edge, visited_edges)

        if next_edge is None or next_edge == start_edge:
            break

        current_edge = next_edge

    return all_group


def group_verts_to_edges(vert_group):
    """Finds the boundary edges that connect consecutive verts in a group."""
    edges = []
    mesh = vert_group[0].split(".")[0]

    for i in range(len(vert_group) - 1):
        vert_a = vert_group[i]
        vert_b = vert_group[i + 1]

        # Get edges connected to both verts — the shared one is our edge
        edges_a = set(get_connected_edges(vert_a))
        edges_b = set(get_connected_edges(vert_b))
        shared = edges_a.intersection(edges_b)

        if shared:
            edges.append(shared.pop())

    return edges


def edges_to_curves(vert_groups):
    curves = []
    for group in vert_groups:
        if len(group) < 2:
            continue

        edges = group_verts_to_edges(group)
        if not edges:
            continue

        # Convert each edge to its own curve, then attach them all together
        segment_curves = []
        for edge in edges:
            result = cmds.polyToCurve(edge, form=2, degree=1)
            segment_curves.append(result[0])

        if len(segment_curves) == 1:
            curves.append(segment_curves[0])
        else:
            # Attach all segments into one curve for this side
            attached = segment_curves[0]
            for i in range(1, len(segment_curves)):
                attached = cmds.attachCurve(attached, segment_curves[i],
                                            constructionHistory=False,
                                            keepMultipleKnots=False)[0]
            curves.append(attached)

    return curves


def main():
    selected_edges = cmds.ls(selection=True, flatten=True)
    selected_object = selected_edges[0].split('.')[0]

    edge_list = group_edge_by_corner()
    print(edge_list)
    # curves_list = edges_to_curves(edge_list)

    # quad_filled_obj = 
    # cmds.boundary(curves_list[0], curves_list[1], curves_list[2], curves_list[3])

    # combined_obj = cmds.polyUnite(selected_object, quad_filled_obj, name=selected_object[0])
    # cmds.delete(combined_obj, ch=True)

if __name__ == "__main__":
    main()