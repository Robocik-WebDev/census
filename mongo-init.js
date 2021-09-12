db.users.drop()
db = new Mongo().getDB("test");

db.createCollection("fields",{
    validator: {
        $jsonSchema:{
            bsonType: "object",
            required: [ "name", "type",],
            properties: {
                name:{
                    bsonType: "string",
                    description: "Nazwa pola"
                },
                type: {
                    bsonType:"string",
                    description: "Jakiego typu pole przechowuje dane"
                }
            }
        }
    }
})


db.createCollection("users",{
    validator: {
        $jsonSchema:{
            bsonType: "object",
            required: [ "name", "last_name", "password", "email" ],
            properties: {
                name: {
                    bsonType: "string",
                    description: "Imie użytkownika"
                },
                last_name: {
                    bsonType: "string",
                    description: "Nazwisko użytkownika"
                },
                password: {
                    bsonType: "string",
                    description: "Zaszyfrowane hasło użytkownika"
                },
                email: {
                    bsonType: "string",
                    description: "Adres email użytkownika"
                }
            }
        }
    }
})

db.fields.insertMany([
    {name:"name", type:"string", public:true, required:true},
    {name:"last_name", type:"string",public:true, required:true},
    {name:"password", type:"string", required:true},
    {name:"email", type:"string",public:true, required:true}
])

db.dropAllUsers()
db.createUser({
    user:_getEnv('MONGO_USERNAME'),
    pwd:_getEnv('MONGO_PASSWORD'),
    roles:[{
        role:"readWrite",
        db:_getEnv('MONGO_INITDB_DATABASE')
    }]
});