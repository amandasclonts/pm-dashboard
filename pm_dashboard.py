import streamlit as st
import base64
from openai import OpenAI

client = OpenAI(api_key=st.secrets["openai"]["openai_api_key"])

st.set_page_config(page_title="AI Dashboard", layout="wide")

# Function to encode image in base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
        return f"data:image/jpeg;base64,{encoded}"

# Load and embed the image
encoded_logo = get_base64_image("logo.jpg")
st.markdown(
    f"""
    <div style='text-align: center;'>
        <img src="{encoded_logo}" style='width: 375px; margin-bottom: 10px;' />
        <h1 style='color: white; font-size: 36px;'>🧠 AI Tools Dashboard</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# Create tabbed layout
tabs = st.tabs(["Forecast AI", "Compliance Checker", "Summarizer", "Contract Parsing", "More Coming Soon"])


with tabs[0]:
    st.subheader("📈 Forecast AI")
    st.text_input("Enter project name:")
    st.button("Run Forecast")

with tabs[1]:
    st.subheader("📋 Compliance Checker")
    st.file_uploader("Upload civil plan PDF", type=["pdf"])
    st.button("Check Compliance")

with tabs[2]:
    st.subheader("📝 Document Summarizer")
    st.text_area("Paste text to summarize")
    st.button("Summarize")

with tabs[3]:  # Contract Parsing (AI)
    st.subheader("📂 Contract Parsing – AI Summary by Topic")

    uploaded_contract = st.file_uploader("Upload a contract PDF", type=["pdf"])

    topic_options = [
        "Liquidated Damages", "Payment Terms", "Delays", "Retention",
        "Schedule", "Scope of Work", "Contract Value", "Safety Requirements"
    ]
    selected_topic = st.selectbox("Choose a topic to analyze:", topic_options)

    if uploaded_contract and selected_topic:
        if st.button("Run Full AI Parsing"):
            with st.spinner("Analyzing contract with OpenAI..."):
                import fitz  # PyMuPDF

                with fitz.open(stream=uploaded_contract.read(), filetype="pdf") as doc:
                    full_text = "\n".join([page.get_text() for page in doc])

                prompt = f"""
You are a contract analysis assistant. Summarize everything in this construction contract related to the topic: **{selected_topic}**.

Only focus on the parts of the contract that discuss this topic.
Use plain English, bullet points if needed, and be as helpful as possible.

Contract Text:
\"\"\"
{full_text[:12000]}
\"\"\"
"""

                from openai import OpenAI

                client = OpenAI(api_key=st.secrets["openai"]["openai_api_key"])

                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "You summarize and extract information from contracts for project managers."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.4
                )

summary = response.choices[0].message.content


                summary = response.choices[0].message.content
                st.markdown("### 🤖 AI Summary")
                st.write(summary)

with tabs[4]:
    st.subheader("More Coming Soon")
