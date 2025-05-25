const kimchimodel = require('../model/KimchiModel');
const axios = require("axios");
const fs = require('fs');
const path = require('path');
const insertdata = require('../InsertData');
const dfd = require("danfojs-node");

class KimchiController {
    
    constructor() {
       this.kimchimodel = new kimchimodel();
    }

    //김치 레시피 만든후 레시피에 삽입
    madeKimchiRecipe = async (req, res) => {
        try {
            // const { recipe_name, recipeList } = req.body;

            console.error("_______________________________");

            console.log(req.body);

            const {title, steps} = req.body;
            
            console.log(title);
            console.log(steps);

            const for_AI_DATA = await this.kimchimodel.user_made_kimchi_recipe(title, steps)

            console.error("_______________________________");

            console.log(for_AI_DATA);

            console.error("_______________________________");

            // const real_AI_data = JSON.stringify(for_AI_DATA)

            const response = await axios.post('http://ec2-3-1-2-125.ap-southeast-1.compute.amazonaws.com:8000/MakeImage/', for_AI_DATA);

            console.log("이미지 저장 시작")

            const arr = response.data.results[0].images

            console.error("______________arr_______________");

            console.log(response.data.results[0])

            console.error("_______________________________");

            let i = 1

            const saveDir = `/home/ubuntu/backendserver/app/images/${response.data.results[0].kimchi_num}`

            for (const data of arr) {
                const base64data = data.image_base64
                const imageBuffer = Buffer.from(base64data, 'base64');
                
                const savePath = path.join(saveDir, `${response.data.results[0].kimchi_name}_${i}.png`);

                // ✅ 디렉토리 생성 (동기)
                if (!fs.existsSync(saveDir)) {
                    fs.mkdirSync(saveDir, { recursive: true });
                    console.log('📁 디렉토리 생성됨:', saveDir);
                }

                // ✅ 이미지 저장 (동기)
                fs.writeFileSync(savePath, imageBuffer);
                console.log('✅ 이미지 저장 완료:', savePath);

                const kimchi_num_data = response.data.results[0].kimchi_num
                const recipe_order_data = i
                // const recipe_detail_data = response.data.results[0].steps[i - 1]
                const recipe_detail_data = response.data.results[0].prompts[i - 1]


                console.log(recipe_detail_data)

                const recipe_image_name_data = response.data.results[0].kimchi_name
                const recipe_image_path_data = saveDir + "/" + data.filename

                await this.kimchimodel.InsertTotalRecipe(kimchi_num_data, recipe_order_data, recipe_detail_data)
                await this.kimchimodel.InsertImage(kimchi_num_data, recipe_order_data, recipe_image_name_data, recipe_image_path_data)

                console.log('데이터베이스 저장 완료:', recipe_order_data);

                i++

                
                console.log("______________(데이터베이스에 저장 된 목록)_______________");  

                console.log(kimchi_num_data, recipe_order_data, recipe_detail_data, recipe_image_name_data, recipe_image_path_data)
                
            }

            console.log("----------kimchi_num----------")

            console.log()

            console.log(response.data.results[0].kimchi_num)
            
            console.log()

            console.log("-----------------------")

            const result_data = await this.kimchimodel.JoinImageAndTotalRecipe(response.data.results[0].kimchi_num)

            console.log(result_data);

            console.log("ok_______________________________________________________________________________________________________");

            return res.status(200).json({ 
                success: "이미지 저장 완료",
                body: {
                    result_data
                }
            });

        } catch (err) {
            console.error(err);
            res.status(500).json({ error: 'Internal Server Error' });
        }
    }

    //모든김치찾기
    getKimchiData = async (req, res) => {
        try {
            const result = await this.kimchimodel.findKimchiData();
            res.json(result);
        } catch (err) {
            console.error(err);
            res.status(500).json({ error: 'Internal Server Error' });
        }
    }

    //김치 래시피 찾기
    getKimchiRecipe = async (req, res) => {
        try {
            console.log(req.params.name);
            const  num  = req.params.name;
            const result = await this.kimchimodel.find_kimchi_recipe_with_name(num);
            res.json(result);
        } catch (err) {
            console.error(err);
            res.status(500).json({ error: 'Internal Server Error' });
        }
    }

    getExmapleImage = async (req, res) => {
        try {
            console.log(req.params.name);
            const result = await this.kimchimodel.kimchidata();
            // res.json(result);
            console.log(result)
            res.send(`
                <h1>sendFile 이미지 보기</h1>
                <img src="${result}" alt="도라에몽 이미지" />
            `);
        } catch (err) {
            console.error(err);
            res.status(500).json({ error: 'Internal Server Error' });
        }
    }
    

    MadeKimchi_Image_From_User = async(req, res) => {
        
        console.log(req)

        return res.status(500).json({ 
                success: "서ㅓ"
        });

    }

    MadeKimchiALLImage_From_AI_Made = async (req, res) => {
        try {
        //입력받은 데이터를 조회 후 바로 AI에게 전송

            const forAI_kimchi_num = await this.kimchimodel.findKimchinum()
            console.log(forAI_kimchi_num.rows);


            console.log("_____________");

            const forAIdata = await this.kimchimodel.postImage(1);


            console.log(forAIdata);

            // const response = await axios.post('http://ec2-3-1-2-125.ap-southeast-1.compute.amazonaws.com:8000/MakeImage/', forAIdata);

            // console.log(response.data)

            // console.log(response.data.results)
            // console.log(response.data.results[0].images)


            // console.log("이미지 저장 시작")
            
            // let listForImageData_base64 = []
            // let listForImageData_kimchi_num= []
            // let listForImageData_kimchi_name = []

            
            // const arr = response.data.results[0].images

            // let i = 1

            // const saveDir = `/home/ubuntu/backendserver/app/images/${response.data.results[0].kimchi_num}`

            // for (const data of arr) {
            //     const base64data = data.image_base64
            //     const imageBuffer = Buffer.from(base64data, 'base64');

                
            //     const savePath = path.join(saveDir, `${response.data.results[0].kimchi_name}_${i}.png`);

            //     // ✅ 디렉토리 생성 (동기)
            //     if (!fs.existsSync(saveDir)) {
            //         fs.mkdirSync(saveDir, { recursive: true });
            //         console.log('📁 디렉토리 생성됨:', saveDir);
            //     }

            //     // ✅ 이미지 저장 (동기)
            //     fs.writeFileSync(savePath, imageBuffer);
            //     console.log('✅ 이미지 저장 완료:', savePath);

            //     listForImageData_base64[i] = base64data
            //     listForImageData_kimchi_num[i] = base64data
            //     listForImageData_kimchi_name[i] = base64data

            //     i++
            // } 

            // return res.status(200).json({ 
            //     success: "이미지 저장 완료",
            //     body: {
            //         imagedata : listForImageData_base64,
            //         kimchi_num : listForImageData_kimchi_num,
            //     }
            // });

        return res.status(200).json({ 
            success: "이미지 저장 완료",
            body: forAIdata
        });
        
        }

        catch (err) {
            console.error('❌ 처리 중 오류:', err);
            return res.status(500).json({ 
                error: '서버 오류' 
            });
        } 
    };

    async ExampleSort() {
        const response = await axios.get('http://ec2-3-1-2-125.ap-southeast-1.compute.amazonaws.com:8000/sortExample/');

        console.log(response.data)

        console.log("이미지 저장 시작")

        const base = response.data.images[0].image_base64
        const base64Data = base;
        const imageBuffer = Buffer.from(base64Data, 'base64');

        const saveDir = `/home/ubuntu/backendserver/app/images/5`
        // const saveDir = `/home/ubuntu/backendserver/app/images/${response.data.results[0].kimchi_num}`
        const savePath = path.join(saveDir, `example_abc.png`);

        // ✅ 디렉토리 생성 (동기)
        if (!fs.existsSync(saveDir)) {
            fs.mkdirSync(saveDir, { recursive: true });
            console.log('📁 디렉토리 생성됨:', saveDir);
        }

        // ✅ 이미지 저장 (동기)
        fs.writeFileSync(savePath, imageBuffer);
        console.log('✅ 이미지 저장 완료:', savePath);

        return res.status(200).json({ 
            success: "이미지 저장 완료",
        });
    }

}

module.exports = KimchiController;