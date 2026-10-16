-- 1. Публичная таблица
CREATE TABLE public_profiles (
    id SERIAL PRIMARY KEY,
    last_name VARCHAR(100) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    mobile_phone VARCHAR(20) NOT NULL,
    home_phone VARCHAR(20) DEFAULT NULL,
    birth_date DATE NOT NULL,
    gender VARCHAR(10) NOT NULL,
    email VARCHAR(150) NOT NULL
);

-- 2. Приватная таблица
CREATE TABLE private_passports (
    profile_id INT PRIMARY KEY REFERENCES public_profiles(id) ON DELETE CASCADE,
    passport_series_number VARCHAR(20) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    middle_name VARCHAR(100),
    birth_date DATE NOT NULL,
    issue_date DATE NOT NULL,
    department_code VARCHAR(10) NOT NULL,
    issued_by TEXT NOT NULL,
    birth_address TEXT NOT NULL,
    actual_address TEXT NOT NULL,
    has_international_passport BOOLEAN NOT NULL DEFAULT FALSE
);

-- 3. Создание роли с ограниченным доступом
CREATE ROLE general_staff_role;
GRANT SELECT, INSERT, UPDATE ON public_profiles TO general_staff_role;
