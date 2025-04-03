# Stage 1: Build the Agent UI (if needed)
FROM node:16 AS agent-ui-build
WORKDIR /app/agno-server/agent-ui
COPY agno-server/agent-ui/package*.json ./
RUN npm install -g pnpm && pnpm install
# Optionally, build production assets:
# RUN pnpm build

# Stage 2: Final image
FROM python:3.9-slim

# Install system dependencies, Supervisor, Nginx, AND Node.js & npm
RUN apt-get update && apt-get install -y \
    supervisor nginx curl nodejs npm && rm -rf /var/lib/apt/lists/*

# Copy all project files into /app (adjust paths if necessary)
WORKDIR /app
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Node dependencies for Agent UI
WORKDIR /app/agno-server/agent-ui
RUN npm install -g pnpm && pnpm install

# Set working directory back to /app
WORKDIR /app

# Copy Supervisor and Nginx configuration files
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80 (Azure Web Apps expect your container to listen on this port)
EXPOSE 80

# Start Supervisor (which will launch Nginx and your services)
CMD ["/usr/bin/supervisord", "-n"]
