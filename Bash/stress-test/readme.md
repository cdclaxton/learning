# Stress-test HTTP endpoint

This code tests an HTTP endpoint using the `curl` command to see if it fails to return a response (e.g. because of a proxy error). A simple Python-based HTTP server generates a 500 server failure with a given probability.

Install the required Python libraries:

```bash
pip install -r requirements.txt
```

In one terminal, run the HTTP server with a probability of a failure (500 response code) of 0.001:

```bash
python3 server.py 0.001
```

In another terminal, run the stress test using:

```bash
./test.sh
```

Each time the server comes back with a non-200 status code, a message is printed to stdout.