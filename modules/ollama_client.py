import ollama


MODEL_NAME = "qwen3:14b"


def call_qwen(prompt):

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response[
        "message"
    ]["content"]