import streamlit as st
import pandas as pd
import sqlite3
import json
import os

from pathlib import Path
from textwrap import dedent


from crewai import Agent, Crew, Process, Task
from crewai_tools import tool
# from langchain.schema import AgentFinish
# from langchain.schema.output import LLMResult
from langchain_community.tools.sql_database.tool import (
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
    QuerySQLCheckerTool,
    QuerySQLDataBaseTool,
)
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities.sql_database import SQLDatabase
# from langchain_core.callbacks.base import BaseCallbackHandler
# from langchain_core.prompts import ChatPromptTemplate

# Streamlit interface for file upload
st.title("CSV to SQL Conversion and Analysis")
uploaded_file = st.file_uploader("Upload a CSV file", type="csv")

if uploaded_file is not None:
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(uploaded_file)
    
    # Display the DataFrame in Streamlit
    st.write("Uploaded CSV file:")
    st.dataframe(df)
    
    # Convert DataFrame to SQLite database
    connection = sqlite3.connect("salaries.db")
    df.to_sql(name="salaries", con=connection, if_exists="replace", index=False)
    st.success("CSV data has been converted to SQLite database and loaded into table 'salaries'.")

    # Initialize the required SQL and LLM tools
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key="AIzaSyAu7N_nUyoDcH_c0zultQI_tHJuxTKo3g4")
    db = SQLDatabase.from_uri("sqlite:///salaries.db")

    @tool("list_tables")
    def list_tables() -> str:
      """List the available tables in the database"""
      return ListSQLDatabaseTool(db=db).invoke("")

    @tool("tables_schema")
    def tables_schema(tables: str) -> str:
      """
      Input is a comma-separated list of tables, output is the schema and sample rows
      for those tables. Be sure that the tables actually exist by calling list_tables first!
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

    # Define agents and tasks as per the original code
    thinker = Agent(
        role="Senior Data Scientist",
        goal="Identify relationships and insights in data, then delegate SQL tasks.",
        backstory=dedent("""
            A creative data scientist who discovers new insights by exploring data relationships.
        """),
        llm=llm,
        tools=[list_tables, tables_schema, execute_sql, check_sql],
        allow_delegation=False,
    )

    sql_dev = Agent(
        role="Senior Database Developer",
        goal="Construct and execute SQL queries based on requests.",
        backstory=dedent("""
            An expert in creating complex SQL queries for data retrieval and optimization.
        """),
        llm=llm,
        tools=[list_tables, tables_schema, execute_sql],
        allow_delegation=False,
    )

    data_analyst = Agent(
        role="Senior Data Analyst",
        goal="Analyze dataset statistics and summarize insights.",
        backstory=dedent("""
            An experienced data analyst who produces detailed, accurate analyses.
        """),
        llm=llm,
        allow_delegation=True,
    )

    report_writer = Agent(
        role="Senior Report Editor",
        goal="Write a detailed, clear report based on analysis.",
        backstory=dedent("""
            Known for creating concise, clear, and detailed executive summaries.
        """),
        llm=llm,
        allow_delegation=False,
    )

    # Define tasks
    thinking = Task(
        description="Determine creative ways to analyze the data.",
        expected_output="Identified analysis strategies and insights.",
        agent=sql_dev,
    )

    extract_data = Task(
        description="Extract necessary data for analysis.",
        expected_output="Extracted database results.",
        agent=sql_dev,
    )

    analyze_data = Task(
        description="Perform statistical analysis on extracted data.",
        expected_output="Detailed analysis.",
        agent=data_analyst,
        context=[extract_data],
    )

    write_report = Task(
        description="Summarize analysis findings in report format.",
        expected_output="Markdown report.",
        agent=report_writer,
        context=[analyze_data],
    )

    crew = Crew(
        agents=[thinker, sql_dev, data_analyst, report_writer],
        tasks=[thinking, extract_data, analyze_data, write_report],
        process=Process.sequential,
        verbose=True,
        memory=False,
    )

    # Kick off the analysis process
    inputs = {
        "query": "Perform statistical comparisons and find insights on the data."
    }
    result = crew.kickoff(inputs=inputs)

    # Display the final report in Streamlit
    st.write("Analysis Result:")
    st.write(result)
