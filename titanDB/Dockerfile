# Use a lightweight base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy database files
COPY . .

# Set environment variable for SQLite database path
RUN pip install --no-cache-dir -r requirements.txt

# Command to keep the container running
CMD ["python", "db.py"]