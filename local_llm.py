from ollama import chat

model = "qwen3:8b"

# For normal text generation
def generate(prompt):
    response = chat(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        think=True
    )

    return response.message.content

# For json content generation
def generate_json(prompt):
    response = chat(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        think=True,
        format="json"
    )

    return response.message.content