#!/usr/bin/bash

AUTH0_DOMAIN=$1 
AUTH0_CLIENT_ID=$2
AUTH0_CLIENT_SECRET=$3
AUTH0_AUDIENCE=$4

res=`curl -X POST -H 'Content-Type:application/json' --data '@-' ${AUTH0_DOMAIN} << EOF 
{ 
  "client_id": "$AUTH0_CLIENT_ID", 
  "client_secret": "$AUTH0_CLIENT_SECRET", 
  "audience": "$AUTH0_AUDIENCE", 
  "grant_type": "client_credentials" 
} 
EOF`   
parsed=`echo $res | jq -r .access_token` 
echo $parsed
