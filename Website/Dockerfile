# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory to /app
WORKDIR /app

# upgrade pip 
RUN pip install --no-cache-dir --upgrade pip

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 3000 available to the world outside this container
EXPOSE 8000

VOLUME ["/app/storage"]

# Run the command to start your application
CMD [ "python", "main.py" ]
