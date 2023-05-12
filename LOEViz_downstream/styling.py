# CREATE STYLESHEET FOR CYTOSCAPE

stylesheet = [
            # Group selectors
            # all nodes
            {
                'selector': 'node',
                'style': {
                    'label': 'data(label)'
                }
            },

            # Class selectors
            # LOEs gray
            {
                'selector': '.loe',
                'style': {
                    'background-color': 'gray'
                }
            },
            # Objectives circles
            {
                'selector': '.obj',
                'style': {
                    'shape': 'circle'
                }
            },
            # Intermediate Objectives triangles
            {
                'selector': '.io',
                'style': {
                    'shape': 'triangle'
                }
            },
            # Dependent edges cyan
            {
                'selector': '.dep',
                'style': {
                    'curve-style': 'bezier',
                    'line-color': 'black',
                    'line-style': 'solid',
                    'source-arrow-color': 'black',
                    'source-arrow-shape': 'triangle'
                }
            },
            # Interdependent edges violet
            {
                'selector': '.interdep',
                'style': {
                    'curve-style': 'bezier',
                    'line-color': 'black',
                    'line-style': 'dashed',
                    'source-arrow-color': 'black',
                    'source-arrow-shape': 'triangle',
                    'target-arrow-color': 'black',
                    'target-arrow-shape': 'triangle'
                }
            },

            # Attribute selectors
            # Status
            {
                'selector': '[status = "behind"]',
                'style': {
                    'background-color': 'red',
                }
            },
            {
                'selector': 'node[status = "on track"]',
                'style': {
                    'background-color': 'yellow'
                }
            },
            {
                'selector': '[status = "ahead"]',
                'style': {
                    'background-color': 'green'
                }
            },
            {
                'selector': '[status = "completed"]',
                'style': {
                    'background-color': 'blue'
                }
            },
        ]