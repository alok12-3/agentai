# from flask import Flask, request, render_template, jsonify
# import pandas as pd
# import sqlite3
# import json
# import os
# from pathlib import Path
# from textwrap import dedent

# from crewai import Agent, Crew, Process, Task
# from crewai_tools import tool
# from langchain_community.tools.sql_database.tool import (
#     InfoSQLDatabaseTool,
#     ListSQLDatabaseTool,
#     QuerySQLCheckerTool,
#     QuerySQLDataBaseTool,
# )
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_community.utilities.sql_database import SQLDatabase

# from flask_cors import CORS
# from io import BytesIO

# app = Flask(__name__)
# CORS(app)  



# # Initialize the required LLM and SQL tools
# llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key="AIzaSyAu7N_nUyoDcH_c0zultQI_tHJuxTKo3g4")
# db = SQLDatabase.from_uri("sqlite:///salaries.db")

# # Define custom tools for database interactions
# @tool("list_tables")
# def list_tables() -> str:
#     """List the available tables in the database"""
#     return ListSQLDatabaseTool(db=db).invoke("")

# @tool("tables_schema")
# def tables_schema(tables: str) -> str:
#     """Retrieve schema and sample rows for specific tables"""
#     tool = InfoSQLDatabaseTool(db=db)
#     return tool.invoke(tables)

# @tool("execute_sql")
# def execute_sql(sql_query: str) -> str:
#     """Execute a SQL query and return results"""
#     return QuerySQLDataBaseTool(db=db).invoke(sql_query)

# @tool("check_sql")
# def check_sql(sql_query: str) -> str:
#     """Check if SQL query is correct before executing"""
#     return QuerySQLCheckerTool(db=db, llm=llm).invoke({"query": sql_query})

# # Define agents and tasks
# thinker = Agent(
#     role="Senior Data Scientist",
#     goal="Identify relationships and insights in data, then delegate SQL tasks.",
#     backstory=dedent("A creative data scientist who discovers new insights by exploring data relationships."),
#     llm=llm,
#     tools=[list_tables, tables_schema, execute_sql, check_sql],
#     allow_delegation=False,
# )

# sql_dev = Agent(
#     role="Senior Database Developer",
#     goal="Construct and execute SQL queries based on requests.",
#     backstory=dedent("An expert in creating complex SQL queries for data retrieval and optimization."),
#     llm=llm,
#     tools=[list_tables, tables_schema, execute_sql],
#     allow_delegation=False,
# )

# data_analyst = Agent(
#     role="Senior Data Analyst",
#     goal="Analyze dataset statistics and summarize insights.",
#     backstory=dedent("An experienced data analyst who produces detailed, accurate analyses."),
#     llm=llm,
#     allow_delegation=True,
# )

# report_writer = Agent(
#     role="Senior Report Editor",
#     goal="Write a detailed, clear report based on analysis.",
#     backstory=dedent("Known for creating concise, clear, and detailed executive summaries."),
#     llm=llm,
#     allow_delegation=False,
# )

# thinking = Task(
#     description="Determine creative ways to analyze the data.",
#     expected_output="Identified analysis strategies and insights.",
#     agent=sql_dev,
# )

# extract_data = Task(
#     description="Extract necessary data for analysis.",
#     expected_output="Extracted database results.",
#     agent=sql_dev,
# )

# analyze_data = Task(
#     description="Perform statistical analysis on extracted data.",
#     expected_output="Detailed analysis.",
#     agent=data_analyst,
#     context=[extract_data],
# )

# write_report = Task(
#     description="Summarize analysis findings in report format.",
#     expected_output="Markdown report.",
#     agent=report_writer,
#     context=[analyze_data],
# )

# crew = Crew(
#     agents=[thinker, sql_dev, data_analyst, report_writer],
#     tasks=[thinking, extract_data, analyze_data, write_report],
#     process=Process.sequential,
#     verbose=True,
#     memory=False,
# )

# @app.route('/')
# def upload_file():
#     return render_template('upload.html')  # Create upload.html with file upload form

# @app.route('/upload', methods=['POST'])
# def upload_csv():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file uploaded'}), 400
#     uploaded_file = request.files['file']
#     if uploaded_file.filename == '':
#         return jsonify({'error': 'No file selected'}), 400

#     # Load the CSV file into a pandas DataFrame
#     df = pd.read_csv(uploaded_file)
    
#     # Convert DataFrame to SQLite database
#     connection = sqlite3.connect("salaries.db")
#     df.to_sql(name="salaries", con=connection, if_exists="replace", index=False)
#     connection.close()

#     # Run analysis process
#     inputs = {"query": "Perform statistical comparisons and find insights on the data."}
#     result = crew.kickoff(inputs=inputs)

#     return jsonify({"message": "CSV data has been converted to SQLite database and loaded into table 'salaries'.", "analysis_result": result})

# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, request, render_template, jsonify
import pandas as pd
import sqlite3
import json
import os
from pathlib import Path
from textwrap import dedent

from crewai import Agent, Crew, Process, Task
from crewai_tools import tool
from langchain_community.tools.sql_database.tool import (
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
    QuerySQLCheckerTool,
    QuerySQLDataBaseTool,
)
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities.sql_database import SQLDatabase

from flask_cors import CORS
from io import BytesIO

app = Flask(__name__)
CORS(app)  



# Initialize the required LLM and SQL tools
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key="AIzaSyAu7N_nUyoDcH_c0zultQI_tHJuxTKo3g4")
db = SQLDatabase.from_uri("sqlite:///salaries.db")

# # Define custom tools for database interactions
# @tool("list_tables")
# def list_tables() -> str:
#     """List the available tables in the database"""
#     return ListSQLDatabaseTool(db=db).invoke("")


# @tool("tables_schema")
# def tables_schema(tables: str) -> str:
#     """
#     Input is a comma-separated list of tables, output is the schema and sample rows
#     for those tables. Be sure that the tables actually exist by calling `list_tables` first!
#     Example Input: table1, table2, table3
#     """
#     tool = InfoSQLDatabaseTool(db=db)
#     return tool.invoke(tables)



# @tool("execute_sql")
# def execute_sql(sql_query: str) -> str:
#     """Execute a SQL query against the database. Returns the result"""
#     return QuerySQLDataBaseTool(db=db).invoke(sql_query)


# @tool("check_sql")
# def check_sql(sql_query: str) -> str:
#     """
#     Use this tool to double check if your query is correct before executing it. Always use this
#     tool before executing a query with `execute_sql`.
#     """
#     return QuerySQLCheckerTool(db=db, llm=llm).invoke({"query": sql_query})


# Define custom tools for database interactions
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


sql_dev = Agent(
    role="Senior Database Developer",
    goal="Construct and execute SQL queries based on a request",
    backstory=dedent(
        """
        You are an experienced database engineer who is master at creating efficient and complex SQL queries.
        You have a deep understanding of how different databases work and how to optimize queries.
        Use the `list_tables` to find available tables.
        Use the `tables_schema` to understand the metadata for the tables.
        Use the `execute_sql` to check your queries for correctness.
        Use the `check_sql` to execute queries against the database.
    """
    ),
    llm=llm,
    tools=[list_tables, tables_schema, execute_sql, check_sql],
    allow_delegation=False,
    max_iter=100,
    max_rpm=30,
)



data_analyst = Agent(
    role="Senior Data Analyst",
    goal="You receive data from the database developer and analyze it",
    backstory=dedent(
        """
        You have deep experience with analyzing datasets using Python.
        Your work is always based on the provided data and is clear,
        easy-to-understand and to the point. You have attention
        to detail and always produce very detailed work (as long as you need).
    """
    ),
    llm=llm,
    allow_delegation=False,
    max_iter=50,
    max_rpm=30,
)



report_writer = Agent(
    role="Senior Report Editor",
    goal="Write an executive summary type of report based on the work of the analyst",
    backstory=dedent(
        """
        Your writing still is well known for clear and effective communication.
        You always summarize long texts into bullet points that contain the most
        important details.
        """
    ),
    llm=llm,
    allow_delegation=False,
    max_iter=50,
    max_rpm=30,
)


extract_data = Task(
    description="Extract data that is required for the query {query}.",
    expected_output="Database result for the query",
    agent=sql_dev,
)





analyze_data = Task(
    description="Analyze the data from the database and write an analysis for {query}.",
    expected_output="Detailed analysis text",
    agent=data_analyst,
    context=[extract_data],
)



write_report = Task(
    description=dedent(
        """
        Write a detailed report with acctual numerical data findings after analysis and based on that data write a report and teh report should be insightful with all the key findings. 
    """
    ),
    expected_output="Markdown report with acctual numerical data findings after analysis",
    agent=report_writer,
    context=[analyze_data],
)

crew = Crew(
    agents=[sql_dev, data_analyst, report_writer],
    tasks=[extract_data, analyze_data, write_report],
    process=Process.sequential,
    verbose=2,
    memory=False,
    output_log_file="crew.log",
)

@app.route('/')
def upload_file():
    return render_template('upload.html')  # Create upload.html with file upload form

@app.route('/upload', methods=['POST'])
def upload_csv():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(uploaded_file)
    
    # Convert DataFrame to SQLite database
    connection = sqlite3.connect("salaries.db")
    df.to_sql(name="salaries", con=connection, if_exists="replace", index=False)
    connection.close()

    # Run analysis process
    inputs = {"query": "How is the `Machine Learning Engineer` salary in USD is affected by remote positions"}
    result = crew.kickoff(inputs=inputs)

    return jsonify({"message": "CSV data has been converted to SQLite database and loaded into table 'salaries'.", "analysis_result": result})

if __name__ == '__main__':
    app.run(debug=True)


# @app.route('/upload', methods=['POST'])
# def upload_csv():
#     if 'file' not in request.files or 'query' not in request.form:
#         return jsonify({'error': 'File and query are required'}), 400
    
#     uploaded_file = request.files['file']
#     query = request.form['query']

#     if uploaded_file.filename == '':
#         return jsonify({'error': 'No file selected'}), 400

#     try:
#         # Load the CSV file into a pandas DataFrame
#         df = pd.read_csv(uploaded_file)
        
#         # Convert DataFrame to SQLite database
#         connection = sqlite3.connect("salaries.db")
#         df.to_sql(name="salaries", con=connection, if_exists="replace", index=False)
#         connection.close()
        
#         # Run analysis process with the provided query
#         inputs = {"query": query}
#         result = crew.kickoff(inputs=inputs)

#         return jsonify({"message": "CSV data has been converted to SQLite database and loaded into table 'salaries'.", "analysis_result": result})
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)


# from flask import Flask, request, render_template, jsonify
# import pandas as pd
# import sqlite3
# from io import BytesIO
# from textwrap import dedent

# from crewai import Agent, Crew, Process, Task
# from crewai_tools import tool
# from langchain_community.tools.sql_database.tool import (
#     InfoSQLDatabaseTool,
#     ListSQLDatabaseTool,
#     QuerySQLCheckerTool,
#     QuerySQLDataBaseTool,
# )
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_community.utilities.sql_database import SQLDatabase

# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

# # Initialize the required LLM and SQL tools
# llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key="AIzaSyAu7N_nUyoDcH_c0zultQI_tHJuxTKo3g4")
# db = SQLDatabase.from_uri("sqlite:///:memory:")

# # Define custom tools for database interactions
# # @tool("list_tables")
# # def list_tables() -> str:
# #     """List the available tables in the database"""
# #     return ListSQLDatabaseTool(db=db).invoke("")

# @tool("list_tables")
# def list_tables() -> str:
#     """List the available tables in the database"""
#     return ListSQLDatabaseTool(db=db).invoke("")

# # @tool("tables_schema")
# # def tables_schema(tables: str) -> str:
# #     """Retrieve schema and sample rows for specific tables"""
# #     tool = InfoSQLDatabaseTool(db=db)
# #     return tool.invoke(tables)

# @tool("tables_schema")
# def tables_schema(tables: str) -> str:
#     """
#     Input is a comma-separated list of tables, output is the schema and sample rows
#     for those tables. Be sure that the tables actually exist by calling `list_tables` first!
#     Example Input: table1, table2, table3
#     """
#     tool = InfoSQLDatabaseTool(db=db)
#     return tool.invoke(tables)


# # @tool("execute_sql")
# # def execute_sql(sql_query: str) -> str:
# #     """Execute a SQL query and return results"""
# #     return QuerySQLDataBaseTool(db=db).invoke(sql_query)


# @tool("execute_sql")
# def execute_sql(sql_query: str) -> str:
#     """Execute a SQL query against the database. Returns the result"""
#     return QuerySQLDataBaseTool(db=db).invoke(sql_query)

# # @tool("check_sql")
# # def check_sql(sql_query: str) -> str:
# #     """Check if SQL query is correct before executing"""
# #     return QuerySQLCheckerTool(db=db, llm=llm).invoke({"query": sql_query})

# @tool("check_sql")
# def check_sql(sql_query: str) -> str:
#     """
#     Use this tool to double check if your query is correct before executing it. Always use this
#     tool before executing a query with `execute_sql`.
#     """
#     return QuerySQLCheckerTool(db=db, llm=llm).invoke({"query": sql_query})





# # thinker = Agent(
# #     role="Senior Data Scientist",
# #     goal="Identify relationships and insights in data, then delegate SQL tasks.",
# #     backstory=dedent("A creative data scientist who discovers new insights by exploring data relationships."),
# #     llm=llm,
# #     tools=[list_tables, tables_schema, execute_sql, check_sql],
# #     allow_delegation=False,
# # )

# thinker = Agent(
#     role="Senior Data scientist",
#     goal="you read the data tables rows coloumns and try to guess pssible relatons between them which may give excieting insights then you ask sql_dev to write sql quiries and wive you results and you keep the results and forward the insights you got",
#     backstory=dedent(
#         """
#         you are very creative data scientist yu always find new way and relations in data to gain some insights. you first visualize the data and then madke thoughts what would work and dedicate tasks to sql_dev agent
#     """
#     ),
#     llm=llm,
#     tools=[list_tables, tables_schema, execute_sql,check_sql],
#     allow_delegation=False,
# )

# # sql_dev = Agent(
# #     role="Senior Database Developer",
# #     goal="Construct and execute SQL queries based on requests.",
# #     backstory=dedent("An expert in creating complex SQL queries for data retrieval and optimization."),
# #     llm=llm,
# #     tools=[list_tables, tables_schema, execute_sql],
# #     allow_delegation=False,
# # )
# sql_dev = Agent(
#     role="Senior Database Developer",
#     goal="Construct and execute SQL queries based on a request",
#     backstory=dedent(
#         """
#         You are an experienced database engineer who is master at creating efficient and complex SQL queries.
#         You have a deep understanding of how different databases work and how to optimize queries.
#         Use the `list_tables` to find available tables.
#         Use the `tables_schema` to understand the metadata for the tables.
#         Use the `execute_sql` to check your queries for correctness.
#         Use the `check_sql` to execute queries against the database.
#     """
#     ),
#     llm=llm,
#     tools=[list_tables, tables_schema, execute_sql],
#     allow_delegation=False,
# )

# # data_analyst = Agent(
# #     role="Senior Data Analyst",
# #     goal="Analyze dataset statistics and summarize insights.",
# #     backstory=dedent("An experienced data analyst who produces detailed, accurate analyses."),
# #     llm=llm,
# #     allow_delegation=True,
# # )

# data_analyst = Agent(
#     role="Senior Data Analyst",
#     goal="You receive data from the database developer and analyze it and find all statistics related to data mean median mode standard deviation distribution etc",
#     backstory=dedent(
#         """
#         You have deep experience with analyzing datasets using Python.
#         Your work is always based on the provided data and is clear,
#         easy-to-understand and to the point. You have attention
#         to detail and always produce very detailed work (as long as you need).
#     """
#     ),
#     llm=llm,
#     allow_delegation=True,
# )

# # report_writer = Agent(
# #     role="Senior Report Editor",
# #     goal="Write a detailed, clear report based on analysis.",
# #     backstory=dedent("Known for creating concise, clear, and detailed executive summaries."),
# #     llm=llm,
# #     allow_delegation=False,
# # )

# report_writer = Agent(
#     role="Senior Report Editor",
#     goal="Write an executive summary type of report based on the work of the analyst",
#     backstory=dedent(
#         """
#         Your writing still is well known for clear and effective communication.
#         You always summarize long texts into bullet points that contain the most
#         important details.
#         """
#     ),
#     llm=llm,
#     allow_delegation=False,
# )

# # thinking = Task(
# #     description="Determine creative ways to analyze the data.",
# #     expected_output="Identified analysis strategies and insights.",
# #     agent=sql_dev,
# # )

# thinking = Task(
#     description="think ways to analyze the data and find insights about data in very creative way {query}.",
#     expected_output="thoughts what to find in database and hat to do in database",
#     agent=thinker,
# )

# # extract_data = Task(
# #     description="Extract necessary data for analysis.",
# #     expected_output="Extracted database results.",
# #     agent=sql_dev,
# # )

# extract_data = Task(
#     description="Extract data that is required for the query {query}.",
#     expected_output="Database result for the query",
#     agent=sql_dev,
# )

# # analyze_data = Task(
# #     description="Perform statistical analysis on extracted data.",
# #     expected_output="Detailed analysis.",
# #     agent=data_analyst,
# #     context=[extract_data],
# # )

# analyze_data = Task(
#     description="Analyze the data from the database find mean median for all data find all types of statistics related to data and make report and write an analysis for {query}.",
#     expected_output="Detailed analysis text",
#     agent=data_analyst,
#     context=[extract_data],
# )

# # write_report = Task(
# #     description="Summarize analysis findings in report format.",
# #     expected_output="Markdown report.",
# #     agent=report_writer,
# #     context=[analyze_data],
# # )

# write_report = Task(
#     description=dedent(
#         """
#         Write a detailed report from the analysis.
#         .
#     """
#     ),
#     expected_output="Markdown report",
#     agent=report_writer,
#     context=[analyze_data],
# )

# crew = Crew(
#     agents=[thinker, sql_dev, data_analyst, report_writer],
#     tasks=[thinking, extract_data, analyze_data, write_report],
#     process=Process.sequential,
#     verbose=True,
#     memory=False,
# )

# @app.route('/')
# def upload_file():
#     return render_template('upload.html')  # Create upload.html with file upload form

# @app.route('/upload', methods=['POST'])
# def upload_csv():
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file uploaded'}), 400
#     uploaded_file = request.files['file']
#     if uploaded_file.filename == '':
#         return jsonify({'error': 'No file selected'}), 400

#     # Load the CSV file into a pandas DataFrame
#     csv_data = BytesIO(uploaded_file.read())
#     df = pd.read_csv(csv_data)
    
#     # Create an in-memory SQLite database and store the data
#     connection = sqlite3.connect(":memory:")
#     df.to_sql(name="salaries", con=connection, if_exists="replace", index=False)

#     # Run analysis process
#     inputs = {"query": "Perform statistical comparisons and find insights on the data."}
#     result = crew.kickoff(inputs=inputs)

#     connection.close()

#     return jsonify({"message": "CSV data has been processed in-memory and loaded into a temporary table 'salaries'.", "analysis_result": result})

# if __name__ == '__main__':
#     app.run(debug=True)
