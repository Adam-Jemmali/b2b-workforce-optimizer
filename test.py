import requests

# Define the API endpoint and your API key
url = "https://openrouter.ai/api/v1/chat/completions"
api_key = "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"

# Define the headers and the payload
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}

payload = {
    "model": "deepseek/deepseek-r1:free",
    "messages": [
        {
            "role": "user",
            "content": "What is the meaning of life?"
        }
    ],
}

# Send the POST request to the API
response = requests.post(url, headers=headers, json=payload)

# Check if the response is successful
if response.status_code == 200:
    completion = response.json()
    print(completion['choices'][0]['message']['content'])
else:
    print(f"Error: {response.status_code}, {response.text}")
