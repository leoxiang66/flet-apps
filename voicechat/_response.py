import openai
openai.api_key='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'


def reply(msg:str):
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"{msg}, 請用粵語答我."}]
    )
    response = completion['choices'][0]['message']['content'].strip()
    print(response)
    return response

