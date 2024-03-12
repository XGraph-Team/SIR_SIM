import json

import requests

base_url = "http://0.0.0.0:8000"
model = "long-llama"

def create_chat_completion(model, messages, stream=False):
    data = {
        "model": model,  
        "messages": messages,  
        "stream": stream,  
        "max_tokens": 100,  
        "temperature": 0.8,  
        "top_p": 0.8, 
    }

    response = requests.post(f"{base_url}/v1/chat/completions", json=data, stream=stream)
    if response.status_code == 200:
        if stream:
            for line in response.iter_lines():
                if line:
                    decoded_line = line.decode('utf-8')[6:]
                    try:
                        response_json = json.loads(decoded_line)
                        content = response_json.get("choices", [{}])[0].get("delta", {}).get("content", "")
                        print(content)
                    except:
                        print("Special Token:", decoded_line)
        else:
            decoded_line = response.json()
            print(decoded_line)
            content = decoded_line.get("choices", [{}])[0].get("message", "").get("content", "")
            print(content)
    else:
        print("Error:", response.status_code)
        return None


if __name__ == "__main__":
    chat_messages = [
        {
            "role": "user",
            # "content": "Who are you?"
            "content": "What is the maximum tokens you can handle?"
        }
    ]
    create_chat_completion(model, chat_messages, stream=False)
