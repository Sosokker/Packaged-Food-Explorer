import sqlite3
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx
import plotly.graph_objects as go
import os.path

current_dir = os.path.dirname(os.path.abspath(__file__))
db_path = (current_dir + r"\data\food_data.db")

conn = sqlite3.connect(db_path)
query = "SELECT * FROM food_data LIMIT 100"
df = pd.read_sql_query(query, conn)

df= df.fillna(0)

nutrient_columns = [
    'energy-kcal_100g', 'fat_100g', 'saturated-fat_100g', 'unsaturated-fat_100g',
    'omega-3-fat_100g', 'omega-6-fat_100g', 'omega-9-fat_100g', 'trans-fat_100g',
    'cholesterol_100g', 'carbohydrates_100g', 'sugars_100g', 'sucrose_100g',
    'glucose_100g', 'fructose_100g', 'lactose_100g', 'maltose_100g', 'fiber_100g',
    'soluble-fiber_100g', 'insoluble-fiber_100g', 'proteins_100g', 'salt_100g',
    'added-salt_100g', 'sodium_100g', 'alcohol_100g', 'vitamin-a_100g',
    'beta-carotene_100g', 'vitamin-d_100g', 'vitamin-e_100g', 'vitamin-k_100g',
    'vitamin-c_100g', 'vitamin-b1_100g', 'vitamin-b2_100g', 'vitamin-pp_100g',
    'vitamin-b6_100g', 'vitamin-b9_100g', 'vitamin-b12_100g', 'bicarbonate_100g',
    'potassium_100g', 'chloride_100g', 'calcium_100g', 'phosphorus_100g', 'iron_100g',
    'magnesium_100g', 'zinc_100g', 'copper_100g', 'manganese_100g', 'fluoride_100g',
    'selenium_100g', 'chromium_100g', 'molybdenum_100g', 'iodine_100g',
    'caffeine_100g', 'cocoa_100g', 'carbon-footprint_100g'
]

conn.close()
chunk_size = 1000  

similarity_df = pd.DataFrame(index=df['product_name'], columns=df['product_name'])
for i in range(0, len(df), chunk_size):
    chunk = df.iloc[i:i+chunk_size]
    chunk_similarity_matrix = cosine_similarity(chunk[nutrient_columns])

    chunk_similarity_df = pd.DataFrame(chunk_similarity_matrix, index=chunk['product_name'], columns=chunk['product_name'])
    similarity_df.update(chunk_similarity_df)
similarity_df = similarity_df.fillna(1.0)

# * Similarities calculate by cosine similarities

graph = nx.from_pandas_adjacency(similarity_df)
node_degrees = graph.degree()
sorted_nodes = sorted(node_degrees, key=lambda x: x[1], reverse=True)
top_nodes = [node[0] for node in sorted_nodes[:10]]
subgraph = graph.subgraph(top_nodes)
pos = nx.spring_layout(subgraph)
x, y = zip(*pos.values())
edge_trace = go.Scatter(
    x=[],
    y=[],
    line=dict(width=0.5, color='#888'),
    hoverinfo='none',
    mode='lines')

for edge in subgraph.edges():
    x0, y0 = pos[edge[0]]
    x1, y1 = pos[edge[1]]
    edge_trace['x'] += tuple([x0, x1, None])
    edge_trace['y'] += tuple([y0, y1, None])

node_trace = go.Scatter(
    x=x,
    y=y,
    mode='markers+text',
    hoverinfo='text',
    text=list(subgraph.nodes()),
    textposition='top center',
    marker=dict(
        showscale=False,
        color='rgb(150,150,150)',
        size=10,
        line=dict(width=2, color='rgb(255,255,255)')))

layout = go.Layout(
    showlegend=False,
    hovermode='closest',
    margin=dict(b=20, l=5, r=5, t=40),
    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))

fig = go.Figure(data=[edge_trace, node_trace], layout=layout)
fig.show()


# ! Shortest Path

G = nx.Graph()
G.add_nodes_from(df['product_name'])

# ! Add edges to the graph with weight as the modified similarity score(Reverse similarities score)
for i in range(len(similarity_df)):
    for j in range(i+1, len(similarity_df)):
        if similarity_df.iloc[i,j] > 0:
            similarity_score = similarity_df.iloc[i,j]
            similarity_weight = 1 - similarity_score
            G.add_edge(similarity_df.index[i], similarity_df.columns[j], weight=similarity_weight)

# * Example
start_node = 'Cheese twist'
end_node = 'Pepperidge farm cookies'
shortest_path = nx.shortest_path(G, start_node, end_node, weight='weight')

print(shortest_path)