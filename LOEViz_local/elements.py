# GENERATE ELEMENTS

# define LOEs
loes = [
    {
        'data': {'id': id, 'label': id, 'description': description},
        'position': {'x': 0, 'y': 0},
        'classes': 'loe'
    }
    for id, description in (

        ('LOE1', 'do this week'),
        ('LOE2', 'do next week'),
        ('LOE3', 'do this month')
    )
]

# define objectives
objs = [
    {
        'data': {'id': id, 'label': id, 'description': description, 'status': status, 'progress': progress,
                 'parent': parent},
        'position': {'x': 0, 'y': 0},
        'classes': 'obj'
    }
    for id, description, status, progress, parent in (

        ('O1.1', 'create project visualization tool', 'on track', 'forward', 'LOE1'),
        ('O1.2', 'clean around the house', 'behind', 'neutral', 'LOE1'),
        ('O2.1', 'get groceries', 'behind', 'neutral', 'LOE2'),
        ('O3.1', 'visit NC', 'on track', 'neutral', 'LOE3')
    )
]

# define intermediate objectives
ios = [
    {
        'data': {'id': id, 'label': id, 'description': description, 'status': status, 'progress': progress,
                 'parent': parent},
        'position': {'x': 0, 'y': 0},
        'classes': 'io'
    }
    for id, description, status, progress, parent in (
        ('IO1.1.1', 'research potential methods', 'completed', 'forward', 'LOE1'),
        ('IO1.1.2', 'explore networkx, plotly, dash tools', 'ahead', 'forward', 'LOE1'),
        ('IO1.1.3', 'update Mike and Dave', 'behind', 'backward', 'LOE1'),
        ('IO1.2.1', 'wash sheets and towels', 'on track', 'forward', 'LOE1'),
        ('IO1.2.2', 'swiffer floors', 'behind', 'neutral', 'LOE1'),
        ('IO1.2.3', 'dust living room and bedroom', 'behind', 'neutral', 'LOE1'),
        ('IO2.1.1', 'go to Sams Club', 'on track', 'forward', 'LOE2'),
        ('IO2.1.2', 'go to Aldi', 'behind', 'backward', 'LOE2'),
        ('IO3.1.1', 'book plane ticket', 'completed', 'neutral', 'LOE3'),
        ('IO3.1.2', 'buy gifts', 'on track', 'forward', 'LOE3'),
        ('IO3.1.3', 'pack', 'behind', 'neutral', 'LOE3')
    )
]

# define dependencies
deps = [
    {
        'data': {'source': source, 'target': target},
        'classes': classes
    }
    for source, target, classes in (
        ('O1.1', 'IO1.1.1', 'dep'),
        ('O1.1', 'IO1.1.2', 'dep'),
        ('O1.1', 'IO1.1.3', 'dep'),
        ('O1.2', 'IO1.2.1', 'dep'),
        ('O1.2', 'IO1.2.2', 'dep'),
        ('O1.2', 'IO1.2.3', 'dep'),
        ('O1.1', 'O1.2', 'interdep'),
        ('O1.1', 'IO1.2.1', 'dep'),
        ('O2.1', 'IO2.1.1', 'dep'),
        ('O2.1', 'IO2.1.2', 'dep'),
        ('IO2.1.1', 'IO1.1.1', 'interdep'),
        ('O3.1', 'IO3.1.1', 'dep'),
        ('O3.1', 'IO3.1.2', 'dep'),
        ('O3.1', 'IO3.1.3', 'dep'),
        ('IO3.1.2', 'IO3.1.3', 'dep')
    )
]

# aggregate elements
loes_list = [loe['data']['id'] for loe in loes]
nodes = objs + ios
nodes_list = [node['data']['id'] for node in nodes]
edges = deps
all_elements = loes + nodes + edges