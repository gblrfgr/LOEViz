LOE VISUALIZATION README

Updated 05/11/2023 by Cyrus Rad
Updated 05/17/2023 by Juniper Mills

SUMMARY

There are 3 different folders, each corresponding to a different Dash web app that showcases a particular feature. 
These features will likely be tweaked and/or combined to create a single app in the future.

All apps revolved around the Dash 'cytoscape' object, which creates a network-like visualization of project dependencies.
All apps share the same initial elements and stylesheet for the cytoscape.
All apps also share 'click' and/or 'hover' capabilities to display information about a particular node.


1. LOEViz_base:
	Demonstrates how the user can selectively view LOEs through the use of a checklist. Also features a timeline view,
	whereby project data can be visualized in a Gantt chart that also shows dependencies. Moreover, this app loads project
	data from an Excel file.
	
2. LOEViz_downstream:
	Demonstrates how the user can change the status of a particular node and see the downstream effects on dependent nodes.
	
3. LOEViz_local:
	Demonstrates how the user can selectively view local areas of the network by selecting a subset of nodes.
	
FILE STRUCTURE

app.py: contains layout and callbacks for app
elements.py: creates element variables (nodes represent objectives, edges represent dependencies) for cytoscape
styling.py: creates stylesheet for cytoscape
data_loading.py (only for LOEViz_base): defines additional functions to handle loading Excel data
helper.py (only for LOEViz_downstream): defines additional functions that support the main slider callback function
	
HOW TO RUN
*assumes local machine has python and pip already installed

1. Download/save project folder(s). Each project folder should have at least: 'app.py', 'elements.py', 'styling.py', 'requirements.txt'
2. Open command prompt and navigate into project directory.
	ex: ~/Downloads/LOEViz_base
3. Enter the following command to set up environment:
	pip install -r requirements.txt
4. Enter the following command to run app:
	python app.py
5. At this point, the following text should pop up in the command window:
	'Dash is running on http://127.0.0.1:XXXX/' where XXXX is the port used (different for each app)
	Copy and paste the 'http://127.0.0.1:XXXX/' into a web browser and the app should appear.
6. Ctrl+C in the command window to stop serving the app.
	

LOEVIZ_BASE ONLY

In order to start the app, the project state file must not be concurrently open in Excel. Additionally, to reload the data,
one must press Ctrl+C in the command window to stop serving the app and then restart it. Once the app is running, the file may
be opened in Excel, but saved changes will not be reflected in the app until it is restarted. Any deviation from the existing format,
except for capitalization in the status text and the formatting of the date columns (though it must be formatted as an Excel date),
will result in the program ending with an error.
	