#!/bin/bash

# Create the user
mongosh --host $MONGO_HOST --port $MONGO_PORT -u $MONGO_ROOT_USERNAME -p $MONGO_ROOT_PASSWORD --authenticationDatabase admin <<EOF
use admin
db.createUser({
  user: "$MONGO_USER",
  pwd: "$MONGO_PASSWORD",
  roles: [{ role: "readWrite", db: "$MONGO_CHATBOT_DATABASE" }]
})
EOF

echo "User $MONGO_USER created successfully in database admin"
