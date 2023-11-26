from datetime import datetime
from copy import deepcopy

from pydantic import ValidationError

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"


def get_now_time():
    return datetime.now().strftime(FORMAT)


HEADER = [
    [f"Отчет от {get_now_time()}"],
    ["Топ Проектов ао скорости закрытия"],
    ["Название проекта", "Время сбора", "Описание"],
]

SPREADSHEET_BODY = dict(
    # Свойства документа
    properties=dict(
        title='Актуальный отчёт',
        locale='ru_RU'
    ),
    # Свойства листов документа
    sheets=[dict(
        properties=dict(
            sheetType='GRID',
            sheetId=0,
            title='Sheet',
            gridProperties=dict(
                rowCount=settings.table_columns,
                columnCount=settings.table_rows
            )
        )
    )]
)


def check_table_size(table_values):
    for table_value in table_values:
        # Проверяем количество рядов в таблице
        if len(table_value) > settings.table_rows:
            raise ValidationError(
                f'Ошибка: Превышено ограничение по количеству рядов в таблице.'
                f' Лимит: {settings.table_rows}.'
                f' Пожалуйста, уменьшите количество рядов в таблице.'
            )
        for value in table_value:
            # Проверяем количество столбцов в таблице
            if len(value) > settings.table_columns:
                raise ValidationError(
                    f'Ошибка: Превышено ограничение по количеству столбцов в таблице.'
                    f' Лимит: {settings.table_columns}.'
                    f' Пожалуйста, уменьшите количество столбцов в таблице.'
                )


async def spreadsheets_create(wrapper_services: Aiogoogle):
    # Получаем текущую дату для заголовка документа
    spreadsheet_body = deepcopy(SPREADSHEET_BODY)
    spreadsheet_body['properties']['title'] = get_now_time()
    # Создаём экземпляр класса Resourse
    service = await wrapper_services.discover("sheets", "v4")
    # Формируем тело запроса
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )

    return response["spreadsheetId"], response["spreadsheetUrl"]


async def set_user_permissions(
        spreadsheet_id: str, wrapper_services: Aiogoogle
) -> None:
    permissions_body = {
        "type": "user",
        "role": "writer",
        "emailAddress": settings.email,
    }
    service = await wrapper_services.discover("drive", "v3")
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id, json=permissions_body, fields="id"
        )
    )


async def spreadsheets_update_value(
        spreadsheet_id: str,
        charity_projects: list,
        wrapper_services: Aiogoogle
) -> None:
    service = await wrapper_services.discover("sheets", "v4")
    # Здесь формируется тело таблицы
    charity_projects = sorted(
        charity_projects, key=lambda timedelta: timedelta[1] - timedelta[2]
    )
    table_values = [
        deepcopy(HEADER),
        *[list(map(str, [
            str(charity_project["name"]),
            str(charity_project["close_date"] -
                charity_project["create_date"]),
            str(charity_project["description"]),
        ]
        )) for charity_project in charity_projects],
    ]
    check_table_size(table_values)
    num_rows = len(table_values)
    num_columns = len(table_values[0]) if table_values else 0
    range_str = f'R1C1:R{num_rows}C{num_columns}'
    update_body = {"majorDimension": "ROWS", "values": table_values}
    return await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=range_str,
            valueInputOption="USER_ENTERED",
            json=update_body,
        )
    )
