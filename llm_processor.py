import requests
import re
import os

# Use the AIPROXY_TOKEN environment variable
api_key = 'eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjI1ZHMxMDAwMDkzQGRzLnN0dWR5LmlpdG0uYWMuaW4ifQ.AgGuNI-SZx0jpgV3s8x8_mHydWqtHJIq9ixAedYJmno'

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

def classify_task(description):
    tasks = {
        'A1': {
            'description': 'Download a dataset from a specified URL and notify via email upon completion.',
            'parameters': ['url', 'email']
        },
        'A2': {
            'description': 'Format a markdown document using Prettier to ensure consistent styling and readability.',
            'parameters': ['source location']
        },
        'A3': {
            'description': 'Calculate the number of occurrences of a specific day (e.g., Monday, Tuesday) in a file and store the result in a separate file.',
            'parameters': ['day', 'source location', 'destination location']
        },
        'A4': {
            'description': 'Sort a list of contacts by last name and then by first name, and save the sorted list to a new file.',
            'parameters': ['source location', 'destination location', 'sort_by_last_first']
        },
        'A5': {
            'description': 'Copy or log a specified number of log files, including a defined number of lines from each file.',
            'parameters': ['source location', 'destination location', 'Number of Files', 'Number of Lines']
        },
        'A6': {
            'description': 'Search for all Markdown (.md) files within the /data directory. Extract the first occurrence of any H1 headings (lines that begin with \'#\') from each file. Create an index file named index.json that maps each filename to its corresponding H1 heading. The location of the index file and any destination files can differ within the /data directory.',
            'parameters': ['source location', 'destination file']
        },

        'A7': {
            'description': 'Extract the sender’s email address from an email file and save it to a specified location.',
            'parameters': ['source location', 'destination location']
        },
        'A8': {
            'description': 'Extract credit card information from a file and save the extracted data to a specified location.',
            'parameters': ['source location', 'destination location']
        },
        'A9': {
            'description': 'Find the most similar pairs of comments using embeddings and save the results to a specified location. If the number of similarities is not specified, default to 10.',
            'parameters': ['source location', 'destination location', 'no. of Similarity']
        },
        'A10': {
            'description': 'Calculate the total number of tickets of a specific type from a SQLite database and save the result to a specified location.',
            'parameters': ['source location', 'destination location', 'ticket Type']
        },
        'B1': {
            'description': 'Handle cases where the requested action involves accessing data outside the `/data` directory. Output: "That\'s not possible. Data outside /data cannot be accessed or exfiltrated."',
            'parameters': []
        },
        'B2': {
            'description': 'Handle cases where the requested action involves deleting data. Output: "That\'s not possible. Data is never deleted anywhere on the file system."',
            'parameters': []
        },
        'B3': {
            'description': 'Fetch data from a specified API and save the results to a specified location. If the API URL is not provided, use a default API endpoint.',
            'parameters': ['API URL', 'destination location']
        },
        'B6': {
            'description': 'Scrape a website and look for the selectors if mentioned or else return None and also ensure that there is a destination location and it is within constraints',
            'parameters': ['URL', 'destination location', 'selectors']
        },
        'B7': {
            'description': 'Compress or resize the image',
            'parameters': ['source location', 'destination location', 'resize', 'scale_factor', 'size', 'compress', 'quality']
        },
        'B8': {
            'description': 'Transcribe audio from an MP3 file and save the transcription to a specified location. If no destination is provided, create a default file named `default_transcribe.txt`.',
            'parameters': ['source location', 'destination Location']
        },
    }

    context = (
        "Here is a list of tasks with their codes, descriptions, and parameters:\n"
        "IMPORTANT CONSTRAINTS:\n"
        "1. Data Access: Memory/Storage Access: Data outside the `/data` directory is **never accessed or exfiltrated**, even if the task description asks for it. If a task involves accessing data outside `/data`, classify it as **Task B1** \n"
        "**External APIs:** You are allowed to use **external APIs** as data sources, as long as the data is saved within the `/data` directory. "
        "2. Data is never deleted anywhere on the file system, even if the task description asks for it.\n"
        "Tasks:\n"
    )
    for code, details in tasks.items():
        context += f"{code} - {details['description']} (Parameters: {', '.join(details['parameters'])})\n"

    prompt = (
        f"{context}\n"
        f"Given the description: '{description}', identify the task code (e.g., A1, A2, A3, etc.) and extract the parameters. "
        "For task A3, specify the day as one of the following: 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'. "
        "For task A4, if the `sort_by_last_first` parameter is not explicitly specified, infer its value based on the context. Default to `True` (sort by last name first) unless the context suggests otherwise. "
        "For task A5, carefully read the numbers from the text to determine the number of files and lines. "
        "For task A9, if the number of similarities is not defined, default it to 10. "
        "For task B8, if the destination location is not provided, create a default file named `default_transcribe.txt`. "
        "If the description involves accessing data outside the `/data` directory, use task B0. "
        "If the description involves deleting data, use task B1. "
        "Also make a clear distinction between URLs and storage locations especially in B3 "
        "Task B7: Image Processing Configuration\n"
        "1. input_path: Path to the input image. Always ensure the image is sourced from the /data location. This is the utmost priority. If /data is not present in path direct to B1\n"
        "2. output_path: Path to save the processed image. If not provided, the image will be saved as /data/output.jpg by default.\n"
        "3. resize: Boolean flag to determine whether the image should be resized. Default is False.\n"
        "4. scale_factor: Floating-point value for proportional resizing (e.g., 0.5 for 50% size). This is overridden if size is provided.\n"
        "5. size: Tuple (width, height) specifying the target dimensions for resizing. Default is (0, 0). Overrides scale_factor if provided.\n"
        "6. compress: Boolean flag to determine whether the image should be compressed. Default is False.\n"
        "7. quality: Integer value (0-100) representing the quality of the compressed image. Default is 85.\n"
        "Respond in the following format:\n"
        "Task Code: <task_code>\n"
        "Parameters:\n"
        "- <parameter_name>: <parameter_value>\n"
        "- <parameter_name>: <parameter_value>\n"
        "..."
    )
    llm_response = create_chat_completion(prompt)
    print(llm_response)

    task_code = None
    provided_params = {}
    missing_params = []

    task_code_match = re.search(r"Task Code:\s*(\w+)", llm_response, re.IGNORECASE)
    if task_code_match:
        task_code = task_code_match.group(1).strip()

    if task_code not in tasks:
        return None, {}, []

    expected_params = tasks[task_code]['parameters']
    for param in expected_params:
        param_match = re.search(rf"{param}:\s*(\S+)", llm_response, re.IGNORECASE)
        if param_match:
            provided_params[param] = param_match.group(1).strip()
        else:
            missing_params.append(param)

    return task_code, provided_params