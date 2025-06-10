# medical_agent/agents/comprehensive_chain.py
from langchain.schema.runnable import RunnableSequence
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser
from langchain.chat_models import ChatOpenAI
from .tools import AnalyzeReportTool, AnswerSymptomTool, ExplainTermTool, GenerateSummaryTool

class HealthAssessmentChain:
    def __init__(self):
        # 初始化工具
        self.analyze_report_tool = AnalyzeReportTool()
        self.answer_symptom_tool = AnswerSymptomTool()
        self.explain_term_tool = ExplainTermTool()
        self.generate_summary_tool = GenerateSummaryTool()
        
        # 初始化LLM
        self.llm = ChatOpenAI(model_name="gpt-4", temperature=0.1)
        
        # 创建完整的链式表达式
        self.chain = self._create_full_chain()
    
    def _create_full_chain(self):
        # 1. 报告分析链
        report_prompt = ChatPromptTemplate.from_template(
            "请分析以下医学报告并提取关键异常指标：\n{report_text}"
        )
        report_analysis = report_prompt | self.llm | StrOutputParser()
        
        # 2. 症状评估链
        symptom_prompt = ChatPromptTemplate.from_template(
            "患者报告显示：{analysis_result}\n患者自述症状：{symptoms}\n请评估这些症状的严重性和可能原因"
        )
        symptom_assessment = {
            "analysis_result": lambda x: x["analysis_result"],
            "symptoms": lambda x: x["symptoms"]
        } | symptom_prompt | self.llm | StrOutputParser()
        
        # 3. 术语解释链
        term_prompt = ChatPromptTemplate.from_template(
            "在以下分析中提到的术语：{analysis_result}\n请解释这些术语：{terms}"
        )
        term_explanation = {
            "analysis_result": lambda x: x["analysis_result"],
            "terms": lambda x: x["terms"]
        } | term_prompt | self.llm | StrOutputParser()
        
        # 4. 综合建议链
        advice_prompt = ChatPromptTemplate.from_template("""
            报告分析结果：{analysis_result}
            症状评估：{symptom_assessment}
            术语解释：{term_explanations}
            
            请基于以上信息，为患者提供综合健康建议，包括：
            1. 当前健康状况总结
            2. 需要关注的重点问题
            3. 推荐的下一步行动（如就医、生活方式调整等）
            4. 紧急情况提示
        """)
        advice = {
            "analysis_result": lambda x: x["analysis_result"],
            "symptom_assessment": lambda x: x["symptom_assessment"],
            "term_explanations": lambda x: x["term_explanations"]
        } | advice_prompt | self.llm | StrOutputParser()
        
        # 完整的链式表达式
        return {
            "analysis_result": report_analysis,
            "symptoms": lambda x: x["symptoms"],
            "terms": lambda x: x["terms"]
        } | {
            "analysis_result": lambda x: x["analysis_result"],
            "symptom_assessment": symptom_assessment,
            "terms": lambda x: x["terms"]
        } | {
            "analysis_result": lambda x: x["analysis_result"],
            "symptom_assessment": lambda x: x["symptom_assessment"],
            "term_explanations": term_explanation
        } | advice
    
    def run(self, report_text, symptoms, terms):
        return self.chain.invoke({
            "report_text": report_text,
            "symptoms": symptoms,
            "terms": terms
        })