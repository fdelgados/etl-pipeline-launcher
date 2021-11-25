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

db=db.getSiblingDB("$MONGO_INITDB_DATABASE");
db.createUser(
  {
    user: "$MONGO_INITDB_USER",
    pwd: "$MONGO_INITDB_PASSWORD",
    roles: [ { role: "readWrite", db: "$MONGO_INITDB_DATABASE" } ]
  }
)
EOJS
