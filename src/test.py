import maya.cmds as cmds

verts = cmds.ls(selection=True, flatten=True)

print(verts)

vert_indices = []
edge_groups = []

mesh_name = verts[0].split(".")[0]
print(mesh_name)

for vert in verts:
    idx = vert.split(".")[1]
    idx = idx.replace("vtx[", "").replace("]", "")
    vert_indices.append(idx)

vert_A = vert_indices[0]
vert_B = vert_indices[1]
vert_C = vert_indices[2]
vert_D = vert_indices[3]

side_a = cmds.polySelect(mesh_name, shortestEdgePath=[int(vert_A), int(vert_B)])
edge_groups.append(side_a)

side_b = cmds.polySelect(mesh_name, shortestEdgePath=[int(vert_B), int(vert_C)])
edge_groups.append(side_b)

side_c = cmds.polySelect(mesh_name, shortestEdgePath=[int(vert_C), int(vert_D)])
edge_groups.append(side_c)

side_d = cmds.polySelect(mesh_name, shortestEdgePath=[int(vert_D), int(vert_A)])
edge_groups.append(side_d)


import maya.cmds as cmds

edges_group = cmds.ls(selection=True, flatten=True)
curves_group = []
for edges in edges_group:
    curves = []
    curves.append(cmds.polyToCurve(edges, form=2, degree=1))
print(curves)

import maya.cmds as cmds

curves = cmds.ls(selection=True, flatten=True)
attached_curve = cmds.attachCurve(curves[0:], kmk=False, ch=False)
curves_group.append(attached_curve)
objects_to_remove = curves[1:]
cmds.delete(objects_to_remove)



# Example: Get edges connected to one of the vertices of an edge
edges = cmds.ls(selection=True, flatten=True)
# connected_edges = cmds.polyInfo(vertex, ve=True)
result = cmds.polyToCurve(edges, form=2, degree=1)
cmds.ls(result, selection=True, flatten=True)