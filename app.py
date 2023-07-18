from flask import Flask, jsonify, request
import ssl
from pyngrok import ngrok, conf, installer
import requests
import os

key = 'f1d9d07f-d82b-4673-b9da-935b2a018b73'
secret = '5e1eXChHtECzaYp3XJkUWQ=='


app = Flask(__name__)

pyngrok_config = conf.get_default()

pyngrok_config.monitor_thread = False

if not os.path.exists(pyngrok_config.ngrok_path):
    myssl = ssl.create_default_context()
    myssl.check_hostname = False
    myssl.verify_mode = ssl.CERT_NONE
    installer.install_ngrok(pyngrok_config.ngrok_path, context=myssl)

http_tunnel = ngrok.connect(5000)

callbackUrl = http_tunnel.public_url + '/incoming-call'
print(callbackUrl)

url = "https://api.sinch.com/calling/v1/configuration/callbacks/applications/" + key

payload = {
  "url": 
    {
        "primary": callbackUrl
    }
}

headers = {
    "Content-Type": "application/json"
    }

response = requests.post(url, json=payload, headers=headers, auth=(key, secret))

print("Your callback URL has been set to " + callbackUrl)

@app.route('/incoming-call', methods=['POST'])
def result():
    res = None
    req = request.get_json()
    if req['event'] == 'ice':
        print(req)
        res = jsonify({"instructions": [
                {
                    "name": "say",
                    "text": "Hi, thank you for calling your Sinch number. Congratulations! You just responded to a phone call.",
                    "locale": "en-US"
                }
            ],
            "action": {
                  "name": "hangup"
            }
            })
        return res
    return "200 OK"

if __name__ == "__main__":
    app.run()
