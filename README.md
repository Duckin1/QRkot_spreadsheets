# Проект QR-кот
_____
### Описание проекта
 Сервис регистрации проектов по сбору пожертвований на 
 различные целевые проекты: на медицинское обслуживание 
 нуждающихся хвостатых, на обустройство кошачьей колонии 
 в подвале, на корм оставшимся без попечения кошкам — на 
 любые цели, связанные с поддержкой кошачьей популяции.
 ___
### Используемые технологии
`Python 3.10.11` 
`FastAPI 0.78` 
`SQLAlchemy 1.4.36`
`Uvicorn v0.17.6`
`Aiogoogle v5.6.0`
___
### Установка и запуск
Клонируйте репозиторий, установите виртуальное окружение:
```commandline
git clone https://github.com/Duckin1/cat_charity_fund.git
cd cat_charity_fund/
python -m venv venv
```
В корневой директории создайте файл `.env` следующего содержания:
```commandline
APP_TITLE=App QRKot
APP_DESCRIPTION=**Donation collection service to support kitties.**
DATABASE_URL=sqlite+aiosqlite:///./fastapi.db 
SECRET=NqyCP8-cGyGat-uJOt2o
TYPE=service_account
PROJECT_ID="opportune-lore-369911"
PRIVATE_KEY_ID="1b30aa142b6ef92c824edcf6536e81e8092daaa5"
PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\nMIIEvAIT+YUw==\n-----END PRIVATE KEY-----\n"
CLIENT_EMAIL="service-account@opportune-lore-369911.iam.gserviceaccount.com"
CLIENT_ID="112473947934508090513"
AUTH_URI="https://accounts.google.com/o/oauth2/auth"
TOKEN_URI="https://oauth2.googleapis.com/token"
AUTH_PROVIDER_X509_CERT_URL="https://www.googleapis.com/oauth2/v1/certs"
CLIENT_X509_CERT_URL="https://www.googleapis.com/robot/v1/metadata/x509/service-account%40opportune-lore-369911.iam.gserviceaccount.com"
EMAIL=email@gmail.com

```
Активируйте виртуальное окружение
```
source venv/bin/activate - для Linux
source venv/Scripts/activate - для Windows
```
Установите в виртуальное окружение необходимые зависимости:
```commandline
python -m pip install --upgrade pip
pip install -r requirements.txt
```
Создайте базу с помощью команд:
```commandline
alembic init alembic
alembic revision --autogenerate -m "First migration"
```
Запустите проект:
```commandline
uvicorn app.main:app 
```
___
### Возможности проекта

**Проекты**

В Фонде QRKot может быть открыто несколько целевых проектов.
У каждого проекта есть название, описание и сумма, которую 
планируется собрать. После того, как нужная сумма собрана — проект закрывается.

Пожертвования в проекты поступают по принципу First In, First Out: 
все пожертвования идут в проект, открытый раньше других; 
когда этот проект набирает необходимую сумму и закрывается — 
пожертвования начинают поступать в следующий проект.

**Пожертвования**

Каждый пользователь может сделать пожертвование и сопроводить его комментарием. 
Пожертвования не целевые: они вносятся в фонд, а не в конкретный проект. 
Каждое полученное пожертвование автоматически добавляется в 
первый открытый проект, который ещё не набрал нужную сумму. 
Если пожертвование больше нужной суммы или же в Фонде нет открытых проектов — 
оставшиеся деньги ждут открытия следующего проекта. 
При создании нового проекта все неинвестированные пожертвования автоматически 
инвестируются в новый проект.

**Пользователи**

- Целевые проекты создаются администраторами сайта.
- Любой пользователь может видеть список всех проектов, 
включая требуемые и уже внесенные суммы. Это касается всех проектов — 
и открытых, и закрытых.
- Зарегистрированные пользователи могут отправлять пожертвования и 
просматривать список своих пожертвований.
___

### Документация
Подробная документация к API проекта находится по адресу `http://127.0.0.1:8000/docs` или `http://127.0.0.1:8000/redoc`
___
### Автор
Миннибаев Алмаз https://github.com/Duckin1
