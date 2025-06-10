# medical_agent/app/main.py
import sys
import streamlit as st
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from agents.agent import run_agent
from agents.comprehensive_chain import HealthAssessmentChain
from utils.ocr_parser import parse_uploaded_file

st.set_page_config(page_title="智能医学助手", layout="wide")
st.title("🩺 智能医学报告解读与健康问答助手")

# 初始化综合评估链
health_chain = HealthAssessmentChain()

# 状态管理
if 'report_text' not in st.session_state:
    st.session_state.report_text = ""
if 'report_parsed' not in st.session_state:
    st.session_state.report_parsed = False
if 'symptom_analyzed' not in st.session_state:
    st.session_state.symptom_analyzed = False
if 'terms_explained' not in st.session_state:
    st.session_state.terms_explained = False
if 'comprehensive_analyzed' not in st.session_state:
    st.session_state.comprehensive_analyzed = False


# 1. 报告上传区域
st.subheader("📄 体检报告上传")
uploaded_file = st.file_uploader("选择体检报告文件 (PDF/JPG/PNG)", key="report_uploader")

if uploaded_file:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"已上传文件: {uploaded_file.name}")
    with col2:
        parse_report = st.button("📥 解析报告", key="parse_report")
    
    if parse_report:
        with st.spinner("正在解析报告..."):
            report_text = parse_uploaded_file(uploaded_file)
            
            # 检查报告文本是否为错误信息
            if report_text.startswith(("未上传文件", "上传的文件为空", "不支持的文件类型", "文件解析错误")):
                st.error(report_text)
            else:
                st.session_state.report_text = report_text
                st.session_state.report_parsed = True
                st.success("报告解析成功！")
                
                # 显示报告内容和分析
                st.subheader("📄 报告内容")
                st.text(report_text)
                
                explanation = run_agent(f"analyze_report({report_text})")
                st.subheader("🧠 报告解读")
                st.write(explanation)

# 2. 症状描述区域
st.subheader("💬 症状描述")
user_symptoms = st.text_area("请详细描述您的症状（如头痛、乏力等）", key="symptom_input")

if user_symptoms:
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write(f"症状描述长度: {len(user_symptoms)} 字符")
    with col2:
        analyze_symptom = st.button("🔍 分析症状", key="analyze_symptom")
    
    if analyze_symptom:
        with st.spinner("正在分析症状..."):
            response = run_agent(f"answer_symptom({user_symptoms})")
            st.session_state.symptom_analyzed = True
            st.subheader("💬 症状分析结果")
            st.write(response)

# 3. 医学术语解释区域
st.subheader("📘 医学术语解释")
medical_terms = st.text_input("输入需要解释的医学术语（多个术语用逗号分隔）", key="term_input")

if medical_terms:
    col1, col2 = st.columns([3, 1])
    with col1:
        terms_list = [term.strip() for term in medical_terms.split(",") if term.strip()]
        st.write(f"待解释术语: {', '.join(terms_list)}")
    with col2:
        explain_terms = st.button("📖 解释术语", key="explain_terms")
    
    if explain_terms:
        with st.spinner("正在解释术语..."):
            st.session_state.terms_explained = True
            terms_list = [term.strip() for term in medical_terms.split(",") if term.strip()]
            for term in terms_list:
                term_info = run_agent(f"explain_term({term})")
                st.subheader(f"📘 {term} 术语解释")
                st.write(term_info)

# 4. 综合评估区域（仅当满足条件时显示）
if st.session_state.report_parsed and (st.session_state.symptom_analyzed or st.session_state.terms_explained):
    st.subheader("📊 健康综合评估")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("基于您的报告分析和症状/术语输入，生成综合健康评估")
    with col2:
        generate_comprehensive = st.button("📋 生成评估报告", key="generate_comprehensive")
    
    if generate_comprehensive:
        with st.spinner("正在生成综合评估报告..."):
            st.session_state.comprehensive_analyzed = True
            
            # 运行综合评估链
            result = health_chain.run(
                report_text=st.session_state.report_text,
                symptoms=user_symptoms if st.session_state.symptom_analyzed else "",
                terms=medical_terms if st.session_state.terms_explained else ""
            )
            
            st.subheader("📄 健康综合评估报告")
            st.write(result)