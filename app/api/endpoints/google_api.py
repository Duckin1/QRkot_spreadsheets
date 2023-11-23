import requests
from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.services.google_api import (
    set_user_permissions,
    spreadsheets_create,
    spreadsheets_update_value,
)

router = APIRouter()


@router.post(
    "/", response_model=dict[str, str], dependencies=[Depends(current_superuser)]
)
async def get_report(
    session: AsyncSession = Depends(get_async_session),
    wrapper_services: Aiogoogle = Depends(get_service),
):
    projects = await charity_project_crud.get_projects_by_competion_rate(
        session,
    )
    projects_list = sorted(
        [
            {
                "name": project.name,
                "duration": project.close_date - project.create_date,
                "description": project.description,
            }
            for project in projects
        ],
        key=lambda x: x["duration"],
    )
    spreadsheet_id = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheet_id, wrapper_services)
    try:
        await spreadsheets_update_value(spreadsheet_id, projects_list, wrapper_services)
    except TypeError:
        return {"doc": "Предоставлены неправильные данные аккаунта"}
    except requests.ConnectionError:
        return {"doc": "Не правильный запрос"}
    return {"doc": "https://docs.google.com/spreadsheets/d/" + spreadsheet_id}
