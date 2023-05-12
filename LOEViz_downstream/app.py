from dash import Dash, html, dcc, Input, Output
import dash_cytoscape as cyto
import json

from styling import stylesheet
from elements import all_elements, nodes, nodes_list, edges, loes, loes_list
from helper import update_downstream_elements

# APP CAPABILITIES:
# 1. DISPLAY LOE NETWORK
# 2. CLICK AND HOVER TO DISPLAY NODE OBJECTIVE DETAILS
# 3. CHANGE STATUS OF NODES TO SEE DOWNSTREAM EFFECTS
#   * have to manually update interdependent nodes to see effect on other interdependent nodes,
#       can try to improve on this

app = Dash(__name__)

# Load extra layouts
cyto.load_extra_layouts()

# CREATE MORE COMPLEX COMPONENTS

###
# slider to change node status
# hidden until node is clicked
# starting value is blank and causes error, but app can still run
# need to find a way to set value to existing status of node when clicked
###
node_status_slider = html.Div(id='slider', hidden=True, children=[
    dcc.Slider(
        id='node-status-slider',
        min=0,
        max=3,
        step=1,
        marks={
            0: 'behind',
            1: 'on track',
            2: 'ahead',
            3: 'completed'
        },
        included=False,
        updatemode='drag',
    )])

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
                html.P('Click on a node and use the slider to change the status and see downstream effects'),
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
                        node_status_slider
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


# DASH APP CALLBACKS

# show slider if node selected
@app.callback(
    Output('slider', 'hidden'),
    Input('cytoscape', 'selectedNodeData'))
def displaySlider(data):
    return False if data else True


# update node status based on slider value
@app.callback(Output('cytoscape', 'elements'),
              Input('node-status-slider', 'value'),
              Input('cytoscape', 'elements'),
              Input('cytoscape', 'selectedNodeData'))
def updateNodeStatus(value, elements, selected):
    # create map of values to match slider values
    slider_val_map = {
        0: 'behind',
        1: 'on track',
        2: 'ahead',
        3: 'completed'}

    # Update only the selected element(s)
    if selected:
        # get ids
        ids = [nodeData['id'] for nodeData in selected]
        # access node objects
        selected_nodes = ((i, n) for i, n in enumerate(elements) if n['data']['id'] in ids)
        # update 'status' property in the node
        for i, node in selected_nodes:
            elements[i]['data']['status'] = slider_val_map[value]
        # propagate downstream effects
        update_downstream_elements(selected, elements)

    return elements


# display node info when clicked
@app.callback(Output('cytoscape-tapNodeData-output', 'children'),
              Input('cytoscape', 'tapNodeData'))
def displayTapNodeData(data):
    return json.dumps(data, indent=2)


# display node info when hovered over
@app.callback(Output('cytoscape-mouseoverNodeData-output', 'children'),
              Input('cytoscape', 'mouseoverNodeData'))
def displayTapEdgeData(data):
    return json.dumps(data, indent=2)


if __name__ == '__main__':
    app.run_server(port=1001, debug=True)
