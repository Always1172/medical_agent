from chains.rag_chain import rag_qa

def generate_summary(report_text, symptom):
    prompt = f"以下是医学检查报告内容：{report_text}\n以及用户症状描述：{symptom}\n请生成一个简明的健康摘要报告，包括主要结论和建议。"
    return rag_qa(prompt)