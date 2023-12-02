# Docker tutorial

## Introduction

This tutorial covers how to create and debug a simple Python-based Docker container that runs a service to extract sort-codes and account numbers from free-text.

## Install the required Python libraries

```bash
pip install -r requirements.txt
```

## Develop the Python script

The requirements of the Python script are to:

* Listen to an HTTP POST request
* Extract sort-code and account number pairs
* Return a list of extracted sort-codes and account numbers via the HTTP response

To purpose of the tutorial is to demonstrate how to use Docker, so the Python code will necessarily be lightweight. It can be extended by handling different variants of sort-codes and account numbers and handling a different ordering.

### Function to extract entities from free-text

The website http://regexr.com was used to develop the regular expression:

![](./regexr.png)

The regular expression was then transferred to `regex_extract.py` to extract the required entities from free-text.

Run the tests by running 

```bash
pytest
```

from the command line. All of the tests should pass.

### Hello World HTTP server

The script `hello_world_server.py` runs a simple Hello, World! style HTTP server. Run the script using

```bash
python3 hello_world_server.py
```

and then in another terminal run:

```bash
curl http://localhost:5000
```

### HTTP server for extraction

The code in `regex_extract.py` can be imported into applications to perform entity extraction. The next stage is to wrap the extractor into an HTTP server so that web requests can be made. This has been implemented in `extraction_server.py`.

To test the server, run the script and then on the command line enter:

```bash
curl http://localhost:5000 -X POST -d "This doesn't contain an account."

curl http://localhost:5000 -X POST -d "Accounts: 01-02-03 12345678 and 89-90-91 09876543."
```

## Dockerise the application

### Start Docker

Start Docker (on a Mac):

```bash
open -a Docker
```

Check the containers that are running:

```bash
docker container ls
```

### Simple base Python image

Python Docker images can be found here: https://hub.docker.com/_/python

```bash
docker build -f Dockerfile_01 .
```

Show a list of Docker images:

```bash
docker image ls
```

Run the container:

```bash
docker run <MD5 hash>  # e.g. docker run 22a6 (don't need all of it)
```

The container will print `Hello, World!` before exiting.

### Name the base Python image

Using the hash isn't particularly friendly, so it'll be named:

```bash
docker build -f Dockerfile_01 -t simple-python .
```

Show a list of Docker images:

```bash
docker image ls
```

and there should be an image called `simple-python`. Run the image:

```bash
docker run simple-python
```

The container will print `Hello, World!` before exiting.

### Install Python dependencies into the image

```bash
docker build -f Dockerfile_02 -t simple-python .
```

Note that the Docker image name is being reused.

Build the image:

```bash
docker build -f Dockerfile_02 -t simple-python .
```

Check the Docker images and then run the updated image `simple-python`:

```bash
docker image ls
docker run simple-python
```

The container will print `Python packages installed` before exiting.

