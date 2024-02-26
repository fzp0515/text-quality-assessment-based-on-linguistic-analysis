import openai
import json
OPENAI_API="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"
# 设置API密钥
openai.api_key = OPENAI_API

def ask_openai(question):
    # 调用OpenAI的聊天模型
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # 使用特定的模型
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question}
        ]
    )

    return response.choices[0].message['content']

# 测试函数
prompt=("""Please evaluate the following response from the LLM regarding a discipline-specific question based  on the following criteria. You must score it on a scale of 0, 1, 2 or 3 stars:

Overall Rating:
0 stars indicate wrong answer with a wrong explanation
1 star indicates wrong answer but a partially reasonable explanation
2 stars indicate a correct answer with a partially reasonable explanation
3 stars indicate a correct answer with a reasonable explanation

User: {question}

LLM:{answer_from_llm}

The correct answer to user’s question is: {correct_answer}

You must provide your feedback in the following format:
{"Overall Rating":numbers of its stars(int)}
        """)

with open("test.json", 'r',encoding="utf-8") as file:

    data = json.load(file)
    for item in data:
        question = item['question']
        answer = item['answer']
        question_for_alignment = {
            "question": question,
            "answer": answer,
            "generated_steps": ["", ""],
            "generated_answer": "",
            "difficulty": "",
            "math_topic": ""
        }
        json_str = json.dumps(question_for_alignment, indent=4)
        response = ask_openai(prompt + "input:" + json_str + "output:")
        print(response)
        # item['cleaned_question']=response['question']
        # item['generated_steps'] = response['generated_steps']
        # item['generated_answer'] = response['generated_answer']
        # item['difficulty'] = response['difficulty']
        # item['math_topic'] = response['math_topic']
