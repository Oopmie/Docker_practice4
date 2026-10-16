-- Очищаем базу перед созданием
DROP TABLE IF EXISTS private_passports CASCADE;
DROP TABLE IF EXISTS public_profiles CASCADE;

-- 1. Создаем публичную таблицу
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

-- 2.Создаем приватную таблицу
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

-- 3. Безопасное создание роли
DROP ROLE IF EXISTS general_staff_role;
CREATE ROLE general_staff_role;

-- Раздаем права
GRANT SELECT, INSERT, UPDATE ON public_profiles TO general_staff_role;

-- Вывод схожих данных пользователей
select pp.*
from private_passports pp 
inner join(
select pp.middle_name ,pp.birth_address 
from private_passports pp 
group by pp.middle_name , pp.birth_address 
having COUNT (*)>1
)dup on pp.middle_name = dup.middle_name and pp.birth_address =dup.birth_adress 
order by pp.middle_name , pp.birth_address ;
