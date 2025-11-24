FROM python:3.12-slim

# Workdir inside the container
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project code
COPY . .

# Avoid Python buffering (logs em tempo real)
ENV PYTHONUNBUFFERED=1

# Expose ports used by the services (TCP, XML-RPC, gRPC)
EXPOSE 5050 5051 5052

