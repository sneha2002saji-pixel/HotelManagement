# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./requirements.txt .
COPY ./src /app/src

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 for the FastAPI application
EXPOSE 8000

# Run the uvicorn server when the container launches
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
