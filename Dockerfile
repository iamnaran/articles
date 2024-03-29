# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

EXPOSE 10000

# Run the application with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:10000", "app:app"]

# CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:10000", "app:app"]
