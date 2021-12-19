import mysql.connector
from mysql.connector import Error



def create_server_connection(host_name, user_name, user_password, db_name=False):
    '''funtion to create sql connection.'''
    connection = None
    try:
        if db_name == False:
            connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                passwd=user_password
            )
            print("MySQL database connection sucessful")
        else:
            connection = mysql.connector.connect(
                host=host_name,
                user=user_name,
                passwd=user_password,
                database=db_name
            )
            print("MySQL database connection sucessful to {}".format(db_name))
    except Error as err:
        print(f"Error: '{err}'")

    return connection


def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print('database created sucessully')
    except Error as err:
        print(f"error '{err}'")


def use_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print('database created sucessully')
    except Error as err:
        print(f"error '{err}'")


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        #cursor.execute(query, multi=True)
        connection.commit()
        print("query sucessful:{}".format(query))
    except Error as err:
        print(f"Error: '{err}'")


def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error:'{err}'")
