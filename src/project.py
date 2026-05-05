import maya.cmds as cmds


def get_edge_verts(edge):
    mesh = edge.split(".")[0]
    info = cmds.polyInfo(edge, ev=True)
    vert_indices = info[0].split(":")[1].split()
    vert_indices = [idx for idx in vert_indices if idx.isdigit()]
    return [f"{mesh}.vtx[{idx}]" for idx in vert_indices]


def get_connected_edges(vertex):
    mesh = vertex.split(".")[0]
    info = cmds.polyInfo(vertex, ve=True)
    edge_indices = info[0].split(":")[1].split()
    # Filter out non-numeric tokens like 'Hard' or 'Soft'
    edge_indices = [idx for idx in edge_indices if idx.isdigit()]
    return [f"{mesh}.e[{idx}]" for idx in edge_indices]



def group_edges_by_corner(current_edge, visited_edges):
    
    verts = get_edge_verts(current_edge)
    vert_idx = 0

    current_vert = verts[vert_idx]
    verts_grp = []
    corner_vert_count = 0

    connecting_edges = cmds.polyInfo(current_vert, ve=True)
    edge_count = len(connecting_edges)

    while not corner_vert_count == 2 and vert_idx <= 2:
        if edge_count >= 4:
            verts_grp.add(current_vert)
            corner_vert_count+=1
            vert_idx+=1

        verts_grp.add(current_vert)
        vert_idx+=1
    
    current_vert = verts[1]

    for edge in connecting_edges:
        if edge == current_edge:
            visited_edges.add(edge)
        if edge in visited_edges:
            continue
            

# def get_adjacent_boundary_edge(current_edge, visited_edges):
#     """
#     Given the current edge, finds the next unvisited boundary edge
#     by checking edges connected to its vertices.
#     """
#     verts = get_edge_verts(current_edge)

#     for vert in verts:
#         connected_edges = get_connected_edges(vert)

#         for edge in connected_edges:
#             if edge == current_edge:
#                 continue
#             if edge in visited_edges:
#                 continue

#             # Only follow boundary edges (1 face connection)
#             info = cmds.polyInfo(edge, ef=True)
#             face_indices = info[0].split(":")[1].split()
#             if len(face_indices) == 1:
#                 return edge, vert

#     return None, None


# def group_edges_by_corner():
#     """
#     Walks the boundary loop and groups vertices into 4 sides.
#     A new group starts whenever a corner vertex is detected (valence >= 4
#     boundary edges meaning it's where two sides of the hole meet).
#     """
#     selected = cmds.ls(selection=True, flatten=True)
#     if not selected:
#         cmds.warning("No Edges Selected")
#         return []

#     start_edge = selected[0]

#     all_groups = []
#     current_group = []
#     visited_edges = set()
#     current_edge = start_edge

#     while True:
#         visited_edges.add(current_edge)
#         verts = get_edge_verts(current_edge)

#         for vert in verts:
#             # Skip if already placed in a completed group
#             if vert in [v for group in all_groups for v in group]:
#                 continue
#             # Skip if already in the current group
#             if vert in current_group:
#                 continue

#             connected_edges = get_connected_edges(vert)

#             # Filter down to boundary edges only (1 face connection)
#             boundary_edges = []
#             for e in connected_edges:
#                 info = cmds.polyInfo(e, ef=True)
#                 face_indices = info[0].split(":")[1].split()
#                 if len(face_indices) == 1:
#                     boundary_edges.append(e)

#             valence = len(boundary_edges)

#             if valence >= 2:
#                 # Corner vertex — close current group and start a new one
#                 if current_group:
#                     current_group.append(vert)
#                     all_groups.append(current_group)
#                 current_group = [vert]
#             else:
#                 current_group.append(vert)

#         next_edge, _ = get_adjacent_boundary_edge(current_edge, visited_edges)

#         if next_edge is None or next_edge == start_edge:
#             break

#         current_edge = next_edge

#     if len(all_groups) != 4:
#         cmds.warning(f"Expected 4 edge groups, got {len(all_groups)}. Check your selection.")

#     return all_groups


def group_verts_to_edges(vert_group):
    """
    Converts a group of vertices into the boundary edges that connect them
    by finding the shared edge between each consecutive pair of vertices.
    """
    edges = []

    for i in range(len(vert_group) - 1):
        edges_a = set(get_connected_edges(vert_group[i]))
        edges_b = set(get_connected_edges(vert_group[i + 1]))
        shared = edges_a.intersection(edges_b)

        if shared:
            edges.append(shared.pop())

    return edges


def edges_to_curves(vert_groups):
    """
    Converts each vertex group into a single curve by:
    1. Rebuilding the edge list from consecutive vertex pairs
    2. Converting each edge to its own curve segment
    3. Attaching all segments into one curve per side
    """
    curves = []

    for group in vert_groups:
        if len(group) < 2:
            continue

        edges = group_verts_to_edges(group)
        if not edges:
            continue

        # Convert each edge individually to a curve segment
        segments = []
        for edge in edges:
            result = cmds.polyToCurve(edge, form=2, degree=1)
            segments.append(result[0])

        # Attach all segments into one curve for this side
        if len(segments) == 1:
            curves.append(segments[0])
        else:
            attached = segments[0]
            for i in range(1, len(segments)):
                attached = cmds.attachCurve(attached, segments[i],
                                            constructionHistory=False,
                                            keepMultipleKnots=False)[0]
            curves.append(attached)

    return curves


def main():
    selected_edges = cmds.ls(selection=True, flatten=True)
    if not selected_edges:
        cmds.warning("No edges selected.")
        return

    selected_object = selected_edges[0].split('.')[0]

    starting_edge = selected_edges[0]

    # Step 1: Group boundary vertices into 4 sides
    vert_groups = group_edges_by_corner()
    print("Vertex groups:", vert_groups)

    # if len(vert_groups) != 4:
    #     cmds.error("Could not resolve 4 sides. Aborting.")
    #     return

    # # Step 2: Convert each side into a curve
    # curves = edges_to_curves(vert_groups)
    # print("Curves:", curves)

    # if len(curves) != 4:
    #     cmds.error("Curve generation failed. Aborting.")
    #     return

    # # Step 3: Fill the hole using the boundary tool
    # patch = cmds.boundary(curves[0], curves[1], curves[2], curves[3],
    #                       constructionHistory=False)

    # # Step 4: Convert the NURBS patch to a polygon mesh
    # poly_patch = cmds.nurbsToPoly(patch, constructionHistory=False,
    #                                type=1, format=2, uType=3, vType=3)

    # # Step 5: Merge the patch back into the original mesh
    # combined = cmds.polyUnite(selected_object, poly_patch[0],
    #                            constructionHistory=False)
    # cmds.polyMergeVertex(combined[0], distance=0.001,
    #                       constructionHistory=False)

    # # Step 6: Clean up the curves
    # cmds.delete(curves)

    # print("Quad fill complete!")


if __name__ == "__main__":
    main()