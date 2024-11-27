:: Path: start.bat
@echo off
echo [+] Stopping existing containers...
docker-compose down

echo [+] Building/Updating the image...
docker-compose build

echo [+] Starting the application...
docker-compose up -d

echo [+] Waiting for the application to start...
timeout /t 5 /nobreak >nul

echo.
docker-compose ps
echo.

:: Check if the application is running
docker-compose ps | findstr "running" > nul
if %errorlevel% equ 0 (
    echo [+] Application started successfully!
    echo [+] Interface accessible at: http://127.0.0.1:8000
    echo [+] To view the logs: docker-compose logs -f
) else (
    echo [-] Error: the application did not start correctly.
    echo [+] Displaying logs:
    echo.
    docker-compose logs
)

echo.
echo To stop the application, press any key...
pause >nul