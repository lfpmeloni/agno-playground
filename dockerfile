# Stage 1: Build the Agent UI (if needed) – adjust if you already have production files.
FROM node:16 AS agent-ui-build
WORKDIR /app/agno-server/agent-ui
COPY agno-server/agent-ui/package*.json ./
# Install pnpm and dependencies
RUN npm install -g pnpm && pnpm install
# Optionally, build the production bundle (if your agent-ui supports it)
# RUN pnpm build

# Stage 2: Final image
FROM python:3.9-slim

# Install system dependencies, Supervisor, and Nginx
RUN apt-get update && apt-get install -y \
    supervisor nginx curl && rm -rf /var/lib/apt/lists/*

# Copy all files into /app (adjust if necessary)
WORKDIR /app
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Node dependencies for Agent UI (if needed)
WORKDIR /app/agno-server/agent-ui
RUN npm install -g pnpm && pnpm install

# Set working directory back to /app
WORKDIR /app

# Copy supervisor and nginx config files (we will create these next)
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80 for the container (Azure expects this)
EXPOSE 80

# Start Supervisor (which in turn starts Nginx and all your services)
CMD ["/usr/bin/supervisord", "-n"]
