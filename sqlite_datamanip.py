import sqlite3

def calculate_ticket_sales(parameters):
    print(parameters.get('source location'))
    print(parameters.get('destination location'))
    print(parameters.get('ticket Type'))

    db_path = parameters.get('source location')
    output_file_path = parameters.get('destination location')
    ticket_type = parameters.get('ticket Type')
    print(db_path)

    if not db_path or not output_file_path or not ticket_type:
        raise ValueError("Missing required parameters: 'source location', 'destination location', or 'ticket type'.")

    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # SQL query to calculate the total sales for the specified ticket type
    query = """
    SELECT SUM(units * price) AS total_sales
    FROM tickets
    WHERE type = ?;
    """

    # Execute the query with the ticket type as a parameter
    cursor.execute(query, (ticket_type,))
    result = cursor.fetchone()

    # Extract the total sales from the query result
    total_sales = result[0] if result[0] is not None else 0

    # Write the total sales to the output file
    with open(output_file_path, 'w') as output_file:
        output_file.write(str(total_sales))

    # Close the database connection
    conn.close()

    return total_sales