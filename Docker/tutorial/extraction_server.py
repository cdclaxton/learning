from flask import Flask
from flask import request

from regex_extract import extract

app = Flask(__name__)


@app.route("/", methods=["POST"])
def hello():
    # Extract the text (as bytes) from the HTTP POST request
    bytes = request.get_data()

    # Convert the bytes to a string
    text = bytes.decode("utf-8")

    # Return a list of extracted entities
    return extract(text)


if __name__ == "__main__":
    app.run()
