from dash import Dash, html, dcc, Input, Output
import dash_cytoscape as cyto
import json

from styling import stylesheet
from elements import all_elements, nodes, nodes_list, edges, loes, loes_list

# APP CAPABILITIES:
# 1. DISPLAY LOE NETWORK
# 2. CLICK AND HOVER TO DISPLAY NODE OBJECTIVE DETAILS
# 3. SELECT NODE(S) TO SHOW LOCAL NETWORK

app = Dash(__name__)

cyto.load_extra_layouts()

# CREATE MORE COMPLEX COMPONENTS
# node checklist allows user to select nodes and show local dependencies
node_checklist = dcc.Checklist(
        id='node_checklist',
        options=nodes_list,
        value=nodes_list
    )

# cytoscape is the network/graph structure for dash
cytoscape = cyto.Cytoscape(
        id='cytoscape',
        layout={
            'name': 'dagre',
            'rankDir': 'TB'
        },
        style={'width': '100%', 'height': '500px'},
        elements=all_elements,
        stylesheet=stylesheet
    )

# LAYOUT DETERMINES ORGANIZATION OF COMPONENTS ON THE APP

app.layout = html.Div(
    id='app-container',
    children=[
        # title block on top
        html.Div(
            id='title-block',
            children=[
                html.H1('Project Network'),
                html.P('Click or hover over an objective to see details'),
                html.P('Select nodes from the checklist to see local network'),
                html.Hr()
            ]
        ),

        # menu block for filters, checklist, etc.
        html.Div(
            id='menu-block',
            children=[
                node_checklist,
                html.Hr()
            ]
        ),

        # cytoscape block
        html.Div(
            id='cytoscape-block',
            children=[
                cytoscape,
                html.Hr()
            ]
        ),

        # info block
        html.Div(
            id='info-block',
            children=[
                # left column displays click data and slider
                html.Div(
                    id='left-col',
                    style={'width': '40%', 'height': '200px', 'float': 'left'},
                    children=[
                        html.H4('Click Info'),
                        html.P(id='cytoscape-tapNodeData-output'),
                    ]
                ),
                # right column displays hover data
                html.Div(
                    id='right-col',
                    style={'width': '40%', 'height': '100px', 'float': 'right'},
                    children=[
                        html.H4('Hover Info'),
                        html.P(id='cytoscape-mouseoverNodeData-output')
                    ]
                ),
                html.Hr()
            ]
        )

    ])


# CALLBACKS

# node checklist displays selected nodes + dependencies
@app.callback(Output('cytoscape', 'elements'),
              Input('node_checklist', 'value'))
# update cytoscape based on nodes selected from checklist
def node_filter(node_checklist):
    selected_nodes = []
    selected_edges = []

    # loop through all selected nodes
    for node_id in node_checklist:

        # add selected nodes
        for node in nodes:
            if node['data']['id'] == node_id:
                selected_nodes.append(node)
                loe_node = next(loe for loe in loes if loe['data']['id'] == node['data']['parent'])
                selected_nodes.append(loe_node)

        # add connected edges
        for edge in edges:
            source_node = edge['data']['source']
            target_node = edge['data']['target']
            # add all edges where selected node is source
            if source_node == node_id:
                selected_edges.append(edge)
                # add corresponding target to complete edge
                new_target = next(node for node in nodes if node['data']['id'] == target_node)
                selected_nodes.append(new_target)
                loe_node = next(loe for loe in loes if loe['data']['id'] == new_target['data']['parent'])
                selected_nodes.append(loe_node)
            # add all edges where selected node is target
            if target_node == node_id:
                selected_edges.append(edge)
                # add corresponding source to complete edge
                new_source = next(node for node in nodes if node['data']['id'] == source_node)
                selected_nodes.append(new_source)
                loe_node = next(loe for loe in loes if loe['data']['id'] == new_source['data']['parent'])
                selected_nodes.append(loe_node)

    # remove duplicate nodes
    sel_nodes = []
    [sel_nodes.append(node) for node in selected_nodes if node not in sel_nodes]

    # remove duplicate edges
    sel_edges = []
    [sel_edges.append(edge) for edge in selected_edges if edge not in sel_edges]

    # return selected elements
    return sel_nodes + sel_edges


# click element to display info
@app.callback(Output('cytoscape-tapNodeData-output', 'children'),
              Input('cytoscape', 'selectedNodeData'))
def displayTapNodeData(data):
    return json.dumps(data, indent=2)

# mouse over element to display info
@app.callback(Output('cytoscape-mouseoverNodeData-output', 'children'),
              Input('cytoscape', 'mouseoverNodeData'))
def displayHoverNodeData(data):
    if data:
        return json.dumps(data, indent=2)


if __name__ == '__main__':
    app.run_server(port=1002, debug=True)
