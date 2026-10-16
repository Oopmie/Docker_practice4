import psycopg2
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Разрешаем React-приложению слать запросы к бэкенду (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В продакшене лучше указать конкретный url фронтенда
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Настройки подключения к вашей базе данных в Docker
db_config = {
    "dbname": "identity_db",
    "user": "admin_user",
    "password": "super_secret_pwd",
    "host": "localhost",
    "port": "5433",
}


# Описываем структуру данных, которую мы ждем от React формы
class UserData(BaseModel):
    lastName: str
    firstName: str
    middleName: str | None = None
    mobilePhone: str
    homePhone: str | None = None
    birthDate: str
    gender: str
    email: str
    passportSeriesNumber: str
    passportIssueDate: str
    departmentCode: str
    issuedBy: str
    birthAddress: str
    actualAddress: str
    hasInternationalPassport: bool


@app.post("/api/save-profile")
async def save_profile(data: UserData):
    connection = None
    cursor = None
    try:
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()

        # 1. Вставляем данные в публичную таблицу и получаем сгенерированный ID
        insert_public_query = """
            INSERT INTO public_profiles (last_name, first_name, middle_name, mobile_phone, home_phone, birth_date, gender, email)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
        """
        cursor.execute(
            insert_public_query,
            (
                data.lastName,
                data.firstName,
                data.middleName,
                data.mobilePhone,
                data.homePhone if data.homePhone else None,
                data.birthDate,
                data.gender,
                data.email,
            ),
        )
        profile_id = cursor.fetchone()[0]

        # 2. Вставляем данные во вторую (приватную) таблицу, используя тот же ID
        insert_private_query = """
            INSERT INTO private_passports (profile_id, passport_series_number, last_name, first_name, middle_name, birth_date, issue_date, department_code, issued_by, birth_address, actual_address, has_international_passport)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cursor.execute(
            insert_private_query,
            (
                profile_id,
                data.passportSeriesNumber,
                data.lastName,
                data.firstName,
                data.middleName,
                data.birthDate,
                data.passportIssueDate,
                data.departmentCode,
                data.issuedBy,
                data.birthAddress,
                data.actualAddress,
                data.hasInternationalPassport,
            ),
        )

        # Подтверждаем транзакцию
        connection.commit()
        return {"status": "success", "message": "Данные успешно сохранены в БД!"}

    except Exception as e:
        if connection:
            connection.rollback()
        raise HTTPException(
            status_code=500, detail=f"Ошибка при записи в БД: {str(e)}"
        )
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
