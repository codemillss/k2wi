const db = require('../config/Database');
const path = require('path');
const axios = require("axios");

class kimchimodel {
   
    async findKimchiData() {
        const result = await db.query(`
            SELECT *
            FROM k2wi_schema.kimchi_info
        `);
        
        return result;
    }

    //사용자가 만드는 레시피를 데이터베이스에 삽입
    async user_made_kimchi_recipe(kimchi_name, recipe_list) {

        const select_num = await db.query(
            `
            SELECT COUNT(*)
            FROM k2wi_schema.kimchi_info 
            `
        );

        const serieal_num = parseInt(select_num.rows[0].count) + 1;

        console.log(serieal_num);

        console.log(await kimchi_name);
        console.log(await recipe_list);

        for(let i = 0; i < recipe_list.length; i++) {

            console.log(recipe_list[i].recipe_order + " : " + recipe_list[i].recipe_detail)

        }

        await db.query(
            `INSERT INTO k2wi_schema.kimchi_info (kimchi_num, kimchi_name) VALUES ($1, $2) RETURNING *;`,
            [parseInt(serieal_num), kimchi_name]
        );

        for(let i = 0; i < recipe_list.length; i++) {
            await db.query(
                `
                INSERT INTO k2wi_schema.recipe_list (kimchi_num, recipe_order, recipe_detail) VALUES ($1, $2, $3);
                `
                ,[parseInt(serieal_num), recipe_list[i].recipe_order, recipe_list[i].recipe_detail]
            )
        }
        
        const data_for_ai = await db.query(`
            SELECT k.kimchi_num, k.kimchi_name, r.recipe_order, r.recipe_detail
            FROM k2wi_schema.kimchi_info k
            JOIN k2wi_schema.recipe_list r ON k.kimchi_num = r.kimchi_num
            WHERE k.kimchi_num = ${serieal_num}
            ORDER BY k.kimchi_num, r.recipe_order
        `);


        console.log(data_for_ai.rows)

        return data_for_ai.rows
    }

    async find_kimchi_with_name(name) {
        const result = await db.query(`
            
            SELECT *
            FROM k2wi_schema.kimchi_info
            WHERE kimchi_name = ${name}
            
        `);
        
        return result.rows[0];
    }

    async find_kimchi_recipe_with_name(num) {
        const result = await db.query(`
            
            SELECT *
            FROM k2wi_schema.recipe_list
            WHERE kimchi_num = ${num}
            
        `);
        console.log(result);
        return result.rows;
    }

    async kimchidata() {
        console.log(__dirname)
        const file = path.join('doraemong.png')
        return file;
    }

    async Database_status_check() {
        try {
            const result = await db.query(`
            
                SELECT *
                FROM k2wi_schema.recipe
                
            `);
            return true;
        } catch (err) {
            if(err.message.includes('schema') && err.message.includes('does not exist')) {
                return false;
            } 
        }
        // if(result == `ERROR:  relation "k2wi_schema.recipe" does not exist`)
    }

    async postImage(kimchi_num) {
        const res = await db.query(`
            SELECT k.kimchi_num, k.kimchi_name, r.recipe_order, r.recipe_detail
            FROM k2wi_schema.kimchi_info k
            JOIN k2wi_schema.recipe_list r ON k.kimchi_num = r.kimchi_num
            WHERE k.kimchi_num = ${kimchi_num}
            ORDER BY k.kimchi_num, r.recipe_order
            `);

        console.log(res);

        return res
    }

    // async InsertImage(kimchi_num, recipe_order, recipe_detail, prompts) {
    //     const result = await db.query(`
    //         INSERT INTO k2wi_schema.recipe_list (kimchi_num, recipe_order, recipe_detail, prompts) VALUES ($1, $2, $3, $4);
    //     `, [kimchi_num, recipe_order, recipe_detail, prompts]);
    // }


    async findKimchinum() {
        const result = await db.query(`
            SELECT k.kimchi_num
            FROM k2wi_schema.kimchi_info k
        `);
        
        return result;
    }

    async InsertImage(kimchi_num, recipe_order , recipe_image_name, recipe_image_path) {
        await db.query(`
            INSERT INTO k2wi_schema.recipe_order_image (kimchi_num, recipe_order, recipe_image_name, recipe_image_path) VALUES ($1, $2, $3, $4);
        `, [kimchi_num, recipe_order, recipe_image_name, recipe_image_path]
        );
    }

    //이미지와 매칭
    async InsertTotalRecipe(kimchi_num, recipe_order, recipe_detail) {
        await db.query(`
            INSERT INTO k2wi_schema.recipe_list_total (kimchi_num, recipe_order, recipe_detail) VALUES ($1, $2, $3);
        `, [kimchi_num, recipe_order, recipe_detail]
        );
    }

    async JoinImageAndTotalRecipe(kimchi_num) {
        const res = await db.query(`
            SELECT ki.kimchi_num, ki.kimchi_name, rlt.recipe_order, rlt.recipe_detail, roi.recipe_image_name, roi.recipe_image_path
            FROM k2wi_schema.kimchi_info ki
            JOIN k2wi_schema.recipe_list_total rlt ON ki.kimchi_num = rlt.kimchi_num
            LEFT JOIN k2wi_schema.recipe_order_image roi ON rlt.kimchi_num = roi.kimchi_num AND rlt.recipe_order::text = roi.recipe_order
            WHERE ki.kimchi_num = ${kimchi_num}
            ORDER BY rlt.recipe_order;
        `);
        
        return res.rows
    }


}

module.exports = kimchimodel;