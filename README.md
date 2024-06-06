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

Access via browser to API

(http://localhost:8000/api/schema/swagger-ui/)[http://localhost:8000/api/schema/swagger-ui/]

It's exported to (Postman Collection)[https://www.postman.com/akay7/workspace/socialnetwork/overview]
