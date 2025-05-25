FROM node:22

WORKDIR /home/ubuntu/backendserver/app

COPY package*.json ./
RUN npm install

COPY . .

EXPOSE 3000

CMD ["node", "app.js"]