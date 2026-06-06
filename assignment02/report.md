# Assignment 02 Report

## Spatial Intelligence Through Graph Analysis

**Course:** Graph Machine Learning  
**Assignment:** Homework 02, Spatial Intelligence Part 1  
**Date:** 6 June 2026

## Abstract

This assignment investigates an architectural floor plan as a graph-based
spatial system. A simplified OBJ outline is imported into TopologicPy,
discretised with a regular grid, sliced into 250 topological cells, and
converted into graphs representing spatial adjacency. Three analyses are then
performed: shortest-path routing, closeness centrality, and betweenness
centrality. The results identify the long internal corridor as the dominant
circulation spine. Its central section is both the most globally integrated
part of the plan and the part through which the greatest number of shortest
routes pass. A grid-derived route of 24.84 units is reduced to 22.12 units
after geometric straightening, a reduction of 2.72 units or approximately
10.95%. The study demonstrates how graph analysis can reveal spatial
accessibility, hierarchy, and bottlenecks from architectural geometry.

## 1. Introduction

Architectural plans contain both geometric and relational information.
Geometry describes the size and shape of spaces, while topology describes
which spaces are connected and how movement can occur between them. Graph
analysis provides a useful abstraction for studying the second type of
information. Navigable regions can be represented as vertices, adjacency as
edges, and movement through the building as paths through the resulting graph.

The aim of this assignment is to construct a graph from a residential
floor-plan outline and use it to answer three spatial questions:

1. What route connects two selected points through the accessible plan?
2. Which regions are most accessible from all other regions?
3. Which regions function as necessary passages between other regions?

These questions are addressed through shortest-path analysis, closeness
centrality, and betweenness centrality.

## 2. Input Data and Tools

The source drawing is a residential plan organised around a long internal
corridor, with repeated dwelling units on both sides and a lobby and vertical
circulation zone toward the western end. The analysis uses `plan_5.obj`, a
simplified accessible outline derived from the detailed drawing. Simplification
is important because the analysis requires a clean, closed face rather than
every line and annotation in the architectural drawing.

The implementation uses Python and TopologicPy. Key classes include `Topology`
for importing and querying geometry, `Grid` for discretisation, `Graph` for
topological conversion and network analysis, and `Wire` for route geometry.
The recorded notebook run used TopologicPy 0.9.20 and requires version 0.9.18
or newer.

![Source architectural floor plan](image/floor%20plan.png)

*Figure 1. Source residential floor plan used to derive the simplified
analysis boundary.*

## 3. Methodology

### 3.1 Geometry Import and Validation

The OBJ file is loaded with `Topology.ByOBJPath`. The imported object is
searched first for a face and then for a wire that can be converted into a
face. This produces one valid floor face. Its bounding rectangle has the
following recorded dimensions:

- x extent: 1.0 to 24.3 units
- y extent: 0.1 to 7.9 units
- width: 23.3 units
- length: 7.8 units

![Simplified floor outline](image/image%20%282%29.png)

*Figure 2. Simplified closed floor face imported from `plan_5.obj`.*

### 3.2 Grid Discretisation

A regular grid with a spacing of 1 model unit is clipped to the floor face.
The floor is then sliced by the grid using `Topology.Slice`. Each resulting
face receives a unique `face_id`, which is later used to transfer graph
analysis values back to the corresponding spatial cell.

The operation generates 250 cells. This transforms continuous floor geometry
into a finite set of comparable spatial units.

![Grid overlay](image/image%20%283%29.png)

*Figure 3. One-unit grid clipped to the accessible floor outline.*

![Topological shell](image/image%20%284%29.png)

*Figure 4. Topological shell produced by slicing the floor face with the grid.*

### 3.3 Graph Construction

Two graphs are derived from the shell:

- A navigation graph is generated with shared-topology connections enabled.
  It is used for route finding.
- An analysis graph is generated from the shell and used for centrality
  calculations.

Graph vertices represent the discretised spatial cells, while graph edges
represent traversable adjacency between cells. The graph therefore preserves
the relational organisation of the plan while reducing its geometric
complexity.

![Analysis graph](image/image%20%285%29.png)

*Figure 5. Analysis graph showing cell centres as vertices and adjacency as
edges.*

### 3.4 Shortest-Path Analysis

The start point is placed near the upper-western side of the plan and the end
point near the lower-eastern side. A compiled routing graph is created and
TopologicPy computes a shortest path between the endpoints. Because the graph
follows discretised cells, the original route contains small zig-zag
deviations. `Wire.Straighten` is then used to produce a shorter route that
remains constrained by the floor face.

### 3.5 Centrality Analysis

Closeness centrality measures how near each graph vertex is to all other
vertices through shortest-path distance. High closeness indicates strong
global accessibility. In space syntax terminology, this is interpreted as
integration.

Betweenness centrality measures the proportion of shortest paths between other
vertex pairs that pass through a given vertex. High betweenness indicates that
a location is important for through-movement. In space syntax this is related
to choice.

Computed values are stored in the graph-vertex dictionaries and transferred
back to cells using `face_id`, allowing the metrics to be visualised as
continuous spatial heat maps.

## 4. Results

### 4.1 Quantitative Summary

| Measure | Recorded result |
|---|---:|
| Imported OBJ objects | 1 |
| Floor dimensions | 23.3 x 7.8 units |
| Grid spacing | 1 unit |
| Topological cells | 250 |
| Shortest-path computation time | 0.15 s |
| Route-straightening time | 0.96 s |
| Original grid path | 24.84 units |
| Straightened path | 22.12 units |
| Absolute reduction | 2.72 units |
| Relative reduction | 10.95% |

The straightened route is approximately 10.95% shorter than the original
grid-derived route. This difference quantifies part of the discretisation
effect: movement constrained to graph transitions is less geometrically
efficient than movement represented by a continuous line within the same
boundary.

![Shortest route comparison](image/image%20%286%29.png)

*Figure 6. Grid-derived shortest path in red and straightened path in blue.*

### 4.2 Closeness Centrality

The closeness map shows its highest values around the middle of the main
corridor. Values decrease toward both ends of the building and into the deeper
parts of individual dwelling bays. This pattern is consistent with the
elongated geometry: central corridor cells minimise the total network distance
to the largest number of other cells.

The result suggests that the central corridor is the most globally integrated
location. From a design perspective, this area is well suited to shared
wayfinding information or common functions because it can be reached with
relatively few graph steps from the rest of the plan.

![Closeness centrality](image/image%20%287%29.png)

*Figure 7. Closeness centrality heat map. Brighter central cells have stronger
global integration.*

### 4.3 Betweenness Centrality

The betweenness map concentrates high values along the main corridor,
especially around its central segment. Peripheral cells have low values
because they tend to be origins or destinations rather than necessary
intermediate locations.

This result identifies a clear movement bottleneck. Routes between western and
eastern areas, and between many opposing dwelling bays, must use the corridor.
Consequently, disruption or congestion in this zone would affect a large
proportion of potential journeys. The finding is relevant to circulation
capacity, emergency egress, and the placement of obstacles or shared
facilities.

![Betweenness centrality](image/image%20%288%29.png)

*Figure 8. Betweenness centrality heat map. The corridor carries most
cross-plan shortest routes.*

## 5. Discussion

The three analyses describe complementary properties of the same spatial
system. Shortest-path analysis evaluates one selected journey. Closeness
centrality evaluates how efficiently each cell can reach the complete graph.
Betweenness centrality evaluates how strongly each cell mediates journeys
between all other pairs.

Together, the results reveal a strongly corridor-dominated topology. The
repeated residential bays create local branches, while the horizontal corridor
provides the only continuous east-west connection. This explains why central
corridor cells score highly in both centrality measures. They are close to much
of the graph and are also unavoidable for many cross-plan routes.

The western entrance and lobby area has lower global centrality than the middle
of the corridor. Although it is functionally important as an entry, its
position at one end of an elongated graph increases its average distance to
eastern cells. This distinction shows that functional importance and
topological centrality are related but not identical.

## 6. Limitations

First, the model depends on a 1-unit grid. A finer grid would represent
boundaries and diagonal movement more accurately but would increase graph size
and centrality computation time. A coarser grid would be faster but could
remove narrow connections or exaggerate path error.

Second, the simplified floor face does not encode doors, room functions,
occupancy, accessibility constraints, capacities, or direction-dependent
costs. All graph connections are effectively treated as equally traversable.
The analysis is therefore topological rather than a complete simulation of
human movement.

Third, the route endpoints are manually chosen, so the path result represents
one scenario rather than all origin-destination demands. Finally, the notebook
visualises centrality comparatively but does not export a table of exact
per-cell values, limiting detailed statistical comparison.

## 7. Future Work

The analysis could be extended by:

1. comparing several grid resolutions to test result stability;
2. modelling doors and restricted areas explicitly;
3. assigning weighted edges based on distance, width, or travel cost;
4. testing multiple origin-destination pairs and occupancy scenarios;
5. exporting cell-level metrics for statistical analysis; and
6. comparing graph predictions with observed pedestrian movement.

## 8. Conclusion

This assignment demonstrates a complete geometry-to-graph workflow for
architectural spatial analysis. A simplified residential floor plan was
discretised into 250 cells and converted into navigation and analysis graphs.
The shortest-path experiment showed that geometric straightening reduced the
grid route from 24.84 to 22.12 units. Closeness and betweenness centrality both
identified the internal corridor, particularly its middle section, as the
plan's principal spatial structure.

The analysis confirms that graph methods can expose accessibility, hierarchy,
and bottlenecks that are not captured by geometric dimensions alone. Even with
a simplified model, the results provide interpretable evidence about how the
building supports movement and where its circulation network is most critical.

## References

1. Hillier, B., and Hanson, J. (1984). *The Social Logic of Space*. Cambridge
   University Press.
2. TopologicPy documentation. <https://topologicpy.readthedocs.io/>
3. NetworkX documentation, centrality algorithms.
   <https://networkx.org/documentation/stable/reference/algorithms/centrality.html>
