const express = require('express');
const app = require('../server').app;
const Connection = require('./config').Connection;
const bcrypt = require ('bcrypt');
var jwt = require('jsonwebtoken');


async function authenticate(email, password){
    var db = await Connection();
    if(db){
        var query = {email:email}
        const element = await db.collection('users').findOne(query)
        if(element){
            if(element['email']==email){
                return await bcrypt.compare(password, element['password']);
            }
        }    
    }
    return false;
}


exports.login = async function(req,res){
    let user = await authenticate(req.body['email'], req.body['password']);
    if(user){
        const token = jwt.sign(
            { user_id: user._id, 
            email: req.body['email'] },
            process.env.PASSWORD_SALT,
            {
              expiresIn: "2h",
            }
          );
          res.status(200).json({token: token});
    }
    else{
        res.status(400).json({message:"Unauthorized access"})
    }
}


exports.authenticateJWT = async function(req, res, next){
    const token = req.body['token'];

    if (token) {
        jwt.verify(token, process.env.PASSWORD_SALT, (err, user) => {
            console.log(user)
            if (err) {
                return res.sendStatus(403);
            }

            req.user = user;
            next();
        });
    } else {
        res.sendStatus(401);
    }
};