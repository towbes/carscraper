import sqlite3
import pandas as pd

def load_data_from_sqlite(db_file, table_name):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_file)
    
    # Read data from the database table into a DataFrame
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql_query(query, conn)
    
    # Close the database connection
    conn.close()
    
    return df

def print_df_as_csv(df):
    # Convert the DataFrame to a CSV string
    csv_data = df.to_csv(index=False)
    
    # Print the CSV data
    print(csv_data)

# Example usage
if __name__ == "__main__":
    db_file = "car_data.db"
    table_name = "car_data"
    
    # Load data from SQLite into a DataFrame
    df = load_data_from_sqlite(db_file, table_name)
    
    # Print the DataFrame as a CSV
    print_df_as_csv(df)