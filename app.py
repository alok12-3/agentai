# # app.py
# import streamlit as st
# import os
# from crewai_tools import SerperDevTool
# from crewai import Agent, Task, Crew
# from langchain_google_genai import ChatGoogleGenerativeAI

# # Set API Keys
# SERPER_API_KEY = "0021206eb1302a4b366ff55571f99f0245f7b21d"
# GOOGLE_API_KEY = "AIzaSyAu7N_nUyoDcH_c0zultQI_tHJuxTKo3g4"
# os.environ['SERPER_API_KEY'] = SERPER_API_KEY
# os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY

# # Initialize tools
# search_tool = SerperDevTool()






# # Take industry input from the user
# company = input("Enter the company you want the agent to research: ")

# # Initialize the Agent with the user-defined industry
# researcher = Agent(
#     role=f"Senior industry expert",
#     goal=f"investigate the segment of company and industry it is working in (e.g., Automotive, Manufacturing, Finance, Retail, Healthcare, etc.",
#     backstory=f"""You work at a prominent research institute.
#     Your expertise lies in sourcing and analyzing information on AI technologies used in the industry. You excel at breaking down complex data and presenting it in an accessible and insightful manner.""",
#     verbose=True,
#     allow_delegation=False,
#     tools=[search_tool],
#     llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.1),
#     # max_rpm=20,
#     # max_iter=15
# )


# researcher2 = Agent(
#     role=f"Senior competitor Research Analyst",
#     goal=f"you have to find all the competitors of the {company} and prepare a report where your {company} stands as compared to its competitors.",
#     backstory=f"""You work at a prominent {company} and your expertise lies in  analyzing the competitors information on AI technologies used by competitors of {company}. You excel at breaking down complex data and presenting it in an accessible and insightful manner.""",
#     verbose=True,
#     allow_delegation=False,
#     tools=[search_tool],
#     llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature = 0.1),
#     # max_rpm=20,
#     # max_iter=15
# )


# innovator = Agent(
#      role=f"you are very creative thinker who can make a report of where to use AI/Ml in {company} and what are its competitors are using AI/ML that the {company} should also use",
#     goal=f"make a report of where to use AI/Ml in {company} and what are its competitors are using AI/ML that the {company} should also use",
#     backstory=f"""You work at a prominent {company} and your expertise lies in  analyzing the competitors information on AI technologies used by competitors of {company} and suggest your {company} to use of AI/ML in yiur {company} to enhace your efficiency. You excel at breaking down complex data and presenting it in an accessible and insightful manner.""",
#     verbose=True,
#     allow_delegation=False,
#     tools=[search_tool],
#     llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.8),
#     # max_rpm=20,
#     # max_iter=15
# )


# writer = Agent(
#     role = "Expert report Writer",
#     goal = f"make a report in three sections. first section is  Industry of the {company} and  the company’s key offerings and strategic focus areas (e.g., operations, supply chain, customer experience, etc.). A vision and product information on the industry.   now second section contains the competitor analysis of the {company} and what they are doing in feil of AI/ML to optimize therir profit or production. now in third section suggest the use of AI/ML in {company} for betterment of {company} in terms of profit production or optimisation or environmental benefits",
#     backstory = """You are a well-respected content strategist with a knack for creating engaging and informative articles.
#     Your expertise lies in transforming complex automobiles and AI concepts into clear, compelling narratives that are easily understood by a broad audience.""",
#     verbose = True,
#     allow_delegation = True,
#     llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7),
#     # max_rpm=20
# )



# import os

# # Ensure the directory exists for saving output files
# def ensure_directory_exists(directory):
#     os.makedirs(directory, exist_ok=True)

# # Define the directory path for the company files
# company_directory = f"{company}/file"
# ensure_directory_exists(company_directory)

# # Now define the tasks with the updated output file paths
# task1 = Task(
#     description=(
#         f"Identify the industry where the {company} works."
#         f"what is the product and vision of {company}"
#         f"Focus on the vision of the {company}"
#         f"Identify the {company}’s key offerings and strategic focus areas."
#         "its market opportunities, and potential risks."
#     ),
#     expected_output=f"A comprehensive 1 paragraph long report on about the {company} its industry vision and product. a reference website link should be added at last",
#     tools=[search_tool],
#     agent=researcher,
#     output_file=f'{company_directory}/report_about.md'
# )

# task2 = Task(
#     description=(
#         f"make a competitor analysis report for the {company}"
#         f"Focus on what {company} is doing better as compared to its competitor and what its competitor is doing better."
#     ),
#     expected_output=f"A competitor analysis report with all major competitors of {company}.a reference website link should be added at last",
#     tools=[search_tool],
#     agent=researcher2,
#     async_execution=False,
#     output_file=f'{company_directory}/report_competition.md'
# )

# task3 = Task(
#     description=(
#         f"make a report for the {company}"
#         f"Focus on where the {company} can use AI/ML to enhance the positive outcome of company and also help the {company} to be ahead of its competitors."
#     ),
#     expected_output=f"A report with the use case of AI/ML in {company}.a reference website link should be added at last",
#     tools=[search_tool],
#     agent=innovator,
#     async_execution=False,
#     output_file=f'{company_directory}/report_use_of_ai.md'
# )


# task5 = Task(
#     description=(
#         f"first make a table of contents of the report then"
#         f"make a detailed combined report with three sections: first is the report generated by researcher that is about {company}, then the report generated by researcher2 that is {company} and its competitors, and third is the use of AI/ML in {company}."
#         f"also add the links of references at the end of the report."
#     ),
#     expected_output=f"A detailed and extensive report for {company}.",
#     agent=writer,
#     async_execution=False,
#     output_file=f'{company_directory}/report_temp_sam.md'
# )




# # # Set up the Crew
# # crew = Crew(
# #     agents=[researcher, writer],
# #     tasks=[task1, task2],
# #     verbose=1
# # )

# crew = Crew(
#     agents = [researcher, researcher2, innovator, writer],
#     tasks = [task1, task2, task3, task5],
#     verbose = 1,
# )






# # Streamlit UI
# st.title("Healthcare AI Research & Report Generation")
# st.write("This app uses AI agents to gather and summarize the latest advancements in AI technology for healthcare.")

# if st.button("Run Research and Generate Report"):
#     with st.spinner("Working on tasks..."):
#         final = crew.kickoff()
    
#     st.write("**Research output**:")
#     st.write(final)  # Adjust if final output is structured differently


# from markdown2 import markdown
# from weasyprint import HTML

# # Sample text with markdown-style formatting
# api_response = final

# # Convert markdown text to HTML
# html_content = markdown(api_response)

# # Save the HTML content as a PDF
# pdf_path = f'{company_directory}/output.pdf'
# HTML(string=html_content).write_pdf(pdf_path)

# print(f"PDF saved as {pdf_path}")





# # # Define Agents
# # researcher = Agent(
# #     role="Senior Healthcare Research Analyst",
# #     goal="Investigate and report on the latest advancements in AI applications for the healthcare industry in 2024.",
# #     backstory="""You work at a prominent healthcare research institute. You excel at breaking down complex medical data and presenting it in an accessible and insightful manner.""",
# #     verbose=False,
# #     allow_delegation=False,
# #     tools=[search_tool],
# #     llm=ChatGoogleGenerativeAI(model="gemini-pro")
# # )

# # writer = Agent(
# #     role="Expert Healthcare Technology Writer",
# #     goal="Craft concise and informative articles summarizing the latest advancements in AI applications within the healthcare sector in 2024.",
# #     backstory="""You are a well-respected content strategist with a knack for creating engaging and informative articles.""",
# #     verbose=True,
# #     allow_delegation=True,
# #     llm=ChatGoogleGenerativeAI(model="gemini-pro")
# # )







# # Define Tasks
# # task1 = Task(
# #     description="Investigate the most recent breakthroughs in AI applications for healthcare.",
# #     expected_output="A detailed summary of the latest innovations in AI technology within the healthcare sector.",
# #     agent=researcher
# # )

# # task2 = Task(
# #     description="Compose a concise and informative article highlighting the latest innovations in AI applications for healthcare.",
# #     expected_output="An engaging and well-structured article on the recent advancements in AI technology for healthcare.",
# #     agent=writer
# # )




# app.py
import streamlit as st
import os
from crewai_tools import SerperDevTool
from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI
from markdown2 import markdown
from weasyprint import HTML

# Set API Keys
SERPER_API_KEY = "0021206eb1302a4b366ff55571f99f0245f7b21d"
GOOGLE_API_KEY = "AIzaSyAu7N_nUyoDcH_c0zultQI_tHJuxTKo3g4"
os.environ['SERPER_API_KEY'] = SERPER_API_KEY
os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY

# Initialize tools
search_tool = SerperDevTool()

# Streamlit UI
st.title("AI Research & Report Generation for Company")
st.write("This app uses AI agents to gather and summarize the latest advancements in AI technology for various industries.")

# Take company input from the user
company = st.text_input("Enter the company you want the agent to research:")

# Only run if the company name is provided
if company:
    # Initialize the Agent with the user-defined company
    researcher = Agent(
        role="Senior industry expert",
        goal=f"investigate the segment of company and industry it is working in (e.g., Automotive, Manufacturing, Finance, Retail, Healthcare, etc.",
        backstory="""You work at a prominent research institute.
        Your expertise lies in sourcing and analyzing information on AI technologies used in the industry. You excel at breaking down complex data and presenting it in an accessible and insightful manner. you also keeps the website reference for each facts and information""",
        verbose=True,
        allow_delegation=False,
        tools=[search_tool],
        llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.1),
    
    )

    researcher2 = Agent(
        role="Senior competitor Research Analyst",
        goal=f"find all the competitors of {company} and prepare a report where your {company} stands as compared to its competitors.",
        backstory=f"""You work at a prominent {company} and your expertise lies in analyzing competitors' information on AI technologies used by competitors of {company}. You excel at breaking down complex data and presenting it in an accessible and insightful manner. you also keeps the website reference for each facts and information""",
        verbose=True,
        allow_delegation=False,
        tools=[search_tool],
        llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.1),
     
    )

    innovator = Agent(
        role=f"You are a creative thinker who can make a report of where to use AI/ML in {company} and what competitors are using that {company} should also consider.",
        goal=f"Report on where to use AI/ML in {company} and AI/ML innovations used by competitors that the {company} should also adopt.",
        backstory=f"""You work at a prominent {company} and your expertise lies in analyzing AI technology in the industry, with a focus on opportunities for {company}. You excel at breaking down complex data and presenting it in an accessible and insightful manner. you also keeps the website reference for each facts and information""",
        verbose=True,
        allow_delegation=False,
        tools=[search_tool],
        llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.8),
        
    )

    writer = Agent(
        role="Expert report Writer",
        goal=f"Create a report in three sections: (1) Industry overview of {company}, (2) Competitor analysis, and (3) AI/ML recommendations for {company}.",
        backstory="You are a well-respected content strategist with a knack for creating engaging and informative articles.you also keeps the website reference for each facts and information",
        verbose=True,
        allow_delegation=True,
        llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7),
       
    )

    # Define output directory
    company_directory = f"{company}/file"
    os.makedirs(company_directory, exist_ok=True)

    # Define tasks
    task1 = Task(
        description=(
            f"Identify the industry where {company} operates, including its vision, products, key offerings, and strategic focus areas."
        ),
        expected_output=f"A comprehensive report about {company} with industry vision, products, and opportunities.all reference website link should be kept",
        tools=[search_tool],
        agent=researcher,
        output_file=f'{company_directory}/report_about.md'
    )

    task2 = Task(
        description=f"Competitor analysis report for {company}, highlighting strengths and weaknesses compared to competitors.",
        expected_output=f"Competitor analysis report with major competitors of {company}.all reference website link should be kept",
        tools=[search_tool],
        agent=researcher2,
        output_file=f'{company_directory}/report_competition.md'
    )

    task3 = Task(
        description=f"AI/ML use case report for {company} with potential applications and competitive insights.",
        expected_output=f"Use case report with AI/ML recommendations for {company}.all reference website link should be kept",
        tools=[search_tool],
        agent=innovator,
        output_file=f'{company_directory}/report_use_of_ai.md'
    )

    task5 = Task(
    description=(
        f"Create a combined detailed report with sections: (1) Overview of {company}, (2) Competitor analysis, and (3) AI/ML recommendations. "
        f"Also add all links of references at the end of the report and in between the report add link with numbers like [number] and at last with same serial number paste links at end of report."
    ),
    expected_output=f"Comprehensive report for {company}.",
    agent=writer,
    output_file=f'{company_directory}/report_temp_sam.md'
)


    # Set up the Crew
    crew = Crew(
        agents=[researcher, researcher2, innovator, writer],
        tasks=[task1, task2, task3, task5],
        verbose=1,
    )



# Trigger the research and report generation
if st.button("Run Research and Generate Report"):
    with st.spinner("Working on tasks..."):
        final = crew.kickoff()
 
    # Store output in session state to prevent reset on download
    st.session_state['final_output'] = final

# Display and download report if generated
if 'final_output' in st.session_state:
    # Convert to HTML for saving as PDF
    pdf_path = f'{company_directory}/output.pdf'
    HTML(string=st.session_state['final_output']).write_pdf(pdf_path)

    # Provide download button above the output
    with open(pdf_path, "rb") as pdf_file:
        st.download_button(
            label="Download Report as PDF",
            data=pdf_file,
            file_name=f"{company}_report.pdf",
            mime="application/pdf"
        )

    # Display the research output as it is
    st.write("**Research output:**")
    st.markdown(st.session_state['final_output'])






















    # if st.button("Run Research and Generate Report"):
#     with st.spinner("Working on tasks..."):
#         final = crew.kickoff()

#     # Store output in session state to prevent reset on download
#     st.session_state['final_output'] = final

# # Display and download report if generated
# if 'final_output' in st.session_state:
#     # Convert to HTML and save as PDF
#     html_content = markdown(st.session_state['final_output'])
#     pdf_path = f'{company_directory}/output.pdf'
#     HTML(string=html_content).write_pdf(pdf_path)

#     # Provide download button above the output
#     with open(pdf_path, "rb") as pdf_file:
#         st.download_button(
#             label="Download Report as PDF",
#             data=pdf_file,
#             file_name=f"{company}_report.pdf",
#             mime="application/pdf"
#         )

#     # Display the formatted research output below the download button
#     formatted_response = markdown(st.session_state['final_output'].replace("**", "**"))
#     st.write("**Research output:**")
#     st.markdown(formatted_response)

