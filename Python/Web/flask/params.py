from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/add")
def add():
    x = request.args.get("x", default=0, type=int)
    y = request.args.get("y", default=0, type=int)
    return f"{x} + {y} = {x+y}"


if __name__ == "__main__":
    app.run(host="0.0.0.0")
