const config = require('./config').config;
const fs = require('fs');
const bcrypt = require ('bcrypt');
const Connection = require('./config').Connection



async function validate_email(email){
    var db = await Connection();
    if(db){
        const cursor = db.collection('users').find({email:email})
        var count = await cursor.count()
        return count === 0
    }
}

async function insert_record(collection, object){
    var db = await Connection();
    if(db){
        db.collection(collection).insertOne(object, function(err,res) {
            if (err){
                console.log(err);
                throw err;
            } 
            return true; 
        })
    }
}


async function add_user(name, last_name, email, password){
    console.log('adding')
    var test = await validate_email(email)

    console.log(test)
    if(test){
        console.log('test passed')
        var pwd = await salt_password(password);
        var object = {'name':name, 'last_name':last_name, 'password':pwd, 'email':email};
        insert_record('users', object).then(complete =>{
            if(complete)
                console.log("User added")
        })
    }
    
}

/**
 * Function used to hash password using bcrypt
 * @param {string} password password to hash 
 * @returns hashed password
 */
async function salt_password(password){
    const salt = await bcrypt.genSalt(10)
    const hash = await bcrypt.hash(password, salt)
    return hash
}




module.exports = {validate_email, salt_password, add_user}
require('make-runnable');