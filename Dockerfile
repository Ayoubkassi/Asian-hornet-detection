# Use an official Python runtime as a parent image
FROM python:3.9.6

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install pkg-config and libhdf5-dev
RUN apt-get update \
    && apt-get install -y pkg-config libhdf5-dev \
    && rm -rf /var/lib/apt/lists/* 

# Install any needed packages specified in requirements.txt

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["python", "app.py"]
