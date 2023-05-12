# HELPER FUNCTIONS

# update single node based on status of upstream nodes
def update_single_node(node_id, upstream_status, elements):
    # new node status is equal to worst case status of upstream nodes
    if 'behind' in upstream_status:
        new_status = 'behind'
    elif 'on track' in upstream_status:
        new_status = 'on track'
    elif 'ahead' in upstream_status:
        new_status = 'ahead'
    else:
        new_status = 'completed'

    # access node object
    current_node = ((i, n) for i, n in enumerate(elements) if n['data']['id'] == node_id)
    # update 'status' property
    for i, node in current_node:
        elements[i]['data']['status'] = new_status


# update single level of nodes
def update_level(level, elements, dep_edges, interdep_edges):

    # loop through all nodes in level
    for node_id in level:
        # get upstream nodes that current node depends on
        upstream_level = [edge['data']['target'] for edge in dep_edges if edge['data']['source'] == node_id]
        # get nodes that are interdependent with current node
        upstream_level = upstream_level + [edge['data']['target'] for edge in interdep_edges if
                                           edge['data']['source'] == node_id]
        upstream_level = upstream_level + [edge['data']['source'] for edge in interdep_edges if
                                           edge['data']['target'] == node_id]

        # get status of all upstream nodes
        upstream_status = []
        for upstream_node_id in upstream_level:
            upstream_status = upstream_status + [element['data']['status'] for element in elements if
                                                 element['data']['id'] == upstream_node_id]

        # update node based on status of upstream nodes
        update_single_node(node_id, upstream_status, elements)


# update downstream elements
# issue when interdependent nodes have same dependencies upstream (e.g. O1.1 - O1.2)
def update_downstream_elements(selected, elements):
    # extract selected node id
    selected_id = selected[0]['id']

    # separate dependent and independent edges because they have different update mechanisms
    dep_edges = [element for element in elements if element['classes'] == 'dep']
    interdep_edges = [element for element in elements if element['classes'] == 'interdep']

    # initialize loop parameters
    finished = False
    current_node_level = [selected_id]

    # loop until all downstream nodes checked
    while not finished:
        # initialize empty list of next downstream level
        next_nodes = []

        # loop through all nodes in current level
        for node_id in current_node_level:
            # find nodes in next downstream level and add to list
            next_nodes = next_nodes + [edge['data']['source'] for edge in dep_edges if
                                       edge['data']['target'] == node_id]
            # get interdependent nodes
            next_nodes = next_nodes + [edge['data']['target'] for edge in interdep_edges if
                                       edge['data']['source'] == node_id]
            next_nodes = next_nodes + [edge['data']['source'] for edge in interdep_edges if
                                       edge['data']['target'] == node_id]

            # update status of next downstream level
            update_level(next_nodes, elements, dep_edges, interdep_edges)

        finished = True
