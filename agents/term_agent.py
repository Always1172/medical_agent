import json

def explain_term(term):
    with open("data/medical_terms.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get(term, "未找到相关术语解释")