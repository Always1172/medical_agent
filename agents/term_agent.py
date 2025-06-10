# import json

# def explain_term(term):
#     with open("data/medical_terms.json", "r", encoding="utf-8") as f:
#         data = json.load(f)
#     return data.get(term, "未找到相关术语解释")

from chains.rag_chain import rag_qa

def explain_term(term):
    prompt = f"请详细解释以下名词：{term}"
    return rag_qa(prompt)