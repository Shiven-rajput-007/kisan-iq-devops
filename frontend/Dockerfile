# Multi-stage Dockerfile for KisanIQ React Frontend
# Stage 1: Build production bundle
FROM node:20-alpine AS builder

WORKDIR /app

# Build arguments for Vite environment
ARG VITE_API_URL=/api
ARG VITE_API_BASE_URL=/api
ENV VITE_API_URL=$VITE_API_URL
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

# Copy dependency specifications
COPY package.json package-lock.json ./

# Install npm dependencies
RUN npm ci

# Copy application source files
COPY . .

# Compile and bundle with Vite
RUN npm run build

# Stage 2: Serve static bundle via Nginx reverse proxy
FROM nginx:alpine AS runner

# Remove default static pages
RUN rm -rf /usr/share/nginx/html/*

# Copy compiled SPA bundle from builder
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose HTTP port
EXPOSE 80

# Health check to ensure Nginx is responding
HEALTHCHECK --interval=15s --timeout=5s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://127.0.0.1:80/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
