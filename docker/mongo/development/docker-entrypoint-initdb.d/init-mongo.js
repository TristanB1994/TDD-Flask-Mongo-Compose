db.getSiblingDB('registry');
db.createUser({ user: 'admin',pwd: 'password',roles: [{role: 'readWrite',db: 'registry'}]});
db.start.insertOne({'name':'db_primer'});
