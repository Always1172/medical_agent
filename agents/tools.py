from langchain.tools import BaseTool
from agents.report_agent import analyze_report
from agents.symptom_agent import answer_symptom
from agents.term_agent import explain_term
from agents.summary_agent import generate_summary

class AnalyzeReportTool(BaseTool):
    name: str = "analyze_report"
    description: str = "用于分析医学报告，解释报告内容并指出异常指标。输入为医学报告文本。"

    def _run(self, report_text: str) -> str:
        return analyze_report(report_text)

    async def _arun(self, report_text: str) -> str:
        raise NotImplementedError("此工具不支持异步运行。")

class AnswerSymptomTool(BaseTool):
    name: str = "answer_symptom"
    description: str = "用于回答关于症状的问题，包括可能的原因和是否需要就医。输入为症状描述。"

    def _run(self, symptom: str) -> str:
        return answer_symptom(symptom)

    async def _arun(self, symptom: str) -> str:
        raise NotImplementedError("此工具不支持异步运行。")

class ExplainTermTool(BaseTool):
    name: str = "explain_term"
    description: str = "用于解释医学术语。输入为医学术语。"

    def _run(self, term: str) -> str:
        return explain_term(term)

    async def _arun(self, term: str) -> str:
        raise NotImplementedError("此工具不支持异步运行。")

class GenerateSummaryTool(BaseTool):
    name: str = "generate_summary"
    description: str = "用于根据医学检查报告和症状描述生成健康摘要报告。输入为医学检查报告文本和症状描述，用逗号分隔。"

    def _run(self, input_str: str) -> str:
        report_text, symptom = input_str.split(",", 1)
        return generate_summary(report_text, symptom)

    async def _arun(self, input_str: str) -> str:
        raise NotImplementedError("此工具不支持异步运行。")