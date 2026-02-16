from server import db
import logging

logging.basicConfig(level=logging.INFO)

def test_connection():
    print("Starting local Neo4j connection test...")
    # This forces the 'driver' property to initialize and run get_graph_schema
    try:
        schema = db.execute_read("CALL db.labels()")
        print(f"Connection Successful! Labels found: {schema}")
    except Exception as e:
        print(f"Local Test Failed: {e}")

if __name__ == "__main__":
    test_connection()