#! /bin/bash

curl --location --request POST 'https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token' \
  --header 'Content-Type: application/x-www-form-urlencoded' \
  --data-urlencode 'grant_type=password' \
  --data-urlencode 'username=gus838@gmail.com' \
  --data-urlencode 'password=Ul!RsPWTPuw3' \
  --data-urlencode 'client_id=cdse-public'
