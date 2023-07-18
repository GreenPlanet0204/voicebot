import requests

key = 'f1d9d07f-d82b-4673-b9da-935b2a018b73'
secret = '5e1eXChHtECzaYp3XJkUWQ=='

url = "https://calling.api.sinch.com/calling/v1/callouts"

payload = {
  "method": "ttsCallout",
  "ttsCallout": {
    "cli": "+447520651897",
    "destination": {
      "type": "number",
      "endpoint": "+12029222738"
    },
    "locale": "en-US",
    "text": "Hello, this is a call from Sinch."
  }
}

headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers, auth=(key,secret))

data = response.json()
print(data)