from chains.rag_chain import rag_qa

def answer_symptom(symptom):
    prompt = f"一个患者说自己出现了如下症状：{symptom}，可能的原因有哪些？是否需要就医？"
    return rag_qa(prompt)
