import requests
import json

def fetch_data_from_api(api_url):
    """
    Fetches data from the specified API URL.

    :param api_url: The URL of the API to fetch data from.
    :return: The JSON response from the API, or None if an error occurs.
    """
    try:
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an error for bad status codes
        return response.json()  # Parse JSON response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return None

def save_data_to_file(data, filename):
    """
    Saves the fetched data to a file.

    :param data: The data to save.
    :param filename: The name of the file to save the data to.
    :return: True if the data was saved successfully, False otherwise.
    """
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"Data successfully saved to {filename}")
        return True
    except IOError as e:
        print(f"Error saving data to file: {e}")
        return False

def fetch_and_save_data(parameters):
    api_url =  parameters.get('API URL') 
    output_filename =  parameters.get('destination file') 
    """
    Fetches data from an API and saves it to a file.

    :param api_url: The URL of the API to fetch data from.
    :param output_filename: The name of the file to save the data to.
    :return: True if the operation was successful, False otherwise.
    """
    # Fetch data from the API
    data = fetch_data_from_api(api_url)
    
    if data:
        # Save the fetched data to a file
        return save_data_to_file(data, output_filename)
    return False