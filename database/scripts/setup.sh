#!/bin/bash

# Create the user
mongosh --host $MONGO_HOST --port $MONGO_PORT -u $MONGO_ROOT_USERNAME -p $MONGO_ROOT_PASSWORD --authenticationDatabase admin <<EOF
use $MONGO_CHATBOT_DATABASE
db.createUser({
  user: "$MONGO_USER",
  pwd: "$MONGO_PASSWORD",
  roles: [{ role: "readWrite", db: "$MONGO_CHATBOT_DATABASE" }]
})
EOF

echo "User $MONGO_USER created successfully in database $MONGO_CHATBOT_DATABASE"
