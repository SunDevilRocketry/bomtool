# BOM-Tool
<p>The BOM tool uses a python API to interface with Sun Devil Rocketry PCB BOMs
created using google sheets.</p>

<h3>Source Files</h3>
<p> bomtool.py: contains the main program loop and displays the BOM terminal</p>
<p> commands.py: contains the functions that are evoked by user input</p>
<p> jsonData.py: contains common json formatted data for interfacing with the google sheets api</p>

<h3>Data Files</h3>
<p>pcbs.txt: contains a list of all PCB BOM urls</p>

<h3>Installation Instructions</h3>
<ol>
   <li>Contact an SDR team lead for credentials file</li>
   <li>Download the python google sheets api with <code>pip install --user ezsheets</code></li>
   <li>Create a .gitignore file with python cache and credentials file</li>
</ol>

