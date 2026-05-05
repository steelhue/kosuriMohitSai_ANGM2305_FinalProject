import maya.cmds as cmds

verts = cmds.ls(selection=True, flatten=True)

print(verts)
vert_indices = []
for vert in verts:
    vert_indices.append(vert.split(".")[1][4])

vert_A = vert_indices[0]
vert_B = vert_indices[1]
vert_C = vert_indices[2]
vert_D = vert_indices[3]

print(int(vert_A))
print(int(vert_B))
print(int(vert_C))
print(int(vert_D))

side_a = cmds.polySelect("pCube1", shortestEdgePath=(vert_A, vert_B))
side_b = cmds.polySelect("pCube1", shortestEdgePath=(vert_B, vert_C))
side_c = cmds.polySelect("pCube1", shortestEdgePath=(vert_C, vert_D))
side_d = cmds.polySelect("pCube1", shortestEdgePath=(vert_D, vert_A))

cmds.ls(side_a, selection=True, flatten=True)
cmds.ls(side_b, selection=True, flatten=True)
cmds.ls(side_c, selection=True, flatten=True)
cmds.ls(side_d, selection=True, flatten=True)

cmds.ls(verts, cl=True)



# Example: Get edges connected to one of the vertices of an edge
edges = cmds.ls(selection=True, flatten=True)
# connected_edges = cmds.polyInfo(vertex, ve=True)
result = cmds.polyToCurve(edges, form=2, degree=1)
cmds.ls(result, selection=True, flatten=True)