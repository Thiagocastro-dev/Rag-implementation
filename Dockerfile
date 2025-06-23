# Build stage
FROM node:20-alpine as builder

WORKDIR /app

# Install dependencies and development tools
RUN apk add --no-cache curl wget

# Copy package files first to leverage Docker cache
COPY package*.json ./
RUN npm ci

# Copy all source files and configuration
COPY . .

# Ensure the assets directory exists
RUN mkdir -p /app/src/assets

# Build the application
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy nginx configuration
COPY nginx.conf /etc/nginx/nginx.conf

# Copy built assets from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Create assets directory in nginx
RUN mkdir -p /usr/share/nginx/html/src/assets

# Copy the logo image
COPY src/assets/logo-mpc.png /usr/share/nginx/html/src/assets/

# Expose port
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]