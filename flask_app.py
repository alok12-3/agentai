from flask import Flask, request, jsonify, send_file
import os
from crewai_tools import SerperDevTool
from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI
from weasyprint import HTML

from flask_cors import CORS

app = Flask(__name__)
CORS(app)  


# Set API Keys
SERPER_API_KEY = "0021206eb1302a4b366ff55571f99f0245f7b21d"
GOOGLE_API_KEY = "AIzaSyAu7N_nUyoDcH_c0zultQI_tHJuxTKo3g4"
os.environ['SERPER_API_KEY'] = SERPER_API_KEY
os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY

# Initialize tools
search_tool = SerperDevTool()

@app.route('/generate_report', methods=['POST'])
def generate_report():
    data = request.json
    company = data['company']
    
    # Initialize agents
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
        backstory="You are a well-respected content strategist with a knack for creating engaging and informative articles. you also keeps the website reference for each facts and information",
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
        expected_output=f"A comprehensive report about {company} with industry vision, products, and opportunities. All reference website links should be kept.",
        tools=[search_tool],
        agent=researcher,
        output_file=f'{company_directory}/report_about.md'
    )

    task2 = Task(
        description=f"Competitor analysis report for {company}, highlighting strengths and weaknesses compared to competitors.",
        expected_output=f"Competitor analysis report with major competitors of {company}. All reference website links should be kept.",
        tools=[search_tool],
        agent=researcher2,
        output_file=f'{company_directory}/report_competition.md'
    )

    task3 = Task(
        description=f"AI/ML use case report for {company} with potential applications and competitive insights.",
        expected_output=f"Use case report with AI/ML recommendations for {company}. All reference website links should be kept.",
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
    final = crew.kickoff()

   #  # Convert to HTML for saving as PDF
   #  pdf_path = f'{company_directory}/output.pdf'
   #  HTML(string=final).write_pdf(pdf_path)

   #  return send_file(pdf_path, as_attachment=True)
    return jsonify({"report": final})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use PORT env variable, default to 5000
    app.run(host='0.0.0.0', port=port, debug=True)
