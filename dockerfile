# Stage 1: Build the Agent UI (if needed)
FROM node:16 AS agent-ui-build
WORKDIR /app/agent-ui
COPY agent-ui/package*.json ./
RUN npm install -g pnpm && pnpm install
# Optionally, build production assets:
# RUN pnpm build

# Stage 2: Final image
FROM python:3.9-slim

# Install system dependencies, Supervisor, Nginx, curl, Node.js, and npm
RUN apt-get update && apt-get install -y \
    supervisor nginx curl nodejs npm && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Node dependencies for Agent UI
WORKDIR /app/agent-ui
RUN npm install -g pnpm && pnpm install

# Set working directory back to /app
WORKDIR /app

# Copy Supervisor and Nginx configuration files
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80 (Azure Web Apps expects your container to listen on port 80)
EXPOSE 80

CMD ["/usr/bin/supervisord", "-n"]
