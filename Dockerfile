# Use the official Python 3 image as the base image
FROM python:3

# Set environment variables if proxy is required
# ENV http_proxy http://${HTTP_PROXY}
# ENV https_proxy http://${HTTPS_PROXY}

# Copy requirements.txt and install dependencies in a virtual environment
WORKDIR /app
COPY ./requirements.txt /app/requirements.txt
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy the application code into the image
COPY . /app

# Expose a port if your application listens on a specific port
# EXPOSE 80

# Set the default command to run the application
CMD ["venv/bin/python", "app.py"]