# Use the official Python image from the Docker Hub
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Make entrypoint.sh executable
RUN chmod +x entrypoint.sh

# Set the entry point
ENTRYPOINT ["./entrypoint.sh"]
