import requests
import re
import os

# # Use the AIPROXY_TOKEN environment variable
# api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjI1ZHMxMDAwMDkzQGRzLnN0dWR5LmlpdG0uYWMuaW4ifQ.AgGuNI-SZx0jpgV3s8x8_mHydWqtHJIq9ixAedYJmno'

# Access the API key from the environment variable
api_key = os.getenv("API_KEY")

if not api_key:
    raise ValueError("Please set the AIPROXY_TOKEN environment variable.")

def create_chat_completion(prompt):
    url = "http://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    data = {
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an error for bad status codes
        response_data = response.json()
        return response_data['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        return str(e)

def extract_email_address(email_content):
    """
    Extracts the sender's email address from the given email content using an LLM.

    Args:
        email_content (str): The content of the email.

    Returns:
        str: The extracted sender's email address.
    """
    # Use the chat-based LLM to extract the sender's email address
    prompt = f"Extract the sender's email address from the following email:\n\n{email_content}\n\nSender's email address:"
    email_address = create_chat_completion(prompt)
    return email_address.strip()

def process_email_file(parameters):
    input_file_path = parameters.get('source location')
    output_file_path = parameters.get('destination location')

    # Read the email content from the input file
    with open(input_file_path, 'r') as file:
        email_content = file.read()
    
    # Extract the sender's email address
    sender_email = extract_email_address(email_content)
    
    # Write the extracted email address to the output file
    with open(output_file_path, 'w') as file:
        file.write(sender_email)