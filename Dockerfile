# Use the official Python image from DockerHub
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install LibreOffice and any other system dependencies
RUN apt-get update && apt-get install -y libreoffice

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that the Flask app will run on
EXPOSE 5000

# Command to run the Flask app
CMD ["gunicorn", "backend.pdfmaker:app"]


