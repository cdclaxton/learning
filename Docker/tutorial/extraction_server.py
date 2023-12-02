import logging

from flask import Flask
from flask import request

from regex_extract import extract

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
app = Flask(__name__)


@app.route("/", methods=["POST"])
def hello():
    # Extract the text (as bytes) from the HTTP POST request
    bytes = request.get_data()

    # Convert the bytes to a string
    text = bytes.decode("utf-8")

    # Create a log message
    logging.info(f"Received request: {text}")

    # Return a list of extracted entities
    entities = extract(text)
    logging.info(f"Extracted entities: {entities}")

    return entities


if __name__ == "__main__":
    app.run(host="0.0.0.0")
