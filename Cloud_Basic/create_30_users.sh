#!/bin/bash

# Define the base URL of your Nextcloud instance
NEXTCLOUD_URL="http://localhost:8080"

# Define credentials for an admin user
ADMIN_USERNAME="mubashar"
ADMIN_PASSWORD="Mubashar64."

# Loop to create 30 users
for i in {1..30}; do
    # Generate username and password for each user
    USERNAME="user$i"
    PASSWORD="password$i"
    
    # Create the user using the Nextcloud API
    curl -X POST -u "${ADMIN_USERNAME}:${ADMIN_PASSWORD}" "${NEXTCLOUD_URL}/ocs/v2.php/cloud/users" \
         -d "userid=${USERNAME}" \
         -d "password=${PASSWORD}" \
         -d "displayname=User ${i}" \
         -d "email=user${i}@example.com"

    # Print user creation status
    echo "User ${USERNAME} created with password: ${PASSWORD}"
done
