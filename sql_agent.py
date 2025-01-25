from langchain.utilities import SQLDatabase
from langchain_openai import OpenAI
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType
from langchain_core.prompts import PromptTemplate 
import pandas as pd
import matplotlib.pyplot as plt
import io

# Load the environment varibles
from dotenv import load_dotenv
load_dotenv()


def get_db_connection():
    # Create SQL DB connection
    # print(db.get_usable_table_names())
    db = SQLDatabase.from_uri("sqlite:////Users/ashwjosh/modernaipro/UdemyLangchainCourse/TextToSQL/chinook.db")
    return db
    
def get_llm():
    # Initialte LLM
    llm = OpenAI(temperature=0, verbose=True)
    return llm


def init_agent():
    # Creating React Agent. Sort of an agent chain here
    llm = get_llm()
    db = get_db_connection()
    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=SQLDatabaseToolkit(db=db, llm=llm),
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True
    )
    return agent_executor


def run_agent(query_user=None):
    agent_executor = init_agent()
    query = f"""
    You are an AI assistant that helps with SQL queries. 
    For the question below, provide a result in CSV format. Add the header according to answer to user query:
    Question: {query_user}
    Answer in CSV format:
    """
    response = agent_executor.run(query)
    return response


def user_prompt(query_user):
    resp = run_agent(query_user=query_user)
    return resp


while True:
    response = user_prompt(query_user=input("NLP: "))
    print(response)
     # "Who are top 5 Artists and how many albums did each of them sell?"

    data = io.StringIO(response)  # Simulating a CSV file
    df = pd.read_csv(data)

    # # Print the DataFrame
    # print(df)


# # Extract headers and data items
# headers = df.columns.tolist()  # ['Artist', 'AlbumsSold']
# data_items = df.values.tolist()  # [['Artist A', 120], ['Artist B', 90], ...]

# # Bar Graph Plot
# plt.figure(figsize=(10, 6))
# plt.bar(df[headers[0]], df[headers[1]], color="skyblue", edgecolor="black")
# plt.title(f"{headers[0]} vs {headers[1]}", fontsize=16)
# plt.xlabel(headers[0], fontsize=12)
# plt.ylabel(headers[1], fontsize=12)
# plt.grid(axis="y", linestyle="--", alpha=0.7)
# plt.tight_layout()

# # Show the plot
# plt.show()
