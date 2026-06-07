# Assignment 03: Building Graph Representation

This folder contains the Assignment 03 workflow for converting Rhino OBJ files
into a Building Graph Representation (BGR), exporting CSV datasets, and running
node classification with TopologicPy and PyTorch Geometric.

## Main Files

| Path | Purpose |
|---|---|
| `obj/` | Source Rhino OBJ and MTL files |
| `classfications/S06-13A GML Creating BGR Graph - dan.ipynb` | Builds the BGR graph and exports CSV |
| `classfications/S06-13 Node Classification - DAN.ipynb` | Generates node labels and trains the node classifier |
| `bgr_dataset/` | Original BGR CSV export |
| `bgr_node_dataset/` | Node-classification CSV dataset |
| `bgr_node_model.pt` | Trained node-classification model |
| `topology.png` | Exported coloured topology image |
| `report.md` | Written assignment report |
| `report.pdf` | PDF version of the report |

## Source OBJ Layers

| File | Category |
|---|---|
| `ground.obj` | Ground slab / podium |
| `columns.obj` | Columns |
| `offices.obj` | Office volumes |
| `core.obj` | Core / circulation |

## Generated Dataset Summary

Original BGR dataset:

- Graphs: 1
- Nodes: 55
- Directed edge records: 286

Node classification dataset:

- Ground nodes: 1
- Column nodes: 36
- Office nodes: 17
- Core nodes: 1

The original graph-classification dataset has only one graph, so the machine
learning task was adapted to node classification.

## How to Run

1. Open VS Code from the repository root.
2. Select the `.gmlenv` Python kernel.
3. Run:

   `classfications/S06-13A GML Creating BGR Graph - dan.ipynb`

   This imports OBJ geometry, creates the BGR graph, exports CSV files to
   `bgr_dataset`, and saves `topology.png`.

4. Run:

   `classfications/S06-13 Node Classification - DAN.ipynb`

   This creates `bgr_node_dataset`, trains the node-classification model, and
   saves `bgr_node_model.pt`.

## Notes

The node-classification result is a workflow demonstration. The dataset is
small and imbalanced, especially for ground and core, which each contain only
one node. More buildings or more labelled components would be needed for a
stronger machine-learning evaluation.

