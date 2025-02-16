import subprocess
import requests
import sys  # To get the Python executable path

def download_and_run_script(parameters):
    #print(parameters)
#     print(f"Email passed to script: {email}")  # Debugging: ensure email is correctly passed

    script_url = parameters.get('url')
    email  = parameters.get('email')
    # Print or use the values
    #print(f"URL: {script_url}")
    #print(f"Email: {email}")
    response = requests.get(script_url)
    print(response)
    
    if response.status_code == 200:
        script_path = 'datagen.py'  # Assuming the script is saved in the current working directory
        with open(script_path, 'w') as file:
            file.write(response.text)

        # Use the full path to the Python executable
        python_executable = sys.executable
        command = [python_executable, script_path, email]

        # Correctly execute the script with the email argument
        result = subprocess.run(command, capture_output=True, text=True)
        
        if result.returncode == 0:
            return result.stdout
        else:
            raise Exception(f"Script execution failed: {result.stderr}")
    else:
        raise Exception(f"Failed to download the script with status code {response.status_code}")