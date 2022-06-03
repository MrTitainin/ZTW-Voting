FROM node
WORKDIR .

RUN npm install -g http-server

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 8080
CMD ["npm", "run", "serve"]