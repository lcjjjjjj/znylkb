from zhipuai import ZhipuAI

def text_rewrite(text):
    client = ZhipuAI(api_key='7992ac400f7f3f9f9f2a46bbe4ea0e37.Fx9djSwRjLeLyzIQ')
    response = client.chat.completions.create(
        model="glm-4",
        messages=[
            {"role": "system", "content": "你是一个智能助手，请将在口语化的中文文本转换为书面中文文本，仅给出改写后的句子即可。"},
            {"role": "user", "content": text}
        ],
        stream=True
    )
    result = ''

    for chunk in response:
        result += chunk.choices[0].delta.content
    return result
    

