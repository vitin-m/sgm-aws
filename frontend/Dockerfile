FROM node:current

WORKDIR /src

ADD package.json /
ADD . .

RUN ["npm", "i"]

EXPOSE 3000
CMD ["npm", "run", "dev"]
