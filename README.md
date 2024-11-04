Market Research & Use Case Generation Agent
The Market Research & Use Case Generation Agent is an AI-powered application designed to assist companies in identifying relevant market insights and proposing strategic AI/ML implementations. This tool leverages multi-agent architecture to generate comprehensive reports on industry trends, competitor analysis, and potential AI/ML use cases. Built with Flask on the backend and React for the frontend, this project provides users with actionable insights and downloadable reports in PDF format.

Demo
The project is live at: agentai-seven.vercel.app

Features
Multi-Agent System: Includes agents for industry research, competitor analysis, AI/ML innovation, and report writing.
Comprehensive Report Generation: Produces detailed, multi-section reports in PDF format.
Automated Web Search: Uses CrewAI and Serper for real-time web data collection.
Interactive Frontend: Allows users to input company names and receive downloadable reports.
Cloud-Ready Deployment: Hosted on Vercel and connected to an AI processing backend.
Architecture
This project uses a modular architecture with four specialized agents:

Industry Research Agent: Gathers data on industry trends, company products, and mission/vision.
Competitor Analysis Agent: Provides insights on competitors and compares the target company with them.
Innovation Agent: Suggests AI/ML use cases and highlights innovations by competitors.
Report Writing Agent: Combines the above insights into a well-organized report.
The project leverages:

Flask for the backend API.
React for the frontend interface.
CrewAI with the Gemini language model and Serper web search for data aggregation.
WeasyPrint for HTML to PDF conversion.
CORS to allow cross-origin resource sharing between frontend and backend.
Installation
Prerequisites
Ensure you have the following installed:

Python 3.x
Node.js and npm
A Flask-compatible environment
API keys for Serper and Google Generative AI
Backend Setup
Clone the repository:

bash
Copy code
git clone https://github.com/username/MarketResearchAgent.git
cd MarketResearchAgent
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Set up environment variables:

Replace SERPER_API_KEY and GOOGLE_API_KEY in the code with your actual API keys or add them to an .env file if you prefer.
Run the Flask server:

bash
Copy code
python flask_app.py
Frontend Setup
Navigate to the frontend directory and install dependencies:

bash
Copy code
cd frontend
npm install
Start the React frontend:

bash
Copy code
npm run dev
Usage
Visit the frontend interface at agentai-seven.vercel.app.
Enter the name of the company you want to research and click Run Research and Generate Report.
Wait a few minutes as the agents process the request.
Download the generated PDF report when it becomes available.
Project Structure
bash
Copy code
MarketResearchAgent/
├── flask_app.py          # Flask backend application
├── frontend/             # React frontend application
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
└── .env.example          # Example environment variables



API Endpoints
POST /generate_report
Description: Generates a market research report for a specified company.

Request Body (JSON):

json
Copy code
{
  "company": "CompanyName"
}
Response: PDF file download of the report.

Tech Stack
Backend: Flask, CrewAI, Serper, Google Generative AI, WeasyPrint
Frontend: React, HTML, CSS
Hosting: Vercel
License
This project is licensed under the MIT License.

Acknowledgments
CrewAI
Serper
Langchain Google GenAI
Feel free to customize this README with additional information or instructions as needed. This structure will help guide users in understanding and setting up your project easily.
