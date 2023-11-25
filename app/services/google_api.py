from datetime import datetime

from pydantic import ValidationError

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"

NOW_DATE_TIME = datetime.now().strftime(FORMAT)

HEADER = [
    ["Отчет от", NOW_DATE_TIME],
    ["Топ Проектов ао скорости закрытия"],
    ["Название проекта", "Время сбора", "Описание"],
]


def check_table_size(rows: int, columns: int, table_values):
    for table_value in table_values:
        if len(table_value) > 3:
            raise ValidationError(f'Невозможно создать таблицу размера {rows} > 3')
        for value in table_value:
            if len(value) > 100:
                raise ValidationError(f'Невозможно создать таблицу размера {columns} > 100')


async def spreadsheets_create(wrapper_services: Aiogoogle):
    # Получаем текущую дату для заголовка документа
    # Создаём экземпляр класса Resourse
    service = await wrapper_services.discover("sheets", "v4")
    # Формируем тело запроса
    spreadsheet_body = dict(
        # Свойства документа
        properties=dict(
            title=f'Отчет от {NOW_DATE_TIME}',
            locale='ru_RU'
        ),
        # Свойства листов документа
        sheets=[dict(
            properties=dict(
                sheetType='GRID',
                sheetId=0,
                title='Sheet',
                gridProperties=dict(
                    rowCount=100,
                    columnCount=3
                )
            )
        )]
    )

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
        spreadsheet_id: str, charity_projects: list, wrapper_services: Aiogoogle
) -> None:
    rows = 100
    columns = 3
    service = await wrapper_services.discover("sheets", "v4")
    # Здесь формируется тело таблицы
    charity_projects = sorted(
        charity_projects, key=lambda timedelta: timedelta[1] - timedelta[2]
    )
    table_values = [
        *HEADER,
        *[list(map(str, [
            str(charity_project["name"]),
            str(charity_project["close_date"] -
                charity_project["create_date"]),
            str(charity_project["description"]),
        ]
        )) for charity_project in charity_projects],
    ]
    check_table_size(rows, columns, table_values)
    update_body = {"majorDimension": "ROWS", "values": table_values}
    return await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{rows}C{columns}',
            valueInputOption="USER_ENTERED",
            json=update_body,
        )
    )
