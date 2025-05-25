const { Pool } = require('pg');

class Database {
  constructor() {
    this.pool = new Pool({
      user: 'postgres',
      host: process.env.DB_HOST || 'db',
      database: 'k2wi',
      password: '7872',
      port: 5432,
    });
  }
aa
  query(text, params) {
    return this.pool.query(text, params);
  }
}

module.exports = new Database();
