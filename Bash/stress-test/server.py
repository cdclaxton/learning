import random
import sys
from flask import Flask, Response

app = Flask(__name__)

# Default probability of a failure
p_failure = 0.9

@app.route("/")
def root():
    if random.random() < p_failure:
        return Response("Failure", status=500)
    else:
        return Response("Success", status=200)

if __name__ == '__main__':
    
    if len(sys.argv) == 2:
        try:
            p_failure = float(sys.argv[1])
            print(f"Using p_failure = {p_failure}")
        except:
            print("Invalid probability of failure")
            exit(-1)

    app.run()