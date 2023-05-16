# GENERATE ELEMENTS

import data_loading

project_data = data_loading.load_data("project_state.xlsx")

loes = []
objs = []
ios = []
deps = []

for _, row in project_data.iterrows():
    if row["ID"].startswith("LOE"):
        loes.append(
            {
                "data": {
                    "id": row["ID"],
                    "label": row["ID"],
                    "description": row["Description"],
                },
                "position": {"x": 0, "y": 0},
                "classes": "loe",
            }
        )
    elif row["ID"].startswith("O"):
        parent_id = f"LOE{row['ID'].split('.')[0][1:]}"
        print(parent_id)
        objs.append(
            {
                "data": {
                    "id": row["ID"],
                    "label": row["ID"],
                    "description": row["Description"],
                    "status": row["Status"].lower(),
                    # "progress": "neutral",
                    "parent": parent_id,
                },
                "position": {
                    "x": 0,
                    "y": 0,
                },
                "classes": "obj",
            }
        )
    elif row["ID"].startswith("IO"):
        parent_id = f"LOE{row['ID'].split('.')[0][2:]}"
        print(parent_id)
        objs.append(
            {
                "data": {
                    "id": row["ID"],
                    "label": row["ID"],
                    "description": row["Description"],
                    "status": row["Status"].lower(),
                    # "progress": "neutral",
                    "parent": parent_id,
                },
                "position": {
                    "x": 0,
                    "y": 0,
                },
                "classes": "io",
            }
        )
    if not isinstance(row["Dependencies"], str):
        continue
    dependencies = row["Dependencies"].split(",")
    deps += [
        {"data": {"source": row["ID"], "target": dependency}, "classes": "dep"}
        for dependency in dependencies
        if not row["ID"].startswith("LOE")
    ]

# aggregate elements
loes_list = [loe["data"]["id"] for loe in loes]
nodes = objs + ios
nodes_list = [node["data"]["id"] for node in nodes]
edges = deps
all_elements = loes + nodes + edges
