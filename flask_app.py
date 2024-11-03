from flask import Flask, request, jsonify, send_file,make_response
import os
from crewai_tools import SerperDevTool
from crewai import Agent, Task, Crew
from langchain_google_genai import ChatGoogleGenerativeAI
from weasyprint import HTML
import markdown2 
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

    # Convert to HTML for saving as PDF
    pdf_path = f'{company_directory}/output.pdf'
    HTML(string=final).write_pdf(pdf_path)

    return send_file(pdf_path, as_attachment=True)
  


@app.route('/test_format', methods=['GET'])
def test_format():
    # Sample string with Markdown-like syntax
    test_string = (
        "## AI/ML Use Case Report for Asian Paints **Executive Summary:** This report explores potential applications of AI/ML for Asian Paints, focusing on enhancing operational efficiency, improving customer experience, and driving innovation. It also analyzes how competitors are leveraging AI/ML and recommends similar strategies for Asian Paints. **1. Industry Overview of Asian Paints** Asian Paints is a leading paint manufacturer in India, holding a dominant market share. According to various sources, their market share in 2023 was around 59%, making them the undisputed leader in the Indian paint industry. **Key Product Categories:** * **Decorative Paints:** This is their core business, accounting for a significant portion of their revenue. They offer a wide range of decorative paints for both interior and exterior applications, catering to residential, commercial, and industrial segments. * **Industrial Paints:** Asian Paints also manufactures industrial paints for various applications, including automotive, marine, and aerospace. * **Automotive Coatings:** They provide coatings for both OEM (original equipment manufacturer) and aftermarket applications. * **Specialty Coatings:** This category includes products like wood finishes, waterproofing solutions, and protective coatings. **Business Model:** Asian Paints operates a multi-pronged business model: * **Strong Brand Presence:** They have established a strong brand reputation in India, known for quality, innovation, and customer service. * **Extensive Distribution Network:** They have a vast distribution network across India, ensuring wide reach and accessibility to their products. * **Focus on Innovation:** Asian Paints invests heavily in research and development to introduce new products and technologies, catering to evolving customer needs. * **Strategic Acquisitions:** They have acquired several companies over the years, expanding their product portfolio and market reach. * **Digital Transformation:** Asian Paints is embracing digital technologies to enhance customer experience, improve operational efficiency, and drive growth. **Overall, Asian Paints is a dominant player in the Indian paint industry, with a strong brand, extensive distribution network, and a focus on innovation. Their business model has enabled them to achieve a significant market share and maintain their leadership position.** **2. Competitor Analysis** ## Asian Paints Competitor AI/ML Landscape Here's a breakdown of how Asian Paints' key competitors are leveraging AI/ML in the Indian paint market: **1. Berger Paints:** * **AI-powered Predictive Maintenance:** Berger Paints is using AI to predict equipment failures and optimize maintenance schedules, reducing downtime and improving operational efficiency. [1] * **Customer Experience Enhancement:** Berger Paints is using AI-powered chatbots and virtual assistants to provide instant customer support, answer queries, and personalize interactions. [2] * **Product Development:** Berger Paints is using AI to analyze customer feedback and market trends, enabling them to develop new paint formulations and colors that meet evolving consumer preferences. [3] **2. Kansai Nerolac Paints:** * **AI-driven Supply Chain Optimization:** Kansai Nerolac is using AI to optimize its supply chain, predicting demand fluctuations and ensuring timely delivery of raw materials and finished products. [4] * **Customer Segmentation and Targeting:** Kansai Nerolac is using AI to segment its customer base and tailor marketing campaigns to specific customer groups, improving marketing effectiveness and customer engagement. [5] * **Product Quality Control:** Kansai Nerolac is using AI-powered image recognition systems to inspect paint quality and identify defects, ensuring consistent product quality and reducing production errors. [6] **3. Akzo Nobel India:** * **AI-powered Color Matching:** Akzo Nobel is using AI to develop advanced color matching algorithms, enabling customers to easily find the perfect paint color for their projects. [7] * **Digital Marketing Optimization:** Akzo Nobel is using AI to optimize its digital marketing campaigns, targeting the right audience with the right message at the right time. [8] * **Sustainable Manufacturing:** Akzo Nobel is using AI to monitor and optimize its manufacturing processes, reducing energy consumption and waste generation, contributing to a more sustainable business model. [9] **4. Nippon Paint:** * **AI-powered Color Visualization:** Nippon Paint is using AI to create virtual paint simulations, allowing customers to visualize how different paint colors will look in their homes before making a purchase. [10] * **Personalized Customer Recommendations:** Nippon Paint is using AI to provide personalized paint recommendations based on customer preferences, project details, and past purchase history. [11] * **Smart Coatings Development:** Nippon Paint is using AI to develop innovative paint coatings with enhanced properties, such as self-cleaning, anti-fouling, and heat-resistant capabilities. [12] **5. Shalimar Paints:** * **AI-driven Inventory Management:** Shalimar Paints is using AI to optimize its inventory management, reducing storage costs and minimizing stockouts. [13] * **Customer Relationship Management (CRM):** Shalimar Paints is using AI-powered CRM systems to manage customer interactions, track purchase history, and provide personalized customer service. [14] * **Data-driven Decision Making:** Shalimar Paints is using AI to analyze market data and competitor insights, enabling them to make informed decisions about product pricing, marketing strategies, and new product development. [15] **Comparison with Asian Paints:** While Asian Paints has not publicly disclosed specific AI/ML initiatives, it is likely that they are exploring similar applications to their competitors. Asian Paints' strong focus on innovation and customer experience suggests they are likely investing in AI to enhance their operations and stay ahead of the competition. **Conclusion:** Asian Paints' competitors are actively using AI/ML to improve efficiency, customer satisfaction, and innovation. This highlights the growing importance of AI in the paint industry and underscores the need for Asian Paints to invest in AI to maintain its market leadership. **3. AI/ML Recommendations for Asian Paints** Based on my research, here are some specific AI/ML applications that Asian Paints can implement, drawing inspiration from competitor strategies: **Efficiency Enhancement:** * **Predictive Maintenance:** Asian Paints can leverage AI to predict equipment failures and schedule maintenance proactively. This can significantly reduce downtime, improve operational efficiency, and minimize maintenance costs. * **Example:** Dürr's  AI application identifies sources of defects and determines optimal maintenance schedules. [16] * **Optimized Production Planning:** AI can analyze historical data and real-time information to optimize production schedules, minimize waste, and improve resource utilization. * **Example:** Asian Paints itself uses AI-powered predictive tools to forecast demand, which likely helps them optimize production planning. [17] * **Automated Quality Control:** Implementing AI-powered vision systems can automate quality inspection processes, reducing human error and improving consistency. * **Example:** AI/ML algorithms can diagnose and prevent flaws in existing products with remarkable accuracy when provided with extensive image data. [18] **Customer Experience Enhancement:** * **Personalized Recommendations:** By analyzing customer purchase history and preferences, AI can recommend products and services tailored to individual needs. * **Example:** A paint company launched an AI-powered voice recognition tool that allows people to utter relevant phrases about their desired paint color and finish, generating personalized recommendations. [19] * **Virtual Paint Visualizers:** AI-powered tools can allow customers to virtually visualize paint colors on their walls, improving the decision-making process. * **Example:** Many companies have created AI paint visualizers that work with augmented reality to help people find the ideal interior and exterior paint colors. [20] * **Chatbots for Customer Support:** AI-powered chatbots can provide instant customer support, answer frequently asked questions, and resolve issues efficiently. **Innovation and Product Development:** * **New Color and Formula Development:** AI algorithms can analyze vast datasets of color and formula information to identify new color trends and develop innovative paint formulas. * **Example:** AI and ML algorithms are being used for data modeling about the properties of different types of paints (based on their chemical composition), which can aid in developing new formulas. [21] * **Smart Coatings Research:** AI can accelerate the research and development of smart coatings, such as self-cleaning, anti-fouling, or self-healing coatings. * **Example:** Large Language Models (LLM) are fueling AI innovations that could transform the paint and coatings sector, including the development of smart coatings. [22] * **Predictive Coating Performance:** AI can analyze data from real-world applications to predict coating performance and identify areas for improvement. * **Example:** Asian Paints leverages Sight Machine's digital twin technology to improve production efficiency and reduce batch cycle time. [23] By implementing these AI/ML applications, Asian Paints can gain a competitive advantage in the paint industry by improving efficiency, enhancing the customer experience, and driving innovation in product development. **References:** [1] https://www.bergerpaints.com/in/about-us/sustainability.html [2] https://www.bergerpaints.com/in/contact-us.html [3] https://www.bergerpaints.com/in/products.html [4] https://www.kansaineerolac.com/about-us/our-journey.html [5] https://www.kansaineerolac.com/about-us/our-journey.html [6] https://www.kansaineerolac.com/about-us/our-journey.html [7] https://www.akzonobel.com/en/about-us/our-history.html [8] https://www.akzonobel.com/en/about-us/our-history.html [9] https://www.akzonobel.com/en/about-us/our-history.html [10] https://www.nipponpaint.co.in/about-us/our-journey.html [11] https://www.nipponpaint.co.in/about-us/our-journey.html [12] https://www.nipponpaint.co.in/about-us/our-journey.html [13] https://www.shalimarpaints.com/about-us/our-journey.html [14] https://www.shalimarpaints.com/about-us/our-journey.html [15] https://www.shalimarpaints.com/about-us/our-journey.html [16] https://www.pcimag.com/articles/107753-bringing-artificial-intelligence-to-the-paint-shop [17] https://d3.harvard.edu/platform-digit/submission/asian-paints-indias-biggest-data-science-company-that-sells-paint/ [18] https://www.pirta.com/education/the-role-of-artificial-intelligence-and-machine-learning-in-the-paints-and-coatings-industry [19] https://www.pcimag.com/articles/112048-is-ai-the-catalyst-for-growth-in-coatings [20] https://www.pcimag.com/articles/112048-is-ai-the-catalyst-for-growth-in-coatings [21] https://www.datatobiz.com/blog/ai-in-paints-and-coatings-industry/ [22] https://www.polymerspaintcolourjournal.com/focus-on-smart-coatings-llm-fuels-ai-innovations-in-the-coatings-industry/ [23] https://sightmachine.com/customers/asian-paints/ .com/focus-on-smart-coatings-llm-fuels-ai-innovations-in-the-coatings-industry/ [23] https://sightmachine.com/customers/asian-paints/"
    )

    test_string = markdown2.markdown(test_string)

    # Create response with HTML content and set Content-Type to text/html
    response = make_response(test_string)
    response.headers['Content-Type'] = 'text/html'
    
    return response


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use PORT env variable, default to 5000
    app.run(host='0.0.0.0', port=port, debug=True)
