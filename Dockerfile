# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p /app/static
RUN chmod 777 /app/static
RUN chmod 777 static

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

# Expose port 8000 to the outside world
EXPOSE 10000

# Run the application with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:10000", "app:app"]