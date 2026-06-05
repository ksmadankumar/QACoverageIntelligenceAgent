import ollama

MODEL_NAME = "qwen3:14b"


def call_qwen(
    prompt
):

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0,
            "num_predict": 120,
            "top_p": 0.8
        }
    )

    return response[
        "message"
    ][
        "content"
    ]