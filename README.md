# UPSC Study Assistant

The UPSC Study Assistant is a Streamlit-based AI-powered tool designed to help UPSC aspirants prepare for the exam. It provides personalized study plans, recommended study materials, current affairs summaries, and motivational support to make the UPSC preparation journey easier.

## Features

1. **Personalized Study Plans**: Generate a study plan based on selected subjects and weekly study hours.
2. **Study Material Suggestions**: Get recommendations for the best books, online courses, and resources for various UPSC subjects.
3. **Current Affairs Summaries**: Stay updated with key current affairs for a specified duration.
4. **Motivational Quotes**: Get motivational quotes tailored specifically for UPSC aspirants.
5. **Flexible Query System**: Input custom queries for more personalized assistance.

## Setup Instructions

### Prerequisites

- Python 3.10 or higher
- An active Google API key for the Gemini AI model

### Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/your-username/upsc-study-assistant.git
    cd upsc-study-assistant
    ```

2. **Create a Python Virtual Environment**:
    ```bash
    python3 -m venv myenv
    source myenv/bin/activate  # On Windows: myenv\Scripts\activate
    ```

3. **Install Required Packages**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Run the Streamlit App**:
    ```bash
    streamlit run upsc_study_assistant.py
    ```

5. **Open the App in Your Browser**:
   The app will automatically open in your default web browser. If it doesn't, navigate to `http://localhost:8501`.

### Configuration

1. **Google API Key**: 
   - Enter your Google API key in the Streamlit sidebar when prompted. The app requires this key to use the Gemini AI model.

## File Structure

- `upsc_study_assistant.py`: The main code for the Streamlit app.
- `README.md`: Instructions for setting up and running the app.
- `requirements.txt`: List of dependencies.

## Troubleshooting

- If you encounter the error `StreamlitAPIException: Every Multiselect default value must exist in options`, ensure that the default value in the `st.multiselect` widget is part of the options.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Gemini](https://gemini.com) for providing AI models.
- [Streamlit](https://streamlit.io) for making it easy to create data apps.
