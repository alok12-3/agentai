import os
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool, tool
from langchain_google_genai import ChatGoogleGenerativeAI
from weasyprint import HTML
from markdown2 import markdown
from io import BytesIO
import sqlite3  # Example with SQLite; adapt to other databases as needed
from langchain_community.tools.sql_database.tool import (
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
    QuerySQLCheckerTool,
    QuerySQLDataBaseTool,
)
from langchain_community.utilities.sql_database import SQLDatabase
import pandas as pd

# Set API Keys
SERPER_API_KEY = "0021206eb1302a4b366ff55571f99f0245f7b21d"
GOOGLE_API_KEY = "AIzaSyCO5gvhQWs27JMRRZsl6pJiKXReRppy1xk"
os.environ['SERPER_API_KEY'] = SERPER_API_KEY
os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY

# Initialize search tool
search_tool = SerperDevTool()

# Define Custom SQL Execution Tool
@tool
def execute_sql_query(query: str) -> str:
    """
    Execute an SQL query on the specified database and return results.
    
    Parameters:
    - query: SQL query string to be executed
    - database_path: Path to the SQLite database file
    
    Returns:
    - String with the query results formatted as text
    """
    try:
        conn = sqlite3.connect('datafile.db')

        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()
        
        result_str = "\n".join(str(row) for row in results)
        return f"Query executed successfully:\n{result_str}"
    except Exception as e:
        return f"Error executing query: {e}"
    
df = pd.read_csv("ds-salaries.csv")
connection = sqlite3.connect("salaries.db")
df.to_sql(name="salari", con=connection)
    
db = SQLDatabase.from_uri("sqlite:///salari.db")
    
@tool("list_tables")
def list_tables() -> str:
    """List the available tables in the database"""
    return ListSQLDatabaseTool(db=db).invoke("")

@tool("tables_schema")
def tables_schema(tables: str) -> str:
    """
    Input is a comma-separated list of tables, output is the schema and sample rows
    for those tables. Be sure that the tables actually exist by calling `list_tables` first!
    Example Input: table1, table2, table3
    """
    tool = InfoSQLDatabaseTool(db=db)
    return tool.invoke(tables)

@tool("execute_sql")
def execute_sql(sql_query: str) -> str:
    """Execute a SQL query against the database. Returns the result"""
    return QuerySQLDataBaseTool(db=db).invoke(sql_query)

@tool("check_sql")
def check_sql(sql_query: str) -> str:
    """
    Use this tool to double check if your query is correct before executing it. Always use this
    tool before executing a query with `execute_sql`.
    """
    return QuerySQLCheckerTool(db=db, llm=llm).invoke({"query": sql_query})

# Define Agents
agent1 = Agent(
    role="Data Strategist",
    goal="Determine the data insights needed and create SQL query requirements.",
    backstory=(
        "You are responsible for formulating data insights goals and instructing Agent 2 on SQL query requirements."
    ),
    
    llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.5),
    verbose=True,
    allow_delegation=True,
)

agent2 = Agent(
    role="SQL Query Writer",
    goal="Write and execute SQL queries based on instructions from Agent 1. and you only write sql quiries without anything else",
    backstory=(
        "You specialize in SQL and can execute queries to retrieve data insights."
    ),
    tools=[list_tables, tables_schema, execute_sql, check_sql],
    llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.1),
    verbose=True
)

agent3 = Agent(
    role="Data Quality Assessor",
    goal="Assess if the SQL data output meets the insights objectives set by Agent 1.",
    backstory=(
        "You are skilled at evaluating data for insightfulness and relevance to project goals."
    ),
    
    llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.1),
    verbose=True,
    allow_delegation=True,
)

agent4 = Agent(
    role="Data Summarizer",
    goal="Summarize the insights into a clear and concise report for stakeholders.",
    backstory=(
        "You have a knack for summarizing complex data into easy-to-understand insights."
    ),
   
    llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.1),
    verbose=True
)
#
# agent5 = Agent(
#     role="Data Finder",
#     goal="Locate the relevant dataset for SQL query execution.",
#     backstory=(
#         "You excel at finding datasets required for analysis and ensuring data accuracy."
#     ),
#     llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.1),
#     verbose=True
#)

# Define Tasks
task1 = Task(
    description="Determine the specific SQL queries required to generate insights from data.",
    expected_output="A list of SQL query requirements for Agent 2 to execute.",
    agent=agent1
)

task2 = Task(
    description="Write and execute SQL queries as per Agent 1's instructions. Use the dataset provided by Agent 5.",
    expected_output="Executed SQL queries with results passed to Agent 3.",
    agent=agent2
)

task3 = Task(
    description="Assess whether the SQL query results from Agent 2 provide meaningful insights.",
    expected_output="A validation report on the insightfulness of data with recommendations if necessary.",
    agent=agent3
)

task4 = Task(
    description="Summarize the validated data insights into a concise and understandable report.",
    expected_output="A clear summary report of insights for stakeholders.",
    agent=agent4
)

# task5 = Task(
#     description="Locate the relevant dataset based on Agent 1's data needs for SQL execution.",
#     expected_output="Dataset required for SQL queries, provided to Agent 2.",
#     agent=agent5
# )

# Define Crew Process
def generate_report():
    # Define the Crew
    crew = Crew(
        agents=[agent1, agent2, agent3, agent4],
        tasks=[task1, task2, task3, task4],
        verbose=True
    )

    # Trigger the research and report generation
    final = crew.kickoff()
    
    finalstr = markdown(final)
    pdf_buffer = BytesIO()
    HTML(string=finalstr).write_pdf(pdf_buffer)
    pdf_buffer.seek(0)

    # Save the PDF
    with open(f"report.pdf", "wb") as f:
        f.write(pdf_buffer.read())
    print(f"Report  generated and saved as report.pdf.")

# Example usage
if __name__ == '__main__':

    # generate_report()
    print(tables_schema.run("datafile.db"))
