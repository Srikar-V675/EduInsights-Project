# Use a Python base image
FROM python:3.11-slim-buster

# Set the working directory in the container
WORKDIR /EduInsights

# Install system dependencies
RUN apt-get update && apt-get install -y \
    chromium \
    unzip \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Download and install ChromeDriver
RUN wget -O /tmp/chromedriver.zip https://storage.googleapis.com/chrome-for-testing-public/125.0.6422.78/linux64/chromedriver-linux64.zip \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && rm /tmp/chromedriver.zip \
    && chmod +x /usr/local/bin/chromedriver-linux64/chromedriver

# Install Poetry
RUN pip install poetry

RUN poetry config virtualenvs.in-project true

# Copy only the pyproject.toml and poetry.lock to leverage Docker cache
COPY pyproject.toml poetry.lock ./

# Install Python dependencies using Poetry
RUN poetry install

# Copy the rest of the application code
COPY . .

# Expose the port your FastAPI server will run on
EXPOSE 8000
