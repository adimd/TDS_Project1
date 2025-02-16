import json
from operator import itemgetter

def sort_json(parameters):
    # Fetch parameters
    input_file = parameters.get('source location')
    output_file = parameters.get('destination location')
    sorting_key = parameters.get('sort_by_last_first', 'False')  # Default to sorting by first name

    # Determine sorting key based on the boolean flag
    if sorting_key.lower() == 'true':
        sort_key = 'last_name'
    else:
        sort_key = 'first_name'

    # Load data from the input JSON file
    with open(input_file, 'r') as file:
        data = json.load(file)

    # Sort data by the determined key
    sorted_data = sorted(data, key=itemgetter(sort_key))

    # Save sorted data to an output file
    with open(output_file, 'w') as file:
        json.dump(sorted_data, file, indent=4)