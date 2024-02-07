# Optical Character Recognition

## Introduction

This Dockerfile builds a Docker image that contains:

- The latest version of Python
- A range of Python libraries defined in the `requirements.txt` file, which includes
  - Scipy, Numpy, Matplotlib, Pandas
  - Jupyter notebook
  - Tesseract OCR
- Tesseract OCR binaries

## Build the Docker image

```bash
# Build the Docker image
docker image build -t nca/python-ocr:latest .

# If a Bash terminal is needed inside the container:
# docker container run -it --mount type=bind,source="$(pwd)"/notebooks,target=/notebooks nca/python-ocr:latest /bin/bash

# Build the EasyOCR Docker image
docker build -t nca/python-easyocr:latest -f Dockerfile-EasyOCR .
```

## Run the Docker image

```bash
# Run the image
docker-compose up

# Copy the token from the Docker Quickstart console (select and press Enter)

# Navigate to http://192.168.99.100:8888/
# Paste in the token

docker-compose -f docker-compose-easyocr.yml up
```

To save the Docker image

```bash
docker save nca/python-ocr -o C:/Users/cdcla/Downloads/python-ocr.docker
```
