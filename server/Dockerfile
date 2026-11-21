# Multi-stage Dockerfile for KisanIQ Node.js/Express Backend
# Stage 1: Build TypeScript source to JavaScript
FROM node:20-alpine AS builder

WORKDIR /app

# Copy dependency manifests
COPY package.json package-lock.json ./

# Install all dependencies including devDependencies for tsc
RUN npm ci

# Copy tsconfig and application source code
COPY tsconfig.json ./
COPY server.ts ./
COPY controllers ./controllers
COPY db ./db
COPY middleware ./middleware
COPY routes ./routes
COPY services ./services
COPY utils ./utils

# Compile TypeScript to dist/
RUN npm run build

# Stage 2: Production execution environment
FROM node:20-alpine AS runner

WORKDIR /app

ENV NODE_ENV=production
ENV PORT=8000

# Install curl and wget for healthchecks
RUN apk add --no-cache curl wget

# Copy package manifests and install production dependencies only
COPY package.json package-lock.json ./
RUN npm ci --omit=dev && npm cache clean --force

# Copy compiled JavaScript output
COPY --from=builder /app/dist ./dist

# Copy PostgreSQL schema file for automated migrations
COPY --from=builder /app/db/schema.sql ./db/schema.sql
COPY --from=builder /app/db/schema.sql ./dist/db/schema.sql

# Create directories and set ownership for unprivileged node user
RUN mkdir -p /app/db/data && chown -R node:node /app

# Run as non-root user
USER node

EXPOSE 8000

# Container healthcheck querying /api/health
HEALTHCHECK --interval=15s --timeout=5s --start-period=15s --retries=5 \
  CMD wget --no-verbose --tries=1 --spider http://127.0.0.1:8000/api/health || exit 1

CMD ["node", "dist/server.js"]
