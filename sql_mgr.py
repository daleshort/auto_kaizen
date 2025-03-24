from pysql import create_database, create_server_connection, \
    execute_query, read_query
from sheet_mgr import excel2sql


class sql_mgr ():

    def __init__(self, tool_file, manufacturer_file,
                 drawer_file, drawer_to_tools_file, profile_file):

        # yes i'm storing a password here as an example. Use env in the future.
        self.connection = create_server_connection('localhost',
                                                   'root', 'kittens')

        execute_query(self.connection, """
        DROP DATABASE pytools
        """
                      )

        create_database(self.connection, """
        CREATE DATABASE pytools
        """)
        # yes i'm storing a password here as an example. Use env in the future.
        self.connection = create_server_connection('localhost', 'root', 'kittens', 'pytools')

        tool_query = """
            CREATE TABLE tool(
            tool_id INT PRIMARY KEY,
            tool_name VARCHAR(40) NOT NULL,
            purchase_date DATE,
            tool_typ VARCHAR(40),
            manufacturer INT,
            profile INT)
        """
        drawer_query = """
        CREATE TABLE drawer(
            drawer_id INT PRIMARY KEY,
            drawer_width INT,
            drawer_height INT)
        """

        manufacturer_query = """
        CREATE TABLE manufacturer(
            manufacturer_id INT PRIMARY KEY,
            manufacturer_name VARCHAR(40))
        """

        profile_query = """
        CREATE TABLE profile(
            profile_id INT PRIMARY KEY,
            profile_path VARCHAR(100))
        """

        execute_query(self.connection, tool_query)
        execute_query(self.connection, drawer_query)
        execute_query(self.connection, manufacturer_query)
        execute_query(self.connection, profile_query)

        execute_query(self.connection, """
        ALTER TABLE tool
        ADD FOREIGN KEY(manufacturer)
        REFERENCES manufacturer(manufacturer_id)
        ON DELETE SET NULL""")

        execute_query(self.connection, """
        ALTER TABLE tool
        ADD FOREIGN KEY(profile)
        REFERENCES profile(profile_id)
        ON DELETE SET NULL""")

        execute_query(self.connection, """
        CREATE TABLE contains_tools(
            tool_id INT,
            drawer_id INT,
            PRIMARY KEY(tool_id,drawer_id),
            FOREIGN KEY(tool_id) REFERENCES tool(tool_id),
            FOREIGN KEY(drawer_id) REFERENCES drawer(drawer_id))""")

        self.import_and_execute(manufacturer_file, "manufacturer")
        self.import_and_execute(profile_file, "profile")
        self.import_and_execute(tool_file, "tool")
        self.import_and_execute(drawer_file, "drawer")
        self.import_and_execute(drawer_to_tools_file, "contains_tools")

    def import_and_execute(self, filePath, database):
        import_data = excel2sql().extract_excel_data(filePath)
        print("values imported")
        print(import_data)

        for query in import_data:
            execute_query(self.connection, """
            INSERT INTO {} VALUES {}
            """.format(database, query))

    def read(self, query):
        data = []
        # "SELECT * FROM tool"
        results = read_query(self.connection, query)
        for result in results:
            print(result)
            data.append(result)
        return data
