# sso auth service

This is the authentication service. And it will be used by other services for authentication.

It contains login/signup feature.

# How it works

Once user signup or login, they will get access and refresh token.

While making request to anyother microservice, they just need to pass the access token in

the header.

# How to connect other microservices with this sso service.

- Create a directory called vault in the root directory of new service.
- copy the jwt_key.pub from sso service and past in the vault directory of the new microservice.
- Use this file as verifying key in jwt token settings.

`'VERIFYING_KEY': open(RSA_PUBLIC_KEY_FILE, 'r').read(),`

# Tech stack

- python 3.10
- django 3.2
- django rest framework 5.2.0
- postgres

# Local setup

- clone the repo
- Run command `make start`
- In another terminal execute this command to generate private and public key  `make generate_key`
