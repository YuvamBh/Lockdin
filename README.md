# Lockdin — Career Intelligence Platform (Monorepo)

Infra-first setup for a real venture:
- Postgres 16 + pgvector (via Docker)
- App services added in later steps (FastAPI, Next.js)

## Quickstart

```bash
# copy env template
cp infra/.env.example infra/.env

# start db
cd infra
docker compose up -d db

# check health
docker compose ps
docker exec -it ci_db psql -U ci_user -d ci_main -c "SELECT extname FROM pg_extension;"
