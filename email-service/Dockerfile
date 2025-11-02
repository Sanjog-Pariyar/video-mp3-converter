FROM node:24-alpine3.21 AS base

WORKDIR /app

COPY package*.json ./

RUN --mount=type=cache,target=/app/.npm \
  npm set cache /app/.npm && \
  npm install

COPY . .

CMD ["npm", "run", "dev"]