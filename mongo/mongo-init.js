db.createCollection("texts", {
    validator: {
      $jsonSchema: {
        bsonType: "object",
        required: [
          "_id",
          "filename",
          "file_id",
        ],
        properties: {
          _id: {
            bsonType: "objectId",
          },
          filename: {
            bsonType: "string",
          },
          created_at: {
            bsonType: "date",
          },
          status: {
            bsonType: "string",
          },
        },
      },
    },
  });


  db.createCollection("roles");

  db.roles.insertMany([
    {
       _id: '12345678abcdef',
       role: 'admin',
       role_definition: 'grants all access rights to the project'
     },
     {
      _id: '01234567bcdefg',
      role: 'user',
      role_definition: 'grants standard read and access rights to the user'
     },
    
   ]);
  
   db.createCollection("project");

   db.createCollection("users");

   db.users.insertMany([
     {
        _id: "12365fcf33722dc242f74321",
        email: 'admin@admin.de',
        username: 'admin',
        password: 'TestPW',
        role: [{'project_id': '', 'role':'admin'}],
        hashed_password: "$2b$12$AJLKmkbLrrV/wCPXkohJyu9ve//p3Usd/IzLgbS.4OZr0w6FR64lS"
      }
     
    ]);


  db.createUser({
    user: "test_user",
    pwd: "c0nt5xt!",
    roles: [
      {
        role: "readWrite",
        db: "contextualiser",
      },
    ],
  });