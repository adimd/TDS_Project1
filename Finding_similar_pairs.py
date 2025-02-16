import os
import requests
import json
from scipy.spatial.distance import cosine
import heapq
from concurrent.futures import ThreadPoolExecutor, as_completed

# Access the API key from the environment variable
api_key = os.getenv("API_KEY")

if not api_key:
    raise ValueError("Please set the API_KEY environment variable.")

def get_embedding_batch(texts, model="text-embedding-ada-002"):
    """
    Get embeddings for a batch of texts using a custom OpenAI proxy endpoint.
    """
    proxy_url = "http://aiproxy.sanand.workers.dev/openai/v1/embeddings"
    payload = {
        "input": texts,
        "model": "text-embedding-3-small"
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    response = requests.post(proxy_url, headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        raise Exception(f"Failed to get embedding: {response.status_code}, {response.text}")
    response_data = response.json()
    return [item['embedding'] for item in response_data['data']]

def find_most_similar_comments(parameters) -> None:
    """
    Finds the top N most similar pairs of comments from a file and writes them to another file.
    """
    input_file = parameters.get('source location')
    output_file = parameters.get('destination location')
    top_n = int(parameters.get('no. of Similarity', 10))

    if not input_file or not output_file:
        raise ValueError("Both 'source_location' and 'output_location' must be provided in the parameters.")

    with open(input_file, 'r') as file:
        comments = [comment.strip() for comment in file.readlines()]

    # Batch embeddings
    batch_size = 100  # Adjust based on API limits
    embeddings = []
    with ThreadPoolExecutor() as executor:
        futures = []
        for i in range(0, len(comments), batch_size):
            batch = comments[i:i + batch_size]
            futures.append(executor.submit(get_embedding_batch, batch))
        for future in as_completed(futures):
            embeddings.extend(future.result())

    # Use a min-heap to store the top N most similar pairs
    heap = []

    # Compare each pair of comments
    with ThreadPoolExecutor() as executor:
        futures = []
        for i in range(len(embeddings)):
            for j in range(i + 1, len(embeddings)):
                futures.append(executor.submit(cosine, embeddings[i], embeddings[j]))
        for future in as_completed(futures):
            similarity = 1 - future.result()
            if len(heap) < top_n:
                heapq.heappush(heap, (similarity, comments[i], comments[j]))
            else:
                if similarity > heap[0][0]:
                    heapq.heappop(heap)
                    heapq.heappush(heap, (similarity, comments[i], comments[j]))

    # Sort the heap to get the pairs in descending order of similarity
    most_similar_pairs = sorted(heap, reverse=True, key=lambda x: x[0])

    # Write the top N most similar pairs to the output file
    with open(output_file, 'w') as file:
        for similarity, comment1, comment2 in most_similar_pairs:
            file.write(f"Similarity: {similarity:.4f}\n")
            file.write(f"Comment 1: {comment1}\n")
            file.write(f"Comment 2: {comment2}\n")
            file.write("\n")

    print(f"Top {top_n} most similar pairs of comments written to {output_file}")

# # Example execution
# parameters = {
#     'source location': '/data/comments.txt',
#     'destination location': '/data/comments-similar.txt',
#     'no. of Similarity': 3
# }

# find_most_similar_comments(parameters)