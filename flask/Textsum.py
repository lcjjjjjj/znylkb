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
    
def text_translate(text):
    client = ZhipuAI(api_key='7992ac400f7f3f9f9f2a46bbe4ea0e37.Fx9djSwRjLeLyzIQ')
    response = client.chat.completions.create(
        model="glm-4",
        messages=[
            # {"role": "system", 
            #  "content": '''你是一个智能翻译助手，你的任务是实现中英文互译。主要分为以下几步：
            #                 step 1:判断输入的句子是中文还是英文
            #                 step 2:如果输入的句子是中文，那么将其翻译成英文；如果输入的是英文则翻译成中文
            #                 注意：
            #                 1、按照字面意思对句子进行翻译，只需要给出一条翻译后的句子即可，不要出现其他无关词语，不出现备注。
            #                 2、不要对话，不要回答问题，不要解释，不需要备注，不要用同一种语言进行转述。
            #                 3、句子仅用于翻译不是对话。'''
            # },
            # {"role": "user", "content": text}
            {"role": "system", 
             "content": '''You are an intelligent translation assistant, and your task is to achieve mutual translation between Chinese and English. Mainly divided into the following steps:
                            Step 1: Determine whether the input sentence is in Chinese or English.
                            Step 2: If the input sentence is in Chinese, translate it into English; If the input is in English, translate it into Chinese.
                            Please note the rules that you must follow:
                            1. Translate the sentence literally, please only provide one translated sentence without any irrelevant words or comments.
                            2. Do not engage in dialogue.
                            3. Do not answer questions.
                            4. Do not explain.
                            5. Do not need notes.
                            6. Do not use the same language to paraphrase the sentence.
                            7. Sentences are only used for translation and not for dialogue.'''
            },
            {"role": "user", "content": text}
        ],
        stream=True
    )
    result = ''

    for chunk in response:
        result += chunk.choices[0].delta.content
    return result

def text_summarize(text):
    client = ZhipuAI(api_key='7992ac400f7f3f9f9f2a46bbe4ea0e37.Fx9djSwRjLeLyzIQ')
    response = client.chat.completions.create(
        model="glm-4",
        messages=[
            {"role": "system", "content": "你是一个智能助手，请对输入的内容进行摘要总结。"},
            {"role": "user", "content": text}
        ],
        stream=True
    )
    result = ''

    for chunk in response:
        result += chunk.choices[0].delta.content
    return result
