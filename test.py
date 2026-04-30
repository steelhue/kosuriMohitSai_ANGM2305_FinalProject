import maya.cmds as cmds


# Example: Get edges connected to one of the vertices of an edge
edges = cmds.ls(selection=True, flatten=True)
# connected_edges = cmds.polyInfo(vertex, ve=True)
result = cmds.polyToCurve(edges, form=2, degree=1)
cmds.ls(result, selection=True, flatten=True)