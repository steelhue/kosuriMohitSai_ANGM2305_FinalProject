import maya.cmds as cmds

# Example: Get edges connected to one of the vertices of an edge
vertex = cmds.ls(selection=True, flatten=True)
connected_edges = cmds.polyInfo(vertex, ve=True)
print(connected_edges)


def get_edge_vector(edge):
    # To get the vector of an edge in Maya Python, you must calculate the 
    # difference between the positions of its two endpoints (vertices). 

    # Using concepts of linear algebra, to extract a vector between 2 points:
        # let P and Q be the start and end points of an edge
        # vector PQ = Q - P
    verts = cmds.polyListComponentConversion(edge, toVertex=True)
    verts = cmds.ls(verts, flatten=True)

    p = cmds.xform(verts[0], q=True, ws=True, t=True)
    q = cmds.xform(verts[1], q=True, ws=True, t=True)

    vector = (q[0] - p[0], q[1] - p[1], q[2] - p[2])
    return vector


def is_zero_vector(v):
    return v[0] == 0.0 and v[1] == 0.0 and v[2] == 0.0


def selected_edges_to_groups(corner_angle_threshold=45.0):
    selected_edges = cmds.ls(selection=True, flatten=True)
    print(selected_edges)

    edge_groups = [[selected_edges[0]]]
    current_group = 0

    for idx in range(len(selected_edges) - 1):
        vec_a = get_edge_vector(selected_edges[idx])
        vec_b = get_edge_vector(selected_edges[idx + 1])

        if is_zero_vector(vec_a) or is_zero_vector(vec_b):
            edge_groups[current_group].append(selected_edges[idx + 1])
            continue

        angle_btw = cmds.angleBetween(
            vector1=[vec_a[0], vec_a[1], vec_a[2]],
            vector2=[vec_b[0], vec_b[1], vec_b[2]]
        )

        angle = angle_btw[3]

        if angle >= corner_angle_threshold:
            current_group += 1
            # if current_group >= 4:
            #     cmds.warning("More than 4 sides detected. Check your selection.")
            #     break
            edge_groups.append([])
        
        edge_groups[current_group].append(selected_edges[idx + 1])

    return edge_groups

def main():
    edge_groups = selected_edges_to_groups()
    print(edge_groups)

if __name__ == "__main__":
    main()