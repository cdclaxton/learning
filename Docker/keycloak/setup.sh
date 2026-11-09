# Login to Keycloak as the admin
docker exec keycloak-sso /opt/keycloak/bin/kcadm.sh config credentials \
  --server http://localhost:8080 \
  --realm master \
  --user admin \
  --password admin

# Create realm
docker exec keycloak-sso /opt/keycloak/bin/kcadm.sh create realms \
  -s realm=myrealm \
  -s enabled=true

# Create first app client
docker exec keycloak-sso /opt/keycloak/bin/kcadm.sh create clients \
  -r myrealm \
  -s clientId=app1 \
  -s enabled=true \
  -s publicClient=false \
  -s secret=app1-secret \
  -s 'redirectUris=["http://localhost:3000/*"]' \
  -s 'webOrigins=["http://localhost:3000"]' \
  -s directAccessGrantsEnabled=true

# Create second app client
docker exec keycloak-sso /opt/keycloak/bin/kcadm.sh create clients \
  -r myrealm \
  -s clientId=app2 \
  -s enabled=true \
  -s publicClient=false \
  -s secret=app2-secret \
  -s 'redirectUris=["http://localhost:3001/*"]' \
  -s 'webOrigins=["http://localhost:3001"]' \
  -s directAccessGrantsEnabled=true

# Create a user in the 'myrealm' realm
docker exec keycloak-sso /opt/keycloak/bin/kcadm.sh create users \
  -r myrealm \
  -s username=user1 \
  -s enabled=true \
  -s emailVerified=true \
  -s email=bob@hotmail.com \
  -s firstName=Bob \
  -s lastName=Cratchit

# Set the user's password
docker exec keycloak-sso /opt/keycloak/bin/kcadm.sh set-password \
  -r myrealm \
  --username user1 \
  --new-password user1
