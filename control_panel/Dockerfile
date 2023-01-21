#######################
### Build React app ###
#######################
FROM node:16 as builder

WORKDIR /app/react-app

COPY react-app/package.json .
COPY react-app/package-lock.json .

RUN npm install --only=prod

WORKDIR /app

COPY . .

WORKDIR /app/react-app

RUN npm run build

##########################
### Start Ngnix server ###
##########################
FROM nginx:stable-alpine

# Copy static files
COPY --from=builder /app/react-app/build /usr/share/nginx/html

# Replace default config
RUN rm /etc/nginx/conf.d/default.conf
COPY --from=builder /app/nginx.conf /etc/nginx/conf.d

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
