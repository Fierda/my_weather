# Stage 1: Build React App
FROM node:20 AS build
WORKDIR /app

# Clean install to avoid broken native dependencies
COPY package.json package-lock.json ./
RUN rm -rf node_modules package-lock.json && npm install

COPY . .

RUN npm run build

# Stage 2: Serve React App with Nginx
FROM nginx:alpine
COPY nginx.conf /etc/nginx/nginx.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]