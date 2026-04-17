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
    verts = cmds.ls(verts, flatter=True)

    p = cmds.xform(verts[0], q=True, ws=True, t=True)
    q = cmds.xform(verts[1], q=True, ws=True, t=True)

    vector = (q[0] - p[0], q[1] - p[1], q[2] - p[2])
    return vector


def selected_edges_to_groups():
    selected_edges = cmds.ls(selection=True, flatten=True)

    edge_list = []

    idx = 0
    list_idx = 0
    while not idx >= len(selected_edges):
        angle_between_edges = cmds.angleBetween(get_edge_vector(selected_edges[idx]), get_edge_vector(selected_edges[idx + 1]))
        if list_idx >= 4:
            list_idx = 0
        
        if not angle_between_edges[3] >= 90.0:
            edge_list[list_idx].append(selected_edges[idx])
            edge_list[list_idx].append(selected_edges[idx + 1]) # creates another list in the index
        else:
            list_idx += 1 
    return edge_list


def edges_to_curves(edge_lists):
    # at every index, there is a list so it accesses every list and converts the edges to corves
    curves = []
    for i in range(len(edge_lists)):
        curves[i].appned(cmds.polyToCurve(edge_lists[i], degree=1))  
    return curves


def main():
    edge_list = selected_edges_to_groups()
    curves_list = edges_to_curves(edge_list)

    cmds.boundry(curves_list[0], curves_list[1], curves_list[2], curves_list[3])


if __name__ == "__main__":
    main()