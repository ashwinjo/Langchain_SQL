from langchain.utilities import SQLDatabase
from langchain_openai import OpenAI
import sqlite3
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough

# Load the environment varibles
from dotenv import load_dotenv
load_dotenv()

db_path = "/Users/ashwjosh/modernaipro/UdemyLangchainCourse/TextToSQL/chinook.db"
# Create SQL DB connection
db = SQLDatabase.from_uri(f"sqlite:///{db_path}")


# Initialte LLM
llm = OpenAI(temperature=0, verbose=True)

""" #### When I want to get query"""

def get_db_schema_as_string(db_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Query to get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    schema_string = "Database Schema:\n"
    
    for table_name in tables:
        table_name = table_name[0]
        schema_string += f"\nTable: {table_name}\n"

        # Query to get table schema
        cursor.execute(f"PRAGMA table_info({table_name});")
        schema = cursor.fetchall()

        # Format column details
        schema_string += "Columns:\n"
        for column in schema:
            cid, name, col_type, not_null, default_val, pk = column
            schema_string += (
                f"  - {name} ({col_type})"
                f"{' NOT NULL' if not_null else ''}"
                f"{' PRIMARY KEY' if pk else ''}"
                f"{f' DEFAULT {default_val}' if default_val else ''}\n"
            )

    # Close the connection
    conn.close()
    
    return schema_string

# Example Query
query = "Which artist sold maximum music tracks"

p = PromptTemplate.from_template("""
### INSTRUCTION
Print ONLY the SQL Query for user question {query} given database schema 
### Schema
{db_schema}
### Restrictions
Do not add any extra text. Just return the SQL query.
###Output
Show  ONLY the < Answer to user query >
""")

import json
# Assuming 'llm' is an instance of a language model
out = p | llm | StrOutputParser()
sqlq = out.invoke(input={'query': query, 'db_schema': get_db_schema_as_string(db_path)})

# Print output of the query run
import ast
query_result = db.run(sqlq)
query_result = ast.literal_eval(query_result)

# Format and print the output
for artist, total_tracks in query_result:
    print(f"Artist: {artist}, Total Tracks Sold: {total_tracks}")

