const {MongoClient} = require('mongodb');


const config = {
    "HASH_SECRET":process.env.PASSWORD_SALT,
    // "DB_USER":"user",
    // "DB_PASSWORD":"abcdef",
    // "DB_USER":"administrator",
    // "DB_PASSWORD":"zaq1WSX",
    "DB_USER":process.env.MONGO_USERNAME,
    "DB_PASSWORD":process.env.MONGO_PASSWORD,
    "DB_NAME":process.env.MONGO_INITDB_DATABASE,
    "DB_HOST":process.env.MONGO_HOST
}

const uri = `mongodb://${config.DB_USER}:${config.DB_PASSWORD}@${config.DB_HOST}:27017/${config.DB_NAME}`
let db;

const Connection = async () => {
    if (db) {
        return db;
    }
    try {
        console.log(uri)
        console.log("starting")
        const client = await MongoClient.connect(uri);
        console.log("client set")
        db = client.db(config.DB_NAME);
        
        console.log("allesGut")
    } catch (err) {
        console.log(err);
    }
    return db;
};


module.exports = {config, Connection};
