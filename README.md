# Cinema Ticket Reservation System

## ER Diagram

![Diagram alt text](./ER-model.png)

### How to start server for local development:

```bash
docker compose up --build
```
Then follow the link: http://localhost:8000/docs

### How to build image:

```bash
docker build -f backend/Dockerfile -t backend backend/
```

### How to run tests:

```bash
docker run --rm -v $(pwd)/backend:$(pwd) --env PYTHONPATH=$(pwd) backend pytest
```