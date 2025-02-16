import os
import json

def extract_h1_title(file_path):
    """Extract the first H1 title from a Markdown file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.startswith('# '):
                return line.strip('# \n')
    return None

def generate_index(directory):
    """Generate an index of H1 titles for all Markdown files in the directory."""
    index = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                title = extract_h1_title(file_path)
                if title:
                    # Remove the /data/docs/ prefix from the file path
                    relative_path = os.path.relpath(file_path, start=directory)
                    index[relative_path] = title
    return index

def save_index_to_json(parameters):
    """Save the index to a JSON file."""
    index = parameters.get('source location')
    output_file = parameters.get('destination file')
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Save the index to the JSON file
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(index, json_file, indent=4)
    
    print(f"Index file created at {output_file}")

# def main():
#     docs_directory = '/data/docs'
#     index_file = '/data/docs/index.json'
    
#     # Generate the index
#     index = generate_index(docs_directory)
    
#     # Save the index to a JSON file
#     save_index_to_json(index, index_file)
    
#     print(f"Index file created at {index_file}")

# if __name__ == "__main__":
#     main()