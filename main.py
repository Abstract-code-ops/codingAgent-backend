from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from litellm import completion
import dotenv
import os
import json

dotenv.load_dotenv()

CEREBRAS_API_KEY=os.getenv("CEREBRAS_API_KEY")

api = FastAPI()

@api.get("/health")
def health():
    return {"status": "A-okay!!"}

@api.get("/chat")
def chat(prompt: str):
    response = completion(
        model="cerebras/llama3.1-8b",
        api_key=CEREBRAS_API_KEY,
        messages=[
            {
                "role": "user",
                "content": f"{prompt}",
            }
        ],
            
        # The prompt should include JSON if 'json_object' is selected; otherwise, you will get error code 400.  
        seed=123,
        stop=["\n\n"],
        temperature=0.2,
        top_p=0.9,
        user="user",
        stream=True
    )

    def stream_content():
        for i, chunk in enumerate(response):
            # Extract the text content from the chunk
            content = chunk.choices[0].delta.content
            content = f"chunk {i}: {content}\n"
            if content:
                yield content
    return StreamingResponse(stream_content(), media_type="text/plain")
