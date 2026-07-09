# Use official Python image as a base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (needed for psycopg2 and other packages if any)
# Note: Since we are using psycopg2-binary, we usually do not need gcc or libpq-dev.


# Copy requirements file first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Make the container startup script executable
RUN chmod +x /app/start.sh

# Expose the port the app runs on
EXPOSE 8011

# Command to run the application
CMD ["/app/start.sh"]
