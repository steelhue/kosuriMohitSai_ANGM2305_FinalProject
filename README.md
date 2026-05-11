# Quad-Fill Tool V.1

A Maya Python tool that automatically fills 4-sided holes in polygon meshes with quad geometry using boundary curve generation.

---

## Requirements

- Autodesk Maya (2023+)
- Python 3 (included with Maya)

---

## Usage

### Auto Fill
The fully automated workflow.

1. Select the mesh hole you want to fill
2. Switch to **Vertex** component mode
3. Select exactly **4 corner vertices** — one at each corner of the hole
4. Open the tool and click **Quad Fill**

The tool will automatically group the boundary edges into 4 sides, convert them to curves, generate a quad patch, and merge it back into the original mesh.

### Manual Fill (Coming in V.2)
A two-step workflow that lets you inspect and adjust the boundary curves before filling.

1. Select 4 corner vertices → click **Generate Curves**
2. Inspect and tweak the generated curves in the viewport
3. Select all 4 curves → click **Fill**

---

## How It Works

### 1. Vertex Sorting — `sort_verts_clockwise`
The 4 selected corner vertices are sorted spatially in clockwise order using their world positions. This ensures consistent edge path traversal regardless of the order the user clicks them.

The angle of each vertex relative to the center point of all 4 vertices is calculated using `atan2`, then sorted accordingly.

### 2. Edge Grouping — `group_edges_by_corner`
Using Maya's `polySelect` with the `shortestEdgePath` flag, the tool finds the shortest edge path between each consecutive pair of corner vertices, producing 4 ordered edge groups — one per side of the hole.

### 3. Edge to Curve Conversion — `edges_to_curves`
Each edge group is selected and converted into a degree-1 (linear) NURBS curve using `polyToCurve`. This gives 4 curves that trace the boundary of the hole.

### 4. Boundary Fill — `cmds.boundary`
The 4 curves are passed into Maya's `boundary` command which generates a NURBS surface patch that spans the hole.

### 5. NURBS to Polygon — `cmds.nurbsToPoly`
The NURBS patch is converted to a polygon mesh using Control Points tessellation, which ensures the patch vertices line up with the boundary curve endpoints for clean merging.

### 6. Merge — `cmds.polyUnite` + `cmds.polyMergeVertex`
The patch is united with the original mesh and border vertices are welded together using a merge distance of `0.001`. Construction history is deleted and normals are conformed.

---

## Author
Mohit Sai Kosuri
ANGM 2305 — Final Project