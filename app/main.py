import os

import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from utils import clean_text
from chains import Chain
from portfolio import Portfolio

def create_streamlit_app(llm, portfolio):
    st.title("📧 Cold Mail Generator")
    url_input = st.text_input("Enter a url: ", value="https://jobs.nike.com/job/R-41188")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            cleaned_text = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(cleaned_text)
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_emails(job, links)
                st.code(email, language='markdown')

        except Exception as e:
            st.error(f"An error occured {e}")



if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio)
