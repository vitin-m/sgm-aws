FROM node:20-alpine AS build

WORKDIR /src

ADD package.json package-lock.json ./

RUN ["npm", "ci"]

ADD ./ ./

RUN ["npm", "run", "build"]

FROM nginx:stable-alpine

COPY --from=build /src/dist /usr/share/nginx/html
ADD ./nginx.frontend.conf /etc/nginx/conf.d 

EXPOSE 80

ENTRYPOINT ["nginx", "-g", "daemon off;"]