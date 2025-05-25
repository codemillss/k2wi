const express = require('express');
const KimchiController = require('../controller/KimchiController');

class routes {
    constructor() {
        this.router = express.Router();
        this.kimchiController = new KimchiController();
        this.initializeRoutes();
    }

    initializeRoutes() {
        this.router.get('/kimchiRecipe/:name', this.kimchiController.getKimchiRecipe);
        this.router.post('/MadeKimchi', this.kimchiController.madeKimchiRecipe);
        this.router.get('/kimchiData', this.kimchiController.getKimchiData);
        // this.router.get('/exampleimage', this.kimchiController.getExmapleImage);
        this.router.get('/forAI', this.kimchiController.MadeKimchiALLImage_From_AI_Made);
        this.router.get('/ExampleSort', this.kimchiController.ExampleSort);
        this.router.get('/UserMadeImage', this.kimchiController.MadeKimchi_Image_From_User);
    }

}

module.exports = routes;