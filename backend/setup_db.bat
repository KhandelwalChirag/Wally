@echo off

REM PostgreSQL setup script for Smart Cart Builder (Windows)

echo Setting up PostgreSQL for Smart Cart Builder...

REM Check if psql is available
psql --version >nul 2>&1
if %errorlevel% neq 0 (
    echo PostgreSQL is not installed or not in PATH.
    echo Please install PostgreSQL from https://www.postgresql.org/download/windows/
    echo Make sure to add PostgreSQL bin directory to your PATH
    pause
    exit /b 1
)

echo Creating database and user...

REM Database configuration
set DB_HOST=localhost
set DB_PORT=5432
set DB_NAME=smart_cart_db
set DB_USER=smart_cart_user
set DB_PASSWORD=smart_cart_password

REM Create user and database (you'll be prompted for postgres password)
echo Please enter the postgres user password when prompted:
psql -h %DB_HOST% -p %DB_PORT% -U postgres -c "CREATE USER %DB_USER% WITH PASSWORD '%DB_PASSWORD%';" 2>nul
psql -h %DB_HOST% -p %DB_PORT% -U postgres -c "CREATE DATABASE %DB_NAME% OWNER %DB_USER%;" 2>nul
psql -h %DB_HOST% -p %DB_PORT% -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE %DB_NAME% TO %DB_USER%;" 2>nul

echo Database setup completed!
echo Database URL: postgresql://%DB_USER%:%DB_PASSWORD%@%DB_HOST%:%DB_PORT%/%DB_NAME%
echo.
echo Update your .env file with:
echo DATABASE_URL=postgresql://%DB_USER%:%DB_PASSWORD%@%DB_HOST%:%DB_PORT%/%DB_NAME%
pause