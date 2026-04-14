# Grid Fill Tool for Maya

## Repository
https://github.com/steelhue/KosuriMohitSai_ANGM2305_FinalProject.git

## Description
This is a modeling tool for Maya that automatically generates quads geometry across open edges while respecting the surrounding surface flow. It eliminates manual retopology by allowing artists to close curvy and complex gaps with with ease.

## Feature
- Edge loop Detection: The tool must identify the selected open edge border and group the adjacent edges into separate groups
- Edge-to-curve conversion: The selected edge loops will be convereted to 4 seperate curves, with a degree of 1, each adjacent to one another
- Grid Tolopogy Generation: Using the 'Boundry' tool, it uses the 'Polygon Output' geometry setting with 'Quads' type, with 'Control Points' to generate a mesh with quads
- Mesh merge: Since the grid topology generation method creates an individual mesh that is not part of the original object so it merges the newly created mesh to the actual object

## Challenges
- Learning Maya's python library and testing out basic functions through code
- Integrating VS Code with Maya with real-time changes in Maya when code in run in VS code

## Outcomes
- Ideal Outcome: A fully integrated Maya Python tool with a simple UI that allows users to select a hole and instantly generate a curvature-matched quad grid with adjustable "span" and "offset" settings.

- Minimal Viable Outcome: A functional script that automates the "Edges $\rightarrow$ Curves $\rightarrow$ Boundary $\rightarrow$ Mesh Merge" workflow, allowing for a single-click quad fill on a 4-sided boundary loop.

## Milestones
- Week 1:
    1. Write the logic to detect the boundary loop and sort edges into four distinct groups (sides).

    2. Automate the conversion of these edge groups into 1-degree curves.

    2. Ensure the script can identify if the selection is a valid closed loop before proceeding.

- Week 2:
    1. Script the maya.cmds.boundary command using your four curves, ensuring the output is set to Type: Quads.

    2. Automate the polyUnite and polyMergeVertex commands to sew the new patch back into the original mesh seamlessly.

    3. Implement a "Delete History" step on the new patch to prevent the curves from cluttering the Outliner.

- Week 3:
    1. UI Build: Create a floating window.

    2. Refinement: Add a "Reverse Curve" toggle in case the boundary generation creates a flipped or twisted mesh.