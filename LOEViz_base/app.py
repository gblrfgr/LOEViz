from dash import Dash, html, dcc, Input, Output
import dash_cytoscape as cyto
import json

from styling import stylesheet
from elements import all_elements, nodes, nodes_list, edges, loes, loes_list

# APP CAPABILITIES:
# 1. DISPLAY LOE NETWORK
# 2. CLICK AND HOVER TO DISPLAY NODE OBJECTIVE DETAILS
# 3. SELECTIVELY VIEW LOES

app = Dash(__name__)

cyto.load_extra_layouts()

# CREATE MORE COMPLEX APP COMPONENTS

# LOE checklist to select which LOEs to display
loe_checklist = dcc.Checklist(id="loe_checklist", options=loes_list, value=loes_list)

# cytoscape is the network/graph structure for dash
cytoscape = cyto.Cytoscape(
    id="cytoscape",
    layout={"name": "dagre", "rankDir": "TB"},
    style={"width": "100%", "height": "500px"},
    elements=all_elements,
    stylesheet=stylesheet,
)

# LAYOUT DETERMINES ORGANIZATION OF COMPONENTS ON THE APP

app.layout = html.Div(
    id="app-container",
    children=[
        # title block on top
        html.Div(
            id="title-block",
            children=[
                html.H1("Project Network"),
                html.P("Click or hover over an objective to see details"),
                html.Hr(),
            ],
        ),
        # menu block for filters, checklist, etc.
        html.Div(id="menu-block", children=[loe_checklist, html.Hr()]),
        # cytoscape block
        html.Div(id="cytoscape-block", children=[cytoscape, html.Hr()]),
        # info block
        html.Div(
            id="info-block",
            children=[
                # left column displays click data
                html.Div(
                    id="left-col",
                    style={"width": "40%", "height": "100px", "float": "left"},
                    children=[
                        html.H4("Click Info"),
                        html.P(id="cytoscape-tapNodeData-output"),
                    ],
                ),
                # right column displays hover data
                html.Div(
                    id="right-col",
                    style={"width": "40%", "height": "100px", "float": "right"},
                    children=[
                        html.H4("Hover Info"),
                        html.P(id="cytoscape-mouseoverNodeData-output"),
                    ],
                ),
                html.Hr(),
            ],
        ),
    ],
)


# CALLBACKS MAKE APP INTERACTIVE


# LOE checklist displays nodes in selected LOE, along with dependencies in other LOEs
@app.callback(Output("cytoscape", "elements"), Input("loe_checklist", "value"))
def loe_filter(loe_checklist):
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
    sel_nodes = []
    [sel_nodes.append(node) for node in selected_nodes if node not in sel_nodes]

    # return selected elements
    return sel_nodes + selected_edges


# display node info when clicked
@app.callback(
    Output("cytoscape-tapNodeData-output", "children"),
    Input("cytoscape", "tapNodeData"),
)
def displayTapNodeData(data):
    return json.dumps(data, indent=2)


# display node info when hovered over
@app.callback(
    Output("cytoscape-mouseoverNodeData-output", "children"),
    Input("cytoscape", "mouseoverNodeData"),
)
def displayTapEdgeData(data):
    return json.dumps(data, indent=2)


if __name__ == "__main__":
    app.run_server(port=1000, debug=True)
