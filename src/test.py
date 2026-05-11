import maya.cmds as cmds

cmds.selectPref(isp=False, trackSelectionOrder=True)
verts = cmds.ls(orderedSelection=True)
verts = cmds.ls(verts, flatten=True)


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
print(edges_group)


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



import maya.cmds as cmds
# Select objects and combine
objects = cmds.ls(['pCube2', 'pCube2_fill'], selection=True)
combined_mesh = cmds.polyUnite(objects)
# Clean up history to finalize the mesh
cmds.delete(combined_mesh, ch=True)



# Example: Get edges connected to one of the vertices of an edge
edges = cmds.ls(selection=True, flatten=True)
# connected_edges = cmds.polyInfo(vertex, ve=True)
result = cmds.polyToCurve(edges, form=2, degree=1)
cmds.ls(result, selection=True, flatten=True)