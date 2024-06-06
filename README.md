# SocialNetwork
Social network API


## Development

To install pre-commit hook.

```bash
pre-commit install
```

Run project with docker-compose

```bash
docker compose -f compose.yml -f compose.local.yml build
docker compose -f compose.yml -f compose.local.yml up
docker compose -f compose.yml -f compose.local.yml run social-network-app python3 manage.py migrate
```

Access via browser to API docs

1. [/api/schema/swagger-ui/](http://localhost:8000/api/schema/swagger-ui/)
2. [/api/schema/redoc/](http://localhost:8000/api/schema/redoc/)

It's also exported to [Postman Collection](https://www.postman.com/akay7/workspace/socialnetwork/overview)


## Nuances

API endpoints works for authenticated users apart from Login and Registration.

Authentication happened via JWT token.

JWT token possible to obtain via Registration or Login endpoints.
