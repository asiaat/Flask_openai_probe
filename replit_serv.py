
import os
from time import sleep
from packaging import version
from flask import request, jsonify
import openai
from openai import OpenAI
from flask import Flask
from dotenv import load_dotenv

load_dotenv()

# Check OpenAI version is correct
required_version = "1.1.1"
current_version = version.parse(openai.__version__)
required_version = version.parse(required_version)
if current_version < required_version:
    raise ValueError(f"Error: OpenAI version {openai.__version__} is less than the required version 1.1.1")
else:
    print("OpenAI version is compatible.")

# Start Flask app
app = Flask(__name__)

# Init client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) # should use env variable OPENAI_API_KEY in secrets (bottom left corner)

# Create new functions or load existing
#assistant_id = assistants.create_assistant(client)
assistant_id = "asst_X7MjyFnENr0EZkoOCUCeviEo"


# Start conversation thread
@app.route('/start', methods=['GET'])
def start_conversation():
    print('Starting a new conversation...')  # Debugging line
    thread = client.beta.threads.create()
    print(f"New thread created with ID: {thread.id}")  # Debugging line
    return jsonify({"thread_id": thread.id})


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    thread_id = data.get('thread_id')
    user_input = data.get('message', '')

    if not thread_id:
        print("Error: Missing thread_id")  # Debugging line
        return jsonify({"error": "Missing thread_id"}), 400

    print(f"Received message: {user_input} for thread ID: {thread_id}")  # Debugging line

    # Add the user's message to the thread
    client.beta.threads.messages.create(thread_id=thread_id, role='user', content=user_input)

    # Run the Assistant
    run = client.beta.threads.runs.create(thread_id=thread_id, assistant_id=assistant_id)

    # Check if the Run requires action (function call)
    while True:
        run_status = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
        print(f"Run status: {run_status.status}")
        if run_status.status == 'completed':
            break
        sleep(1)  # Wait for a second before checking again

    # Retrieve and return the latest message from the assistant
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    print(f"Messages object: {messages}")  # Debugging line to inspect messages object

    # Assuming messages is iterable and we need to get the latest assistant message
    latest_message = next((msg for msg in messages if msg.role == 'assistant'), None)
    if latest_message is None:
        return jsonify({"error": "No assistant message found"}), 500

    # Extract the text from the content
    response_content = next((block.text.value for block in latest_message.content if block.type == 'text'), None)
    if response_content is None:
        return jsonify({"error": "No text content found in the latest message"}), 500

    print(f"Assistant response: {response_content}")  # Debugging line
    return jsonify({'response': response_content})

# Run server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
