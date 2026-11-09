const express = require('express');
const session = require('express-session');
const Keycloak = require('keycloak-connect');
const app = express();
const memoryStore = new session.MemoryStore();

app.use(session({
  secret: 'some-secret',
  resave: false,
  saveUninitialized: true,
  store: memoryStore,
  cookie: {
    httpOnly: true,
    secure: false,
    sameSite: 'lax'
  }
}));

const KEYCLOAK_URL = process.env.KEYCLOAK_URL || 'http://localhost:8080';

const keycloakConfig = {
  'realm': 'myrealm',
  'auth-server-url': KEYCLOAK_URL,
  'ssl-required': 'none',
  'resource': 'app2',
  'credentials': {
    'secret': 'app2-secret'
  },
  'confidential-port': 0,
  'bearer-only': false
};

const keycloak = new Keycloak({ store: memoryStore }, keycloakConfig);

app.use(keycloak.middleware({
  logout: '/logout',
  admin: '/'
}));

// Public route
app.get('/', (req, res) => {
  res.send(`
    <h1>App 2</h1>
    <p><a href="/protected">Protected Page</a></p>
    <p><a href="http://localhost:3000/protected">Go to App 1 Protected</a></p>
  `);
});

app.get('/api/get-token', keycloak.protect(), (req, res) => {
  res.json({
    token: req.kauth.grant.access_token.token,
    expires: req.kauth.grant.access_token.content.exp
  });
});

// Protected route with CORS test
app.get('/protected', keycloak.protect(), (req, res) => {
  const token = req.kauth.grant.access_token.token;
  const tokenExp = req.kauth.grant.access_token.content.exp;

  res.send(`
    <h1>App 2 - Protected</h1>
    <p>Logged in as: ${req.kauth.grant.access_token.content.preferred_username}</p>

    <p><a href="#" onclick="fetchUserInfo(); return false;">Fetch User Profile (CORS Test)</a></p>

    <script>
      let token = '${token}';
      let tokenExp = ${tokenExp};

      function getTimeLeft() {
        return tokenExp - Math.floor(Date.now() / 1000);
      }

      async function rotateToken() {
        const resp = await fetch('/api/get-token');
        const data = await resp.json();

        return {
          t: data.token,
          e: data.expires
        };
      }

      async function fetchUserInfo() {
        const resultDiv = document.getElementById('result');
        resultDiv.innerHTML = 'Loading...';

        try {
          const { t, e } = await rotateToken();

          token = t;
          tokenExp = e;

          const timeLeft = getTimeLeft();

          resultDiv.innerHTML = '<h3>Token Status:</h3>' +
            '<p>Expires in: ' + timeLeft + ' seconds ' +
            (timeLeft > 0 ? '(valid)' : '(EXPIRED)') + '</p>' +
            '<p>Testing CORS...</p>';

          const response = await fetch('${KEYCLOAK_URL}/realms/myrealm/protocol/openid-connect/userinfo', {
            headers: {
              'Authorization': 'Bearer ' + token,
              'Accept': 'application/json'
            }
          });

          if (!response.ok) throw new Error('Request failed - token expired?');

          const userInfo = await response.json();
          resultDiv.innerHTML = '<h3>Token Status:</h3>' +
            '<p>Expires in: ' + timeLeft + ' seconds</p>' +
            '<h3>CORS Working! User Profile:</h3>' +
            '<pre>' + JSON.stringify(userInfo, null, 2) + '</pre>';
        } catch (error) {
          const timeLeft = getTimeLeft();

          resultDiv.innerHTML = '<h3>Token Status:</h3>' +
            '<p>Expires in: ' + timeLeft + ' seconds ' +
            (timeLeft > 0 ? '(should be valid)' : '(EXPIRED)') + '</p>' +
            '<h3>Error:</h3>' +
            '<p style="color:red">' + error.message + '</p>';
        }
      }
    </script>

    <p><a href="http://localhost:3000/protected">Go to App 1 (should not require login)</a></p>
    <p><a href="/logout">Logout</a></p>

    <div id="result"></div>
  `);
});

app.listen(3001, () => {
  console.log('App 2 running on http://localhost:3001');
});