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
    db = SQLDatabase.from_uri("sqlite:///chinook.db")
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

    #print(df)
    # Create a prompt template to ask the LLM for the best plot
    prompt = PromptTemplate(
        input_variables=["data"],
        template="""
        Given the following dataset, output the Plotly code to render the visualization:

        {data}

        Output should only be the python code, no extra information.
        """
    )

    # Set up the LLM and chain
    llm = OpenAI(temperature=0.5)
    chain = prompt | llm

    # Prepare the data (convert the DataFrame into a string format that LLM can understand)
    data_string = df.head().to_string()

    # Ask the LLM to suggest a Plotly graph
    response = chain.invoke(input=data_string)

    # Print the response (Python code for Plotly graph)
    print(response)

    # Run the generated code (after ensuring it's safe and valid)
    # exec(response)
    # Prepare a safe execution context
    safe_locals = {}

    # Execute the generated Plotly code safely
    try:
        exec(response, {}, safe_locals)
        if 'fig' in safe_locals:
            safe_locals['fig'].show()  # Show the plot if it exists
    except Exception as e:
        print(f"Error executing the code: {e}")

