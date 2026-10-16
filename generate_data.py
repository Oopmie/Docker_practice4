import random
from datetime import datetime
import psycopg2
from faker import Faker

# Инициализируем Faker с русской локалью
fake = Faker("ru_RU")

# Конфигурация подключения к PostgreSQL
db_config = {
    "dbname": "identity_db",
    "user": "admin_user",
    "password": "super_secret_pwd",
    "host": "localhost",
    "port": "5433"
}

def generate_data(records_count=1000):
    connection = None
    cursor = None
    try:
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()
        print(f"Начало генерации и вставки {records_count} записей...")

        for _ in range(records_count):
            # Определяем пол для генерации консистентных ФИО
            gender_code = random.choice(["male", "female"])
            gender_str = "Мужской" if gender_code == "male" else "Женский"

            if gender_code == "male":
                first_name = fake.first_name_male()
                last_name = fake.last_name_male()
                middle_name = fake.middle_name_male()
            else:
                first_name = fake.first_name_female()
                last_name = fake.last_name_female()
                middle_name = fake.middle_name_female()

            birth_date = fake.date_of_birth(minimum_age=18, maximum_age=70)

            # --- Данные для первой таблицы (публичной) ---
            mobile_phone = fake.phone_number()
            home_phone = fake.phone_number() if random.random() > 0.3 else None
            email = fake.ascii_free_email()

            insert_public_query = """
                INSERT INTO public_profiles (last_name, first_name, middle_name, mobile_phone, home_phone, birth_date, gender, email)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id;
            """
            cursor.execute(insert_public_query, (last_name, first_name, middle_name, mobile_phone, home_phone, birth_date, gender_str, email))
            profile_id = cursor.fetchone()[0]

            # --- Данные для второй таблицы (приватной) ---
            passport_series_number = f"{random.randint(10, 99)} {random.randint(10, 99)} {random.randint(100000, 999999)}"

            start_issue_year = max(birth_date.year + 14, 2000)
            try:
                issue_date = fake.date_between_dates(date_start=datetime(start_issue_year, 1, 1), date_end=datetime(2026, 1, 1))
            except Exception:
                issue_date = datetime(2025, 1, 1).date()

            department_code = f"{random.randint(100, 999)}-{random.randint(100, 999)}"
            issued_by = f"ТП №{random.randint(1, 10)} ОУФМС РОССИИ ПО {fake.region().upper()}"
            birth_address = fake.address()
            actual_address = birth_address if random.random() > 0.4 else fake.address()
            has_international_passport = random.choice([True, False])

            insert_private_query = """
                INSERT INTO private_passports (profile_id, passport_series_number, last_name, first_name, middle_name, birth_date, issue_date, department_code, issued_by, birth_address, actual_address, has_international_passport)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """
            cursor.execute(insert_private_query, (profile_id, passport_series_number, last_name, first_name, middle_name, birth_date, issue_date, department_code, issued_by, birth_address, actual_address, has_international_passport))

        connection.commit()
        print("Успешно! 1000 связанных записей добавлены в БД.")

    except Exception as error:
        print(f"Ошибка при работе с PostgreSQL: {error}")
        if connection:
            connection.rollback()
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

if __name__ == "__main__":
    generate_data()
