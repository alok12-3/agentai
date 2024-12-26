
# 🌟 Multi-Agent System for Market Research & AI Use Case Generation

An AI-powered multi-agent system designed to conduct market research and generate actionable AI/ML use cases for companies across diverse industries. This project leverages state-of-the-art tools and methodologies to deliver detailed insights, competitor analysis, and innovation recommendations.

---

## 📋 Project Details

### **Project Name:**  
Market Research & Use Case Generation Agent  

### **Project Links:**  
- **Deployed Application**: [AgentAI Web App](https://agentai-seven.vercel.app/)  
- **GitHub Repository**: [AgentAI Repository](https://github.com/alok12-3/agentai)  
- **Video Demonstration**: [Google Drive Video](https://drive.google.com/drive/folders/1AkSW9s8zyjP99IRCXzHySHMEzNGr6fjY?usp=drive_link)

---

## 🛠️ System Architecture  

The system is built on a **multi-agent architecture**, where each agent is responsible for a specialized task to ensure high-quality insights.  

### **Agents and Their Roles:**  
1. **Research Agent**  
   - **Goal**: Analyze the company's industry and focus areas.  
   - **Tools**: Serper API for advanced web search and Gemini LLM (low temperature) for precise data processing.  
   - **Output**: Detailed industry report with references.  

2. **Competitor Analysis Agent**  
   - **Goal**: Identify and evaluate competitors' positioning.  
   - **Tools**: Serper API and Gemini LLM.  
   - **Output**: Comparative report on competitors' strengths and weaknesses.  

3. **Innovation Agent**  
   - **Goal**: Propose innovative AI/ML use cases for the target company.  
   - **Tools**: Industry trend analysis and Gemini LLM.  
   - **Output**: Recommendations for AI/ML applications to improve operations and customer experience.  

4. **Report Writing Agent**  
   - **Goal**: Compile insights into a structured report.  
   - **Tools**: Aggregates outputs from all agents.  
   - **Output**: PDF report with sections for industry overview, competitor analysis, and AI/ML use cases.

---

## 🌐 Workflow and Implementation  

### **Workflow:**  
1. **User Input**: User submits the company name via the React-based web app.  
2. **Agent Processing**:  
   - Research Agent generates the industry overview.  
   - Competitor Analysis Agent evaluates competitors.  
   - Innovation Agent recommends AI/ML use cases.  
3. **Report Compilation**: Report Writing Agent creates a structured PDF report.  
4. **Output**: The final PDF report is downloadable and contains:  
   - **Industry Overview**  
   - **Competitor Analysis**  
   - **AI/ML Recommendations**  

### **Backend:**  
- Flask API for managing agent interactions and generating reports.  

### **Frontend:**  
- React-based application for user interactions and report retrieval.  

---

## 🔧 Tools and Technologies  

| **Category**            | **Technologies Used**                                |
|-------------------------|-----------------------------------------------------|
| **Agent Framework**     | CrewAI                                              |
| **Language Model**      | Gemini LLM (gemini-1.5-flash)                        |
| **Search Tool**         | Serper API                                          |
| **Backend**             | Flask                                               |
| **Frontend**            | React.js                                            |
| **Document Generation** | PDF libraries for structured report creation         |

---

## 📂 File Structure  

```plaintext
.
├── frontend/                # React frontend
├── backend/                 # Flask backend
├── reports/                 # Generated PDF reports
├── README.md                # Project documentation
```

---

## 🚀 Quick Start Guide  

### 📋 Prerequisites  
- Install [Python](https://www.python.org/), [Flask](https://flask.palletsprojects.com/), and required Python libraries.  
- Install [Node.js](https://nodejs.org/) and npm.

### 🖥️ Running Locally  

1. **Clone the repository**:  
   ```bash
   git clone https://github.com/alok12-3/agentai
   cd agentai
   ```

2. **Backend Setup**:  
   ```bash
   cd backend
   pip install -r requirements.txt
   flask run
   ```

3. **Frontend Setup**:  
   ```bash
   cd frontend
   npm install
   npm start
   ```

4. Access the app on `http://localhost:3000`.

---

## 📝 Results and Conclusion  

- **Achievements**:  
  - Generated comprehensive reports for market research and AI/ML use cases.  
  - Enabled efficient information retrieval using Serper and Gemini LLM.  
  - Improved accuracy through specialized agent roles.  

- **Impact**:  
  - Demonstrated the feasibility of a multi-agent architecture for automating complex tasks.  
  - Delivered actionable insights to enhance operational efficiencies and customer experience.

---

## 🤝 Acknowledgments  

- **CrewAI**: For enabling multi-agent system implementation.  
- **Gemini LLM**: For its precise language processing capabilities.  
- **Serper API**: For advanced web search integration.  
- **Flask and React**: For seamless backend and frontend development.  

---

**⭐ Star this repository if you found it helpful!**  
```
