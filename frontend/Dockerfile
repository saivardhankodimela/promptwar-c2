# Build stage
FROM node:20-slim AS build
WORKDIR /app

COPY package*.json ./
RUN npm install
COPY . ./

# Fix backend URLs
RUN sed -i 's|http://localhost:9191/chat|https://voter-ai-backend-us-ivagfrcnna-uc.a.run.app/chat|g' src/components/ChatInterface.jsx
RUN sed -i 's|https://voter-ai-guide-ivagfrcnna-el.a.run.app/chat|https://voter-ai-backend-us-ivagfrcnna-uc.a.run.app/chat|g' src/components/ChatInterface.jsx

RUN chmod +x node_modules/.bin/vite
RUN npm run build

# Production stage
FROM nginx:stable-alpine
COPY --from=build /app/dist /usr/share/nginx/html

# Cloud Run expects 8080 by default
RUN echo 'server { listen 8080; location / { root /usr/share/nginx/html; index index.html; try_files $uri $uri/ /index.html; } }' > /etc/nginx/conf.d/default.conf

# Port 8080 is the Cloud Run standard
EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]
