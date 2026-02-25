@echo off
:: containers.bat — Create, start, and manage Docker Compose services
::
:: Usage: scripts\containers.bat [COMMAND]
::
:: Commands:
::   (none) | start   Create containers if they do not exist, then start them
::   stop             Stop all running containers (data is preserved)
::   restart          Stop then start all containers
::   status           Show the current state of every container
::   logs [service]   Stream logs (all services, or one specific service)
::   down             Stop and remove containers (volumes are preserved)
::   destroy          Stop and remove containers AND all volumes  WARNING: deletes DB data
::   help             Print this help message

setlocal EnableDelayedExpansion

:: ── Resolve project root (parent of scripts\) ────────────────────────────────
set "SCRIPT_DIR=%~dp0"
:: Strip trailing backslash from SCRIPT_DIR
if "%SCRIPT_DIR:~-1%"=="\" set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"
:: Go one level up to project root
for %%I in ("%SCRIPT_DIR%") do set "PROJECT_ROOT=%%~dpI"
:: Strip trailing backslash
if "%PROJECT_ROOT:~-1%"=="\" set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"

cd /d "%PROJECT_ROOT%"

:: ── Parse command ─────────────────────────────────────────────────────────────
set "COMMAND=%~1"
if "%COMMAND%"=="" set "COMMAND=start"

if /i "%COMMAND%"=="start"   goto :cmd_start
if /i "%COMMAND%"=="stop"    goto :cmd_stop
if /i "%COMMAND%"=="restart" goto :cmd_restart
if /i "%COMMAND%"=="status"  goto :cmd_status
if /i "%COMMAND%"=="logs"    goto :cmd_logs
if /i "%COMMAND%"=="down"    goto :cmd_down
if /i "%COMMAND%"=="destroy" goto :cmd_destroy
if /i "%COMMAND%"=="help"    goto :cmd_help
if /i "%COMMAND%"=="-h"      goto :cmd_help
if /i "%COMMAND%"=="--help"  goto :cmd_help

echo [ERROR] Unknown command: '%COMMAND%'
echo.
goto :cmd_help

:: ── Preflight checks ─────────────────────────────────────────────────────────

:check_docker
    docker info >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Docker daemon is not running.
        echo         Start Docker Desktop and try again.
        exit /b 1
    )
    docker compose version >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Docker Compose plugin ^(v2^) is not available.
        echo         Update Docker Desktop to get it.
        exit /b 1
    )
    exit /b 0

:check_env
    if not exist ".env" (
        echo [WARN]  .env file not found.
        if exist ".env.example" (
            echo.
            echo         Run the following to create it:
            echo           copy .env.example .env
            echo         Then edit .env and set POSTGRES_PASSWORD, ENCRYPTION_KEY_SECRET,
            echo         and GEN_AI_API_KEY.
        )
        echo.
        echo [ERROR] Aborting. Create .env before starting the containers.
        exit /b 1
    )
    exit /b 0

:containers_exist
    :: Returns errorlevel 0 if at least one container exists (running or stopped)
    for /f "delims=" %%i in ('docker compose ps -a --quiet 2^>nul') do (
        exit /b 0
    )
    exit /b 1

:: ── Commands ─────────────────────────────────────────────────────────────────

:cmd_start
    call :check_docker
    if errorlevel 1 exit /b 1

    call :check_env
    if errorlevel 1 exit /b 1

    call :containers_exist
    if errorlevel 1 (
        echo [INFO]  No containers found -- pulling images and creating containers...
        docker compose up -d --pull missing
    ) else (
        echo [INFO]  Containers already exist -- starting any that are stopped...
        docker compose start
    )

    if errorlevel 1 (
        echo [ERROR] Failed to start containers. Check the logs above.
        exit /b 1
    )

    echo.
    echo [OK]    All services started.
    echo.
    docker compose ps
    echo.
    echo [INFO]  Prediction API : http://localhost:8000
    echo [INFO]  API docs       : http://localhost:8000/docs
    echo [INFO]  Onyx UI        : http://localhost:3000
    echo [INFO]  MCP endpoint   : http://localhost:8000/mcp
    goto :eof

:cmd_stop
    call :check_docker
    if errorlevel 1 exit /b 1

    echo [INFO]  Stopping containers (data is preserved)...
    docker compose stop
    echo [OK]    Containers stopped.
    goto :eof

:cmd_restart
    call :check_docker
    if errorlevel 1 exit /b 1

    call :check_env
    if errorlevel 1 exit /b 1

    echo [INFO]  Restarting all containers...
    docker compose stop
    docker compose start
    echo [OK]    All containers restarted.
    echo.
    docker compose ps
    goto :eof

:cmd_status
    call :check_docker
    if errorlevel 1 exit /b 1

    docker compose ps
    goto :eof

:cmd_logs
    call :check_docker
    if errorlevel 1 exit /b 1

    set "SERVICE=%~2"
    if "%SERVICE%"=="" (
        echo [INFO]  Streaming logs for all services ^(Ctrl+C to stop^)...
        docker compose logs -f
    ) else (
        echo [INFO]  Streaming logs for '%SERVICE%' ^(Ctrl+C to stop^)...
        docker compose logs -f "%SERVICE%"
    )
    goto :eof

:cmd_down
    call :check_docker
    if errorlevel 1 exit /b 1

    echo [WARN]  Removing containers (volumes are preserved -- data is safe)...
    docker compose down
    echo [OK]    Containers removed.
    goto :eof

:cmd_destroy
    call :check_docker
    if errorlevel 1 exit /b 1

    echo.
    echo [WARN]  This will remove ALL containers AND volumes, including the Postgres database.
    set /p "CONFIRM=         Type 'yes' to confirm: "
    if /i not "%CONFIRM%"=="yes" (
        echo [INFO]  Aborted.
        goto :eof
    )
    docker compose down -v
    echo [OK]    Containers and volumes removed.
    goto :eof

:cmd_help
    findstr /b "::" "%~f0" | findstr /v "^::$" | findstr /v "@echo off" | findstr /v "^:: ──" | ^
        for /f "delims=: tokens=2*" %%a in ('findstr /b "::" "%~f0"') do echo %%a %%b
    :: Fallback: just print the header comments
    echo.
    echo Usage: scripts\containers.bat [COMMAND]
    echo.
    echo Commands:
    echo   start            Create containers if they do not exist, then start them
    echo   stop             Stop all running containers (data is preserved)
    echo   restart          Stop then start all containers
    echo   status           Show the current state of every container
    echo   logs [service]   Stream logs (all services, or one specific service)
    echo   down             Stop and remove containers (volumes are preserved)
    echo   destroy          Stop and remove containers AND all volumes
    echo   help             Print this help message
    goto :eof

endlocal
