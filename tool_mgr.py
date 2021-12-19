from sql_mgr import sql_mgr
import os
from dxf_combiner import dxf_combiner

print(os.getcwd())
os.chdir(os.path.dirname(os.path.abspath(__file__)))

tool_file = "tools.xlsx"
manufacturer_file = "manufacturers.xlsx"
drawer_file = "drawers.xlsx"
drawer_to_tools_file = """drawer_to_tools.xlsx"""
profile_file = "profiles.xlsx"

# initialize sql database
# sql_mgr must be modified for database login path and credentials
sql_tool = sql_mgr(tool_file,
                   manufacturer_file,
                   drawer_file,
                   drawer_to_tools_file,
                   profile_file)

# query database for drawers

drawer_list = sql_tool.read(
    """SELECT drawer_id FROM drawer"""
)


def flatten_list(data):
    flat_data = []
    for d in data:
        for i in d:
            flat_data.append(i)
    return flat_data


drawer_list = flatten_list(drawer_list)

print("drawer list \n {}".format(drawer_list))

# for each drawer sql query for tool paths to generate for drawer
for drawer_id in drawer_list:
    data = sql_tool.read(
        """SELECT profile_path
            FROM contains_tools
            JOIN tool
            ON contains_tools.tool_id = tool.tool_id
            JOIN profile
            ON tool.profile = profile.profile_id
            WHERE drawer_id = {id}""".format(id=drawer_id)
    )

    print(data)
    print("flat data")
    print(flatten_list(data))

    # send file paths to combiner to generate drawer layout
    target_file = "drawer_inserts/layoutTest_drawer_{}.dxf".format(drawer_id)
    bounds = [100, 100]
    padding = .25
    combiner = dxf_combiner()
    combiner.layout_doc(flatten_list(data), target_file, bounds, padding)
