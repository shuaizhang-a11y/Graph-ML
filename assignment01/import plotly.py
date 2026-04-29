import plotly.graph_objects as go
import networkx as nx
import numpy as np

# 生成一个简单的3D网络
G = nx.random_geometric_graph(10, 0.5, dim=3)
pos = nx.get_node_attributes(G, 'pos')

# 节点坐标
Xn = [pos[k][0] for k in G.nodes()]
Yn = [pos[k][1] for k in G.nodes()]
Zn = [pos[k][2] for k in G.nodes()]

# 边坐标
Xe = []
Ye = []
Ze = []
for e in G.edges():
    Xe += [pos[e[0]][0], pos[e[1]][0], None]
    Ye += [pos[e[0]][1], pos[e[1]][1], None]
    Ze += [pos[e[0]][2], pos[e[1]][2], None]

# 绘制房间（长方体）
def draw_box(x, y, z, dx, dy, dz, color='rgba(0,200,255,0.1)'):
    # 8个顶点
    corners = np.array([
        [x, y, z],
        [x+dx, y, z],
        [x+dx, y+dy, z],
        [x, y+dy, z],
        [x, y, z+dz],
        [x+dx, y, z+dz],
        [x+dx, y+dy, z+dz],
        [x, y+dy, z+dz]
    ])
    # 12条边
    lines = [
        [0,1],[1,2],[2,3],[3,0],
        [4,5],[5,6],[6,7],[7,4],
        [0,4],[1,5],[2,6],[3,7]
    ]
    box_traces = []
    for line in lines:
        box_traces.append(go.Scatter3d(
            x=[corners[line[0],0], corners[line[1],0]],
            y=[corners[line[0],1], corners[line[1],1]],
            z=[corners[line[0],2], corners[line[1],2]],
            mode='lines',
            line=dict(color=color, width=2),
            showlegend=False
        ))
    return box_traces

fig = go.Figure()

# 添加房间
for room in [
    (0,0,0,1,2,1), # (x, y, z, dx, dy, dz)
    (1,1.5,0,1,1,1)
]:
    for trace in draw_box(*room):
        fig.add_trace(trace)

# 添加边
fig.add_trace(go.Scatter3d(x=Xe, y=Ye, z=Ze, mode='lines', line=dict(color='cyan', width=2), showlegend=False))

# 添加节点
fig.add_trace(go.Scatter3d(x=Xn, y=Yn, z=Zn, mode='markers',
    marker=dict(symbol='circle', size=10, color='blue', opacity=0.8),
    showlegend=False))

fig.update_layout(scene=dict(
    xaxis=dict(visible=False),
    yaxis=dict(visible=False),
    zaxis=dict(visible=False),
), margin=dict(l=0, r=0, b=0, t=0), paper_bgcolor='black', scene_bgcolor='black')

fig.show()