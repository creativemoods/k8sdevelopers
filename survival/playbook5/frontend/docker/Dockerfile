FROM node:18.17-alpine AS studentx_frontend_builder
LABEL maintainer="jerome@creativemoods.pt"

# Build with command docker build --no-cache -t registry.creativemoods.pt/studentx/studentx_frontend:latest -f frontend/Dockerfile  .
# Run with command docker run -p 3000:3000 -e PORT=3000 -e ... registry.creativemoods.pt/studentx/studentx-frontend

WORKDIR /app

COPY --chown=node ["package.json", "package-lock.json*", "./"]
# https://github.com/nodejs/docker-node/tree/b4117f9333da4138b03a546ec926ef50a31506c3#nodealpine
RUN apk add --no-cache libc6-compat && \
  npm ci --production

COPY --chown=node src ./src/
COPY --chown=node public ./public/

RUN mkdir ./.next && \
  chown node: ./.next && \
  chown -R node: .

USER node

ARG REACT_APP_API_URL
ENV REACT_APP_API_URL=$REACT_APP_API_URL
RUN npm run build

FROM node:18.17-alpine AS studentx_frontend_runner

ARG APP_ENV=production
ARG NODE_ENV=production
ARG PORT=3000

ENV APP_ENV=${APP_ENV} \
    NODE_ENV=${NODE_ENV} \
    PORT=${PORT} \
    NEXT_TELEMETRY_DISABLED=1

RUN npm install -g serve

WORKDIR /app
USER node

COPY --from=studentx_frontend_builder --chown=node /app/build ./build

EXPOSE ${PORT}
CMD ["serve", "-s", "build", "-l", "3000"]
