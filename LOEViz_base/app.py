from dash import Dash, html, dcc, Input, Output
import dash_cytoscape as cyto
import json
import plotly.express as px
import pandas as pd

from styling import stylesheet
from elements import (
    all_elements,
    nodes,
    nodes_list,
    edges,
    loes,
    loes_list,
    project_data,
)


# APP CAPABILITIES:
# 1. DISPLAY LOE NETWORK
# 2. CLICK TO DISPLAY NODE OBJECTIVE DETAILS
# 3. SELECTIVELY VIEW LOES
# 4. DISPLAY LOES IN A TIMELINE VIEW WHICH ALSO DISPLAYS DEPENDENCIES

app = Dash(__name__)
cyto.load_extra_layouts()


# CREATE MORE COMPLEX APP COMPONENTS

# LOE checklist to select which LOEs to display
loe_checklist = dcc.Checklist(id="loe_checklist", options=loes_list, value=loes_list)

# cytoscape is the network/graph structure for dash
cytoscape = cyto.Cytoscape(
    id="cytoscape",
    layout={"name": "dagre", "rankDir": "TB"},
    style={"width": "100%", "height": "650px"},
    elements=all_elements,
    stylesheet=stylesheet,
)

# figure for the timeline view
fig = px.timeline(
    data_frame=project_data,
    x_start="Start Date",
    x_end="End Date",
    y="ID",
    color="Status",
    color_discrete_map={
        "Overdue": "red",
        "At Risk": "yellow",
        "On Track": "green",
        "Complete": "blue",
    },
    hover_data="Description",
    height=500,
)
fig.add_shape(
    type="line",
    x0=pd.Timestamp.now(),
    y0=-0.5,
    x1=pd.Timestamp.now(),
    y1=len(project_data) + 0.5,
    line=dict(color="black", dash="dashdot", width=3),
)
fig.add_annotation(
    x=pd.Timestamp.now(), y=len(project_data) + 1, text="Today", showarrow=False
)
fig.update_yaxes(autorange="reversed")
for index, row in project_data.iterrows():
    dependency_list = row["Dependencies"]
    if isinstance(dependency_list, str):
        dependencies = dependency_list.split(",")
    else:
        continue
    for dep in dependencies:
        dep_ind = project_data.index[project_data["ID"] == dep].to_list()[0]
        dep_row = project_data.loc[dep_ind]
        fig.add_annotation(
            ax=dep_row["End Date"],
            ay=dep_row["ID"],
            x=max(row["Start Date"], dep_row["End Date"]),
            y=row["ID"],
            xref="x",
            yref="y",
            axref="x",
            ayref="y",
            showarrow=True,
            text="",
            arrowhead=3,
            arrowwidth=1.5,
            arrowcolor="black",
        )
fig.update_layout(
   margin=dict(l=0, r=0, t=100, b=0)
)


# LAYOUT DETERMINES ORGANIZATION OF COMPONENTS ON THE APP

network_view_layout = [
    # menu block for filters, checklist, etc.
    html.Div(id="menu-block", children=[loe_checklist, html.Hr()]),
    # cytoscape block
    html.Div(id="cytoscape-block", children=[cytoscape]),
]

app.layout = html.Div(
    id="app-container",
    children=[
        # content
        html.Div(
            [
                dcc.Tabs(
                    [
                        dcc.Tab(
                            label="Network View",
                            value="network",
                            className="tab",
                            children=network_view_layout,
                        ),
                        dcc.Tab(
                            label="Timeline View",
                            value="timeline",
                            className="tab",
                            children=dcc.Graph(figure=fig),
                        ),
                    ],
                    id="tabs",
                    value="network",
                )
            ],
            id="content",
        ),
        # info block
        html.Div(
            id="info-block",
            children=[
                html.H3("Info"),
                html.P(id="info-panel"),
            ],
        ),
    ],
)


# CALLBACKS MAKE APP INTERACTIVE


# LOE checklist displays nodes in selected LOE, along with dependencies in other LOEs
@app.callback(Output("cytoscape", "elements"), Input("loe_checklist", "value"))
def loe_filter(loe_checklist: list[str]):
    selected_nodes = []
    selected_edges = []

    # loop through all selected loes
    for loe_id in loe_checklist:
        # add loe node
        for loe in loes:
            if loe["data"]["id"] == loe_id:
                selected_nodes.append(loe)

        # loop through all nodes (global)
        for node in nodes:
            # loop through nodes with parent as LOEx
            if node["data"]["parent"] == loe_id:
                # add node to selected elements list
                selected_nodes.append(node)
                node_id = node["data"]["id"]
                # loop through all edges to find which contain LOEx nodes
                for edge in edges:
                    # find edge containing node
                    if node_id in edge["data"].values():
                        # if not already added
                        if edge not in selected_edges:
                            # add edge to selected elements list
                            selected_edges.append(edge)

                            # add nodes outside of LOE that are connected to nodes inside LOE
                            # get id of other node on the edge
                            edge_nodes = list(edge["data"].values())
                            edge_nodes.remove(node_id)
                            addl_node_id = edge_nodes[0]
                            # use id to get node object
                            addl_node = [
                                node
                                for node in nodes
                                if node["data"]["id"] == addl_node_id
                            ]
                            # add loe parent node (allows app to draw edge if node is outside selected LOE)
                            loe_node = [
                                loe
                                for loe in loes
                                if loe["data"]["id"] == addl_node[0]["data"]["parent"]
                            ]
                            # add to selected_nodes
                            selected_nodes = selected_nodes + addl_node + loe_node

    # remove duplicate nodes
    unique_nodes = []
    for node in selected_nodes:
        if node not in unique_nodes:
            unique_nodes.append(node)

    # return selected elements
    return unique_nodes + selected_edges


# display node info when clicked
@app.callback(
    Output("info-panel", "children", allow_duplicate=True),
    Input("cytoscape", "tapNodeData"),
    prevent_initial_call=True,
)
def displayTapNodeData(data):
    if data is None:
        return
    result = [
        html.H4("ID"),
        html.P(data["id"]),
        html.H4("Description"),
        html.P(data["description"]),
    ]
    if not data["id"].startswith("LOE"):
        result += [
            html.H4("Status"),
            html.P(data["status"]),
        ]
    return result


# display help text in timeline view
@app.callback(
    Output("info-panel", "children", allow_duplicate=True),
    Input("tabs", "value"),
    prevent_initial_call=True,
)
def switchToTimelineText(tab):
    if tab == "timeline":
        return html.H4(
            "Arrows show dependency relationships. To see additional information, hover on the timeline bars."
        )


if __name__ == "__main__":
    app.run_server(port=1000, debug=True)
