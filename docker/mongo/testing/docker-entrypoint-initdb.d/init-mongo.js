db.getSiblingDB('testing');
db.createUser({ user: 'admin',pwd: 'password',roles: [{role: 'readWrite',db: 'testing'}]});
db.start.insertOne({'name':'db_primer'});
