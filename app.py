import os
from dotenv import load_dotenv
load_dotenv()  # Pulls environmental tokens from local .env metadata maps

import streamlit as st
from openai import OpenAI

# Ensure set_page_config is the absolute first Streamlit command executed
st.set_page_config(page_title="Resume Generator UI", layout="wide", page_icon="📄")

# Import engine logic and base profile mapping configurations
from resume_engine import tailor_resume_data, generate_latex_source
from resume_data import resume as BASE_RESUME

st.title("📄 Professional AI LaTeX Resume Generator")
st.markdown("Tailor your foundational resume schema to specific jobs and fetch compilation-ready LaTeX source script instantaneously.")

# Secure Key Initialization sidebar pipeline
api_key = st.sidebar.text_input(
    "OpenAI API Key", 
    type="password", 
    value=os.environ.get("OPENAI_API_KEY", "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")
)

if not api_key:
    st.warning("Please provide an OpenAI API Key in the sidebar to begin.")
    st.stop()

# Instantiate runtime client explicitly using validated token parameters
openai_client = OpenAI(api_key=api_key)

# Render Dashboard Grid Split View layout grids
left_column, right_column = st.columns([2, 3])

with left_column:
    st.subheader("1. Configuration Parameters")
    
    chosen_model = st.selectbox(
        "Select Testing LLM Engine:",
        options=["gpt-4o-mini", "gpt-4o"]
    )
    
    job_description_input = st.text_area(
        "Target Job Specification Details:",
        height=320,
        placeholder="Paste requirements, stack parameters, or raw description guidelines here..."
    )
    
    trigger_generation = st.button("Generate Clean Code copy", type="primary", use_container_width=True)

with right_column:
    st.subheader("2. Varying LaTeX Code Source Copy")
    
    if trigger_generation and job_description_input:
        with st.spinner("Refactoring resume context fields against parameters..."):
            try:
                # 1. Fetch targeted structural schema variations via API client instantiation context pass
                tailored_obj = tailor_resume_data(
                    client=openai_client,
                    job_description=job_description_input, 
                    base_resume=BASE_RESUME, 
                    model_name=chosen_model
                )
                
                # 2. Extract parsed string format document output payloads
                latex_source_code = generate_latex_source(tailored_obj)
                
                # 3. Render success framework results outputs
                st.success(f"Successfully processed tailoring utilizing {chosen_model}!")
                st.code(latex_source_code, language="latex", line_numbers=True)
                
                st.download_button(
                    label="Download Code (.tex)",
                    data=latex_source_code,
                    file_name="tailored_resume.tex",
                    mime="text/x-tex",
                    use_container_width=True
                )
                
            except Exception as e:
                st.error(f"Execution Error encountered: {str(e)}")
    else:
        st.info("Input a Target Job Specification string and click generate to generate custom LaTeX outputs.")