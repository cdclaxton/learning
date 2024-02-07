FROM python:slim

# Upgrade the OS packages
RUN apt-get update && apt-get -y upgrade

# Install Tesseract OCR
RUN apt-get install -y tesseract-ocr

# Install OpenCV dependencies
RUN apt-get install -y ffmpeg libsm6 libxext6  

# Install the required Python libraries
COPY requirements.txt /opt/
RUN ["pip", "install", "-r", "/opt/requirements.txt"]

# Copy the Jupyter config
COPY ./jupyter-config/jupyter_notebook_config.py /root/.jupyter/

# Mount a volume for the Jupyter notebooks
RUN ["mkdir", "/notebooks"]

# Set the working directory
WORKDIR /notebooks

# Expose the Jupyter Notebook port
EXPOSE 8888

# Run the Jupyter notebook
CMD ["jupyter", "notebook", "--allow-root", "--no-browser"]
