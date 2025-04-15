FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy the rest of the application
COPY . .

# Expose the port the app runs on
EXPOSE 8006

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8006", "llm_endpoint:app"]
