
const dfd = require("danfojs-node");
const db = require("./config/Database");

class insertdata {

  async loadCSV() {
    const df = await dfd.readCSV("temple_recipe_forGood.csv", { index: false });

    const kimchi_info = df.loc({columns: ["num", "name"]});
    kimchi_info.head().print()

    const rows = kimchi_info.values;

    for (const [num, name] of rows) {
      try {
        // 🔥 문자열을 실제 배열로 파싱
        // const tags = eval(tagstr); // 주의: 신뢰된 데이터만 사용
  
        console.log(`🍽️ [${num}] ${name}`);

        await db.query(
          `INSERT INTO k2wi_schema.kimchi_info(kimchi_num, kimchi_name) VALUES ($1, $2) RETURNING *`,
          [num, name]
        )
        console.log(`${num} , ${name} : 성공`)
        console.log("------");
      } catch (err) {
        console.error(`❌ 레시피 파싱 실패 (${num} : ${name}):`, err.message);
      }
    }
  }

  async insertrecipes() {

    const df = await dfd.readCSV("temple_recipe_forGood.csv", { index: false });

    const num_name_recipes = df.loc({columns: ["num", "recipes"]});

    num_name_recipes.head().print()

    const rows = num_name_recipes.values;

    for (const [num, recipes] of rows) {
      try {
        // 🔥 문자열을 실제 배열로 파싱
        const recipe = eval(recipes); // 주의: 신뢰된 데이터만 사용

        console.log(`🍽️ [${num}]`);

        for(let j = 0; j < recipe.length; j++) {
          await db.query(
            `INSERT INTO k2wi_schema.recipe_list(kimchi_num, recipe_order, recipe_detail) VALUES ($1, $2, $3) RETURNING *`,
            [num, j+1, recipe[j]]
          )
        }

        console.log("------");
      } catch (err) {
        console.error(`❌ 레시피 파싱 실패 (${num} : ${recipes}):`, err.message);
      }
    }

  }

  async insertingredients() {

    const df = await dfd.readCSV("temple_recipe_forGood.csv", { index: false });

    const num_name_ingredeints = df.loc({columns: ["num", "name", "ingredients"]});

    num_name_ingredeints.head().print()

    const rows = num_name_ingredeints.values;

    for (const [num, name, ingredients] of rows) {
      try {
        console.log(`🍽️ [${num}] ${name}`);

        await db.query(
          `INSERT INTO k2wi_schema.ingredients_list(kimchi_num, kimchi_name, ingredient) VALUES ($1, $2, $3) RETURNING *`,
          [num, name, ingredients]
        )
        console.log(`${num} , ${name} : 성공`)
      } catch (err) {
        console.error(`❌ 레시피 파싱 실패 (${num} : ${name}):`, err.message);
      }
    }

  }

}

module.exports = insertdata;