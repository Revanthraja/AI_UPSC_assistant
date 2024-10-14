import os
import re
import streamlit as st
import google.generativeai as genai

# Load environment variables

# Define action regex pattern
action_re = re.compile(r'^Action: (\w+): (.*)$')

# Define functions for actions using the Gemini API
def generate_study_plan(subjects, study_hours):
    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(
        f"Create a detailed UPSC study plan covering the subjects: {', '.join(subjects)} with {study_hours} hours of study per week."
    )
    return response.text

def suggest_material(subject):
    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(
        f"Recommend the best study materials and resources for {subject} in UPSC preparation, including books, online resources, and courses."
    )
    return response.text

def current_affairs_summary(duration):
    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(
        f"Summarize the key current affairs for the last {duration}, focusing on topics relevant for UPSC."
    )
    return response.text

def motivational_quote():
    response = genai.GenerativeModel("gemini-1.5-flash").generate_content(
        "Provide a motivational quote specifically tailored for UPSC aspirants."
    )
    return response.text

# Mapping actions to functions
known_actions = {
    "generate_study_plan": generate_study_plan,
    "suggest_material": suggest_material,
    "current_affairs_summary": current_affairs_summary,
    "motivational_quote": motivational_quote
}

# Chatbot class to handle conversation
class Chatbot:
    def __init__(self, system=""):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({"role": "system", "content": system})
    
    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result
    
    def execute(self):
        prompt = "\n".join([f'{msg["role"]}: {msg["content"]}' for msg in self.messages])
        model = genai.GenerativeModel('gemini-1.5-flash')
        raw_response = model.generate_content(prompt)
        return raw_response.text

# Query function
def query(question, max_turns=5):
    bot = Chatbot(prompt)
    next_prompt = question
    i = 0
    query_result = ""
    while i < max_turns:
        i += 1
        result = bot(next_prompt)
        query_result += result + "\n\n"
        actions = [action_re.match(a) for a in result.split('\n') if action_re.match(a)]
        if actions:
            # There is an action to run
            action, action_input = actions[0].groups()
            if action not in known_actions:
                raise Exception(f"Unknown action: {action}: {action_input}")
            observation = known_actions[action](action_input)
            query_result += f"Observation: {observation}\n\n"
            next_prompt = f"Observation: {observation}"
        else:
            break
    return query_result

# Prompt for the chatbot
prompt = """
You are a UPSC study assistant specialized in helping students prepare for the UPSC examination. You provide study plans, recommend study materials, current affairs summaries, and motivational support. You are knowledgeable about the following UPSC topics:

1. General Studies (Prelims and Mains): 
    - History of India and Indian National Movement
    - Geography: Physical, Social, and Economic Geography of India and the World
    - Polity and Governance: Constitution, Political System, Panchayati Raj, Public Policy
    - Economic and Social Development: Sustainable Development, Poverty, Inclusion
    - Environment and Ecology
    - General Science
    - Current Events of National and International Importance

2. Optional Subjects: 
    - Geography, History, Political Science, Public Administration, Sociology, Psychology, and others

3. Essay Writing: 
    - Tips and strategies for writing effective essays for the UPSC exam.

4. Current Affairs: 
    - Important events, government policies, and international relations.

Your available actions are:
generate_study_plan:
e.g. generate_study_plan: Indian Polity, History
Generates a study plan based on the selected subjects and available study hours.
suggest_material:
e.g. suggest_material: Geography
Suggests study materials for the selected subject.
current_affairs_summary:
e.g. current_affairs_summary: Last 1 month
Summarizes the current affairs for a specified duration.
motivational_quote:
e.g. motivational_quote:
Returns a motivational quote for UPSC aspirants.
"""

# Streamlit UI
st.sidebar.title("Settings")

# Input for Google API Key in the sidebar
google_api_key = st.sidebar.text_input("Enter your Google API Key:", type="password")

# Store the API key in the environment variable if provided
if google_api_key:
    os.environ['GOOGLE_API_KEY'] = google_api_key
    genai.configure(api_key=google_api_key)  # Reconfigure the API with the new key

# Main app title
st.title("UPSC Study Assistant")

# Multiple select box for subjects
subjects = st.multiselect(
    "Select subjects you want to study:",
    options=[
        "History of India", "Indian National Movement", "Geography", "Polity and Governance",
        "Economic and Social Development", "Environment and Ecology", "General Science",
        "Current Events", "Optional Subject - Geography", "Optional Subject - Political Science"
    ],
    default=["History of India"]
)


# Input for study hours
study_hours = st.number_input("Enter total study hours per week:", min_value=1, value=10)

# Duration for current affairs summary
current_affairs_duration = st.selectbox(
    "Select duration for current affairs summary:",
    options=["Last 1 week", "Last 1 month", "Last 3 months", "Last 6 months"]
)

# Optional user input
user_input = st.text_input("Optional: Enter additional question or clarification:")

if st.button("Generate Response"):
    # If user input is empty, auto-generate based on selected options
    if not user_input:
        question = "I need help with the following:\n"
        if subjects:
            question += f"Generate a study plan for {', '.join(subjects)} with {study_hours} study hours per week.\n"
        
        if current_affairs_duration:
            question += f"Summarize current affairs for {current_affairs_duration}.\n"

        response = query(question)
    else:
        # If user input is provided, append it to the selected options
        response = query(user_input)
    
    # Display the response
    st.markdown("### Response:")
    st.markdown(response)

# Display motivational quote if requested
if st.button("Get a Motivational Quote"):
    quote = motivational_quote()
    st.markdown("### Motivational Quote:")
    st.markdown(quote)
