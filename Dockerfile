# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install dependencies (LibreOffice and Python libraries)
RUN apt-get update && apt-get install -y \
    libreoffice \
    libreoffice-writer \
    libreoffice-calc \
    libreoffice-impress \
    && rm -rf /var/lib/apt/lists/*

# Install pip packages
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application
COPY . /app
WORKDIR /app

# Expose the port Flask will run on
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "backend/pdfmaker.py"]