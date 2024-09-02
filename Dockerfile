# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install pipenv to manage dependencies
RUN pip install --upgrade pip

# Copy requirements.txt
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

RUN python manage.py makemigrations
RUN python manage.py migrate

# Expose the port that Django will run on
EXPOSE 8000

# Run the Django development server (for production use gunicorn or another WSGI server)
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
