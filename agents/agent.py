from langchain.agents import initialize_agent, AgentType
from langchain.chat_models import ChatOpenAI
from .tools import AnalyzeReportTool, AnswerSymptomTool, ExplainTermTool, GenerateSummaryTool

# 初始化工具列表
tools = [
    AnalyzeReportTool(),
    AnswerSymptomTool(),
    ExplainTermTool(),
    GenerateSummaryTool()
]

# 初始化语言模型
llm = ChatOpenAI(model='gpt-4', temperature=0)

# 初始化代理
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

def run_agent(query):
    return agent.run(query)