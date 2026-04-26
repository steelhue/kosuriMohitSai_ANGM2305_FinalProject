import maya.cmds as cmds
import math

# group edges based on the angle
        # To do this, we need to get the vector of each edge and 
        # compare it to the next connected egde
    # if the edge is >= 90 to the other edge, group the edges
# convert the grouped edges to curves
# using the boundry tool, select the edges and make the mesh
# combine the meshes and apply merge by distance

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


def get_dot_product(vec_a, vec_b):
    return sum(vec_a[0] * vec_b[0], vec_a[1] * vec_b[1], vec_a[2] * vec_b[2])


def get_connecting_edge_count(vertex):
    info = cmds.polyInfo(vertex, vertexToEdge=True)
    connected_edges = info.split()
    return len(connected_edges)


def get_adjaent_edge(edge, selected_edges):
    # verts = cmds.polyListComponentConversion(selected_edges[idx], toVertex=True)
    # verts = cmds.ls(verts, flatten=True)

    # check if the adjacent edge's verts belongs in the same selection
    # 


    info = cmds.polyInfo(edge, edgeToEdge=True)
    connected_edges = info.split()[2:] # connected edges set

    obj_name = edge.split('.')[0] # returns object name
    all_neighbors = []

    for i in connected_edges:
        all_neighbors.append(f"{obj_name}.e{i}")

    selection_set = set(selected_edges)

    adjacent_selection = []

    for edge in all_neighbors:
        if edge in selection_set:
            adjacent_selection.append[edge] # has edges from all directions



def selected_edges_to_groups():

    selected_edges = cmds.ls(selection=True, flatten=True)

    edge_groups = [[selected_edges[0]]]
    current_group = 0

    for idx in range(len(selected_edges) - 1):
        vec_a = get_edge_vector(selected_edges[idx])
        vec_b = get_edge_vector(get_adjaent_edge(selected_edges[idx], selected_edges, idx))

        if is_zero_vector(vec_a) or is_zero_vector(vec_b):
            edge_groups[current_group].append(selected_edges[idx + 1])
            continue

        dot = get_dot_product(vec_a, vec_b)
        dot = max(-1.0, min(1.0, dot))

        angle = math.degrees(math.acos(dot))

        if angle >= 90.0:
            current_group += 1
            # if current_group >= 4:
            #     cmds.warning("More than 4 sides detected. Check your selection.")
            #     break
            edge_groups.append([])
        
        edge_groups[current_group].append(selected_edges[idx + 1])

    return edge_groups


def edges_to_curves(edge_lists):
    # at every index, there is a list so it accesses every list and converts the edges to corves
    curves = []
    for group in range(len(edge_lists)):
        if group:
            result = cmds.polyToCurve(group, form=2, degree=1)
            curves.append(result[0])
    return curves


def main():
    selected_object = cmds.ls(selection=True, objectsOnly=True)

    edge_list = selected_edges_to_groups()
    curves_list = edges_to_curves(edge_list)

    # quad_filled_obj = 
    cmds.boundary(curves_list[0], curves_list[1], curves_list[2], curves_list[3])

    # combined_obj = cmds.polyUnite(selected_object, quad_filled_obj, name=selected_object[0])
    # cmds.delete(combined_obj, ch=True)

if __name__ == "__main__":
    main()