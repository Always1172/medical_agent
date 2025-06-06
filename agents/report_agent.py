from chains.rag_chain import rag_qa

def analyze_report(text):
    prompt = f"请用通俗语言解释以下医学报告内容，并指出其中的异常指标：\n{text}"
    return rag_qa(prompt)