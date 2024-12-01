import pandas as pd
import mysql.connector
from mysql.connector import Error
import streamlit as st


# Database connection details
db_config = {
    'host': st.secrets["DB_HOST"],
    'user':  st.secrets["DB_USER"],
    'password':  st.secrets["DB_PASSWORD"],
    'database':  st.secrets["DB_NAME"],
}

# Function to connect to the MySQL database
def connect_to_database():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as e:
        st.error(f"Error connecting to database: {e}")
        return None


def update_brokerage(amfi_code, new_brokerage):

    update_statement = f"Update ALL_SCHEMES SET GW_BROKERAGE={new_brokerage} WHERE Amfi_Code={amfi_code}"
    try:
        connection = connect_to_database()

        if connection.is_connected():
            cursor = connection.cursor()

            # Execute the update query with parameters
            cursor.execute(update_statement)
            rows=cursor.rowcount

            # Commit the transaction
            connection.commit()

            # Return the number of rows updated
            return cursor.rowcount

    except Error as e:
        print(f"Error: {e}")
        return -1

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


@st.cache_data()
def fetch_all_schemes():
    """
    Fetches a dataset from a remote MySQL database based on a query.

    Args:
        query (str): The SQL query to execute.

    Returns:
        pd.DataFrame: The resulting dataset as a Pandas DataFrame.
    """
    try:
        #st.write("function called")
        # Connect to the MySQL database
        connection = connect_to_database()

        if connection.is_connected():
            # Fetch data using Pandas
            df = pd.read_sql("SELECT * FROM ALL_SCHEMES", connection)
            return df

    except Error as e:
        print(f"Error: {e}")
        return None

    finally:
        if connection.is_connected():
            connection.close()


@st.cache_data()
def fetch_dataset(query):
    """
    Fetches a dataset from a remote MySQL database based on a query.

    Args:
        query (str): The SQL query to execute.

    Returns:
        pd.DataFrame: The resulting dataset as a Pandas DataFrame.
    """
    try:
        # Connect to the MySQL database
        connection = connect_to_database()

        if connection.is_connected():
            # Fetch data using Pandas
            df = pd.read_sql(query, connection)
            print("Data fetched successfully.")
            return df

    except Error as e:
        print(f"Error: {e}")
        return None

    finally:
        if connection.is_connected():
            connection.close()
