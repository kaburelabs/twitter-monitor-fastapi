from fastapi import APIRouter, Body, HTTPException, Depends, Request
from config import settings
from schemas import schema as _schm
from typing import Optional, Dict, List
from services import services as _srvc
from datetime import datetime

conn_projlist2 = settings.get_db_projects()

router = APIRouter()


@router.get("/list", response_model=Dict, tags=["Projects"])
async def get_list_projects(request: Request):

    list_projs = await request.app.dbprojs["project-list"].find_one()
    complete_list = list_projs["project_names"]
    return {"total_projects": len(complete_list), "projects": complete_list}


@router.get(
    "/profile/{project}", response_model=_schm.ProjectDisplay, tags=["Projects"]
)
async def get_list_projects(project: str, request: Request):

    exception = HTTPException(
        status_code=400,
        detail="This project doesnt exists in our database. Consider suggesting it to us.",
    )

    project_history = await request.app.dbprojs["projects_card_data"].find_one(
        {"project_name": project}
    )

    if project_history:
        if type(project_history["created_at"]) == str:
            datetime_object = datetime.strptime(
                project_history["created_at"], "%m/%d/%Y %H:%M:%S"
            )
            project_history["created_at"] = datetime_object

        return project_history

    else:
        raise exception


def create_date(entry):
    new_copy = entry.copy()
    new_copy["date"] = new_copy.pop("_id")
    return new_copy




@router.get(
    "/history/{project}", response_model=_schm.OutputHistorical, tags=["Projects"]
)
async def get_project_history(project: str, request: Request):

    exception = HTTPException(
        status_code=400,
        detail="This project doesnt exists in our database. Consider suggesting it to us.",
    )

    projects = [
        create_date(x)
        async for x in request.app.dbprojs[project].find({}).sort("_id", -1)
    ]

    if projects:

        return {"project":project, "history": projects}

    else:
        raise exception


@router.get("/cards/", response_model=List[_schm.ProjectInCards], tags=["Projects"])
async def all_project_cards(request: Request):

    exception = HTTPException(
        status_code=400,
        detail="This project doesnt exists in our database. Consider suggesting it to us.",
    )

    projects = [x async for x in request.app.dbprojs["projects_card_data"].find()]

    if projects:

        return projects

    else:
        raise exception


@router.put("/update/{project}", response_model=_schm.ProjectDisplay, tags=["Projects"])
async def update_student_data(
    project: str,
    request: Request,
    req: _schm.UpdateProject = Body(...),
    current_user: _schm.User = Depends(_srvc.get_current_user),
):
    conn = request.app.dbprojs
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_student = await _srvc.update_project(conn, project, req)

    return updated_student
