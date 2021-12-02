#!/bin/bash

mongo -- "admin" <<-EOJS
use admin
db.createUser(
    {
        user: "$MONGO_INITDB_ROOT_USERNAME",
        pwd: "$MONGO_INITDB_ROOT_PASSWORD",
        roles:["root"]
    }
);

var admin = db.getSiblingDB('admin');
admin.auth("$MONGO_INITDB_ROOT_USERNAME", "$MONGO_INITDB_ROOT_PASSWORD");

db=db.getSiblingDB("corpus_emagister_com");
db.createUser(
  {
    user: "emagister_com",
    pwd: "GMJaX9wRj5XWNwh3",
    roles: [ { role: "readWrite", db: "corpus_emagister_com" } ]
  }
);

db=db.getSiblingDB("corpus_emagister_it");
db.createUser(
  {
    user: "emagister_it",
    pwd: "cmSp2Vb7HRGmv15z",
    roles: [ { role: "readWrite", db: "corpus_emagister_it" } ]
  }
);
EOJS
