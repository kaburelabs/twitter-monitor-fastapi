from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utils.tasks import repeat_every

from datetime import datetime

from config import settings
from services import update_twitter as _twitter
from routes import general, users
from routes import projects


SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES = settings.settings()


origins = [
    "*",
]

app = FastAPI()

app.include_router(general.router)
app.include_router(
    users.router,
    prefix="/user",
)
app.include_router(projects.router, prefix="/projects")


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def setup_database() -> None:
    app.dbusers = settings.get_db_users()
    app.dbprojs = settings.get_db_projects()


@repeat_every(seconds=60)
async def get_twitter_data() -> None:
    fulldate = datetime.utcnow().replace(second=0, microsecond=0)
    hour_minute = fulldate.strftime("%H:%M")
    print("runned here")

    if hour_minute in [f"{str(hr).zfill(2)}:00" for hr in range(1, 23, 1)]:

        list_projs = await app.dbprojs["project-list"].find_one()
        complete_list = list_projs["project_names"]
        await _twitter.projects_list(complete_list, fulldate)

        print(f"updated at: {fulldate}")

    else:
        print(f"Nothing to update at: {hour_minute}")
        pass


@app.on_event("shutdown")
def shutdown_event():
    print("going down")
    fulldate = datetime.utcnow().replace(second=0, microsecond=0)
    with open("log.txt", mode="a") as log:
        log.write(f"finished at {fulldate}\n")
