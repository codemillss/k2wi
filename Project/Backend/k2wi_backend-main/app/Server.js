const express = require('express');
const InsertData = require("./InsertData")

class Server {
  constructor(port) {
    this.app = express();
    this.port = port;
    this.configureMiddleware();
    this.setupRoutes();
    this.insertexampleData = new InsertData();
  }

  configureMiddleware() {
    this.app.use(express.json());
    this.app.use('/findImage', express.static("/")) //저 url을 넣으면 자동으로 static 주소로 이동
  }

  setupRoutes() {
    const goodroutes = require('./routes/routes');
    const inrouter = new goodroutes();
    this.app.use('/', inrouter.router);
  }

  start() {
    this.app.listen(this.port, () => {
      console.log(`서버가 http://localhost:${this.port}에서 실행 중입니다.`);
      // this.insertexampleData.loadCSV();
      // setTimeout(() => {
      //   this.insertexampleData.insertrecipes()
      // }, 1000)
      // setTimeout(() => {
      //   this.insertexampleData.insertingredients()
      // }, 2000)
    });
  }
}

module.exports = Server;