import sys
import streamlit as st
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.report_agent import analyze_report
from agents.symptom_agent import answer_symptom
from agents.term_agent import explain_term
from agents.summary_agent import generate_summary
from utils.ocr_parser import parse_uploaded_file

st.set_page_config(page_title="智能医学助手", layout="wide")
st.title("🩺 智能医学报告解读与健康问答助手")

uploaded_file = st.file_uploader("上传体检报告（支持PDF/JPG/PNG）")
user_symptom = st.text_input("请输入您的症状（如头痛、乏力等）")
query_term = st.text_input("输入医学术语（如CRP、血红蛋白）获取解释")

if uploaded_file:
    with st.spinner("正在解析报告..."):
        report_text = parse_uploaded_file(uploaded_file)
        st.subheader("📄 报告内容")
        st.text(report_text)

        explanation = analyze_report(report_text)
        st.subheader("🧠 报告解读")
        st.write(explanation)

if user_symptom:
    response = answer_symptom(user_symptom)
    st.subheader("💬 健康问答")
    st.write(response)

if query_term:
    term_info = explain_term(query_term)
    st.subheader("📘 医学术语解释")
    st.write(term_info)

if uploaded_file and st.button("📝 生成健康摘要报告"):
    summary = generate_summary(report_text, user_symptom)
    st.subheader("📄 健康摘要")
    st.write(summary)