from flask import Flask, jsonify, request
import requests
import json

app = Flask(__name__)

# Function to send a message to Slack
def call_external_api(message):
    SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

    print(f"Sending message to Slack: {message}")

    blocks_data = [
       {
        "type": "rich_text",
        "elements": [{
            "type": "rich_text_preformatted",
            "elements": [{
                "type": "text",
                "text": json.dumps(message, indent=4)
                },],
            "border": 0
        }]
      }]
    
    response = requests.post(
        SLACK_WEBHOOK_URL, 
        json={'blocks': blocks_data},
        verify=False  # Bypass SSL verification (not recommended)
    )

    # Print the response for debugging
    if response.status_code == 200:
        print("Message sent to Slack successfully!")
    else:
        print(f"Failed to send message: {response.status_code}, Response: {response.text}")

    return response

@app.route('/send-message', methods=['POST'])
def send_message():
    data = request.get_json()
    message = data.get('message')

    if not message:
        return jsonify({"error": "Message is required"}), 400

    response = call_external_api(message)

    if response.status_code == 200:
        return jsonify({"status": "Message sent successfully!"}), 200
    else:
        return jsonify({"error": "Failed to send message", "details": response.text}), response.status_code

if __name__ == '__main__':
    app.run(port=5000)