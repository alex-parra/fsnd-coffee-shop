export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'alexparra.eu', // the auth0 domain prefix
    audience: 'fsnd-drinks.alex-parra.com', // the audience set for the auth0 app
    clientId: '1vztlBsibNgM6I3IKzBm5V70wOiGFDO8', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:4200', // the base url of the running ionic application.
  },
};
