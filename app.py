import streamlit as st
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
from resume_parser import extract_resume_info
from resume_matcher import calculate_match_score
from db_manager import init_db, insert_resume, fetch_all_resumes
import re
import plotly.graph_objects as go
from wordcloud import WordCloud
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# === Slack setup ===
slack_token = "xoxb-8767528992406-8773988400517-CgVQWYbxQCOuKKoYOWmJuhml"
slack_channel = "#all-ai-resume-screen"  # Adjust if necessary
slack_client = WebClient(token=slack_token)

def send_slack_notification(message):
    try:
        response = slack_client.chat_postMessage(channel=slack_channel, text=message)
        if response["ok"]:
            return "✅ Slack notification sent!"
        else:
            return f"⚠️ Slack API Error: {response['error']}"
    except SlackApiError as e:
        return f"❌ Failed to send Slack notification: {e.response['error']}"

def extract_name_and_email(resume_text):
    name_pattern = r"(?i)(?<=Name:)[^\n]*"
    email_pattern = r"(?i)(?<=Email:)[^\n]*"
    name_match = re.search(name_pattern, resume_text)
    email_match = re.search(email_pattern, resume_text)
    name = name_match.group(0).strip() if name_match else "Unknown"
    email = email_match.group(0).strip() if email_match else "Unknown"
    return name, email

def main():
    st.set_page_config(page_title="AI Resume Matcher", layout="wide", page_icon="🤖")
    st.title("📝AI-Powered Resume Matcher")

    dark_mode = st.sidebar.checkbox("🌙 Dark Mode")
    if dark_mode:
        st.markdown("""
        <style>
        body {
            background-color: #121212;
            color: #E8E8E8;
        }
        .stButton>button {
            background-color: #333333;
            color: #ffffff;
        }
        .css-1q8dd3k {
            color: #E8E8E8;
        }
        .stTextInput>div>div>input {
            background-color: #333333;
            color: #E8E8E8;
        }
        </style>
        """, unsafe_allow_html=True)

    init_db()

    tab1, tab2 = st.tabs(["📤 Resume Matcher", "📊 Resume Dashboard"])

    with tab1:
        st.subheader("Upload Resume and Match with Job")
        resume_file = st.file_uploader("Upload Resume (PDF or TXT)", type=["pdf", "txt"], label_visibility="collapsed")
        job_description = st.text_area("Paste Job Description", height=200)

        if st.button("🚀 Analyze & Match"):
            if not resume_file or not job_description:
                st.warning("Please upload a resume and enter a job description.")
                return

            if resume_file.type == "application/pdf":
                import PyPDF2
                reader = PyPDF2.PdfReader(resume_file)
                resume_text = "\n".join([page.extract_text() for page in reader.pages])
            else:
                resume_text = resume_file.read().decode("utf-8")

            with st.spinner("🔍 Extracting resume info..."):
                extracted_resume_info = extract_resume_info(resume_text)
            st.subheader("📄 Extracted Resume Information:")
            st.code(extracted_resume_info)

            with st.spinner("📊 Matching with job description..."):
                match_score = calculate_match_score(extracted_resume_info, job_description)
            st.subheader("📈 Job Match Score:")
            st.success(match_score)

            name, email = extract_name_and_email(extracted_resume_info)
            score_val = match_score.split(":")[-1].strip().replace("%", "")
            insert_resume(name, email, score_val, job_description, resume_text)

            with st.spinner("📨 Sending to Slack..."):
                slack_message = f"""
                📄 *Extracted Resume Info:*
                {extracted_resume_info}

                📊 *Job Match Score:*
                {match_score}
                """
                slack_result = send_slack_notification(slack_message)
            st.info(slack_result)

    with tab2:
        st.subheader("📊 Resume Dashboard")
        data = fetch_all_resumes()

        if data:
            df = pd.DataFrame(data, columns=["ID", "Name", "Email", "Match Score", "Job Description", "Resume Text", "Timestamp"])
            df["Match Score"] = pd.to_numeric(df["Match Score"], errors='coerce')
            df = df.sort_values(by="Match Score", ascending=False)

            fig = px.bar(df, x="Name", y="Match Score", color="Match Score", title="Resume Match Scores", color_continuous_scale="Viridis")
            fig.update_layout(xaxis_title="Resume", yaxis_title="Match Score")
            st.plotly_chart(fig)

            wordcloud = WordCloud(width=800, height=400, background_color="white").generate(' '.join(df["Resume Text"]))
            st.image(wordcloud.to_array(), caption="Keyword Distribution in Resumes", use_container_width=True)

            fig_heatmap = go.Figure(data=go.Heatmap(z=df["Match Score"].values.reshape(1, -1), colorscale='Viridis', showscale=True))
            fig_heatmap.update_layout(title="Match Score Heatmap", xaxis_title="Resumes", yaxis_title="Score")
            st.plotly_chart(fig_heatmap)

            min_score = st.slider("Filter by Match Score", 0, 100, (0, 100), 1)
            df_filtered = df[(df['Match Score'] >= min_score[0]) & (df['Match Score'] <= min_score[1])]

            st.subheader("Filtered Resume Data")
            st.dataframe(df_filtered[["Name", "Email", "Match Score", "Timestamp"]])

            st.download_button(
                label="📥 Download Resume Data",
                data=df_filtered.to_csv(index=False),
                file_name="resume_data.csv",
                mime="text/csv"
            )
        else:
            st.info("No resume data available yet.")

if __name__ == "__main__":
    main()
