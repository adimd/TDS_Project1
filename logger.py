import os
import glob
from datetime import datetime

def write_recent_logs_first_lines(parameters):
    """
    Writes the specified number of lines from the most recent `.log` files to the destination file.

    Args:
        parameters (dict): A dictionary containing:
            - 'source location': Directory containing `.log` files.
            - 'destination location': Path to the output file.
            - 'Number of Files': Number of most recent files to process.
            - 'Lines per File': Number of lines to log from each file.
    """
    log_dir = parameters.get('source location')
    output_file = parameters.get('destination location')
    num_files = int(parameters.get('Number of Files'))
    lines_per_file = int(parameters.get('Number of Lines'))  # Default to 1 line if not specified

    # Get all .log files in the directory
    log_files = glob.glob(os.path.join(log_dir, "*.log"))

    # Sort files by last modification time (most recent first)
    log_files.sort(key=os.path.getmtime, reverse=True)

    # Open the output file for writing
    with open(output_file, "w") as outfile:
        # Process the `num_files` most recent files
        for log_file in log_files[:num_files]:
            # Get the filename (without the full path)
            filename = os.path.basename(log_file)
            # Get the last modification time of the file
            mod_time = os.path.getmtime(log_file)
            mod_time_str = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
            # Write the filename and modification time to the output file
            outfile.write(f"{filename} (Last Modified: {mod_time_str}):\n")
            # Read the specified number of lines from the file
            with open(log_file, "r") as infile:
                for _ in range(lines_per_file):
                    line = infile.readline()
                    if not line:  # Stop if the file has fewer lines than requested
                        break
                    outfile.write(f"  {line.strip()}\n")
            outfile.write("\n")  # Add a blank line between files for readability

    print(f"Results written to {output_file}")


