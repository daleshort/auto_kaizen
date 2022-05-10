# auto_kaizen
A Python tool for automatically creating kaizen foam tool layouts using a mySQL driven tool database.  I made this to as practice for working with SQL databases. The tool data is initially stored in excel spreadsheets but then transferred to the database.  Database queries are then used to pull the correct data to create a DXF file of the tool layout.

tools.xlsx is a spreadsheet of tools
manufacturers.xslx is a mapping of manufacturer numbers to manufacturer names
drawers.xlsx stores the drawer numbers and dimensions
drawer_to_tools.xlsx stores what tools are in what drawer
profiles.xlsx is a sheet of profile numbers mapped to file locations of a DXF graphic profile of that tool.

tool_mgr.py is the main script. It calls sql_mgr.py which creates the database pytools and tables that match the excel files (a mySQL database must be available to the script). tool_mgr.py then queries the database for a list of drawers and then for each drawer executes a SQL query that returns a list of tool profile DXF files that should be added to the particular drawer layout.  The dxf_combiner.py then arranges the profiles into a single DXF file to be used as the foam insert artwork for that drawer.
