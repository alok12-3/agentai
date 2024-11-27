import os
from crewai_tools import SerperDevTool
from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI
from weasyprint import HTML
from markdown2 import markdown
from io import BytesIO

# Set API Keys
SERPER_API_KEY = "0021206eb1302a4b366ff55571f99f0245f7b21d"
GOOGLE_API_KEY = "AIzaSyAu7N_nUyoDcH_c0zultQI_tHJuxTKo3g4"
os.environ['SERPER_API_KEY'] = SERPER_API_KEY
os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY

# Initialize tools
search_tool = SerperDevTool()

def generate_report(company):
    # Initialize agents
    researcher = Agent(
        role="Senior industry expert",
        goal=f"investigate the segment of {company} and its industry also find the products offered by {company} and vision and mission of the {company}",
        backstory="""You work at a prominent research institute. Your expertise lies in analyzing information about industry and finding basic details about the {company} and analyzing its industry and vision and mission of {company} along with their products. You excel at breaking down complex data and presenting it in an accessible and insightful manner.""",
        verbose=True,
        allow_delegation=False,
        tools=[search_tool],
        llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.1),
    )

    researcher2 = Agent(
        role="Senior Competitor Research Analyst",
        goal=f"find all the competitors of {company} and prepare a report on where {company} stands as compared to its competitors.",
        backstory=f"""You work at {company} and specialize in competitor analysis with a focus on AI technologies used by competitors. You excel at breaking down complex data and presenting it in an accessible and insightful manner.""",
        verbose=True,
        allow_delegation=False,
        tools=[search_tool],
        llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.1),
    )

    innovator = Agent(
        role=f"AI/ML innovation expert for {company}",
        goal=f"Report on where to use AI/ML in {company} and AI/ML innovations used by competitors that {company} should consider.",
        backstory=f"""Expert in analyzing AI technology in the industry, with a focus on opportunities for {company}. Skilled at presenting data accessibly and insightfully.""",
        verbose=True,
        allow_delegation=False,
        tools=[search_tool],
        llm=ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.8),
    )

    writer = Agent(
        role="Expert report writer",
        goal=f"Create a report in three sections: (1) Industry overview of {company}, (2) Competitor analysis, and (3) AI/ML recommendations for {company}.",
        backstory="A content strategist with a knack for creating engaging and informative reports.",
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
        expected_output=f"A comprehensive report about {company} with industry vision, products, and opportunities.",
        tools=[search_tool],
        agent=researcher,
    )

    task2 = Task(
        description=f"Competitor analysis report for {company}, highlighting strengths and weaknesses compared to competitors.",
        expected_output=f"Competitor analysis report with major competitors of {company}.",
        tools=[search_tool],
        agent=researcher2,
    )

    task3 = Task(
        description=f"AI/ML use case report for {company} with potential applications and competitive insights.",
        expected_output=f"Use case report with AI/ML recommendations for {company}.",
        tools=[search_tool],
        agent=innovator,
    )

    task4 = Task(
        description=(
            f"Create a combined detailed report with sections: (1) Overview of {company}, (2) Competitor analysis, and (3) AI/ML recommendations."
        ),
        expected_output=f"Comprehensive report for {company}.",
        agent=writer,
    )

    # Set up the Crew
    crew = Crew(
        agents=[researcher, researcher2, innovator, writer],
        tasks=[task1, task2, task3, task4],
        verbose=True,
    )

    # Trigger the research and report generation
    final = crew.kickoff()
    
    finalstr = markdown(final)
    pdf_buffer = BytesIO()
    HTML(string=finalstr).write_pdf(pdf_buffer)
    pdf_buffer.seek(0)

    # Save the PDF
    with open(f"{company}_report.pdf", "wb") as f:
        f.write(pdf_buffer.read())
    print(f"Report for {company} generated and saved as {company}_report.pdf.")

# Example usage
if __name__ == '__main__':
    company_name = "ExampleCompany"  # Set your company name
    generate_report(company_name)
