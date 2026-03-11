# FinCubes FAQ Bot
## Deploy
```bash
py -m app.main
```
```bash
docker-compose up
```
## Env
```env
ENV=

PATHS__CONSTANTS="./config/constants.yml"
PATHS__MESSAGES="./config/messages.yml"
PATHS__COMMANDS="./config/commands.yml"
PATHS__REQUESTS="./config/requests.yml"

TG_TOKEN=
TG_ADMINS=[]

DB_NAME=
DB_USER=
DB_PASS=
DB_HOST=

REDIS_HOST=
REDIS_PASS=
REDIS_LONG_TTL=
REDIS_SHORT_TTL=

REQUESTS__FOLDER_ID=
REQUESTS__IAM_TOKEN=

QN_SIM_THRESHOLD=0.8
```