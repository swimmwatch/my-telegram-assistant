FROM node:18.14.1 as builder

WORKDIR /app

COPY web/vue-app/package.json .
COPY web/vue-app/package-lock.json .

RUN npm install --only=prod

COPY web/vue-app .

RUN npm run build

FROM caddy:2.6.4

COPY web/Caddyfile /etc/caddy/

COPY --from=builder /app/dist /usr/share/caddy/html
