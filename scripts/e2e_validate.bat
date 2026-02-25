@echo off
REM e2e_validate.bat — End-to-end validation against the live Docker stack (Windows)
REM
REM Usage: scripts\e2e_validate.bat [BASE_URL]
REM
REM Requires: curl (included in Windows 10+)

setlocal EnableDelayedExpansion

set "BASE_URL=%~1"
if "%BASE_URL%"=="" set "BASE_URL=http://localhost:8000"

set PASSED=0
set FAILED=0
set TOTAL=0

echo.
echo == E2E Validation — %BASE_URL% ==
echo.

REM ── Health Check ────────────────────────────────────────────────────────

echo -- Health Check --

curl -s -o NUL -w "%%{http_code}" "%BASE_URL%/health" > "%TEMP%\e2e_code.txt" 2>NUL
set /p HTTP_CODE=<"%TEMP%\e2e_code.txt"
if "%HTTP_CODE%"=="200" (
    echo   PASS  GET /health returns 200
    set /a PASSED+=1
) else (
    echo   FAIL  GET /health returns 200 ^(got %HTTP_CODE%^)
    set /a FAILED+=1
)
set /a TOTAL+=1

REM ── Valid Prediction ────────────────────────────────────────────────────

echo.
echo -- Valid Prediction --

curl -s -o "%TEMP%\e2e_predict.json" -w "%%{http_code}" -X POST "%BASE_URL%/predict" -H "Content-Type: application/json" -d "{\"product_id\":\"PROD-001\",\"store_id\":\"STORE-A\",\"start_date\":\"2026-03-02\",\"end_date\":\"2026-03-04\"}" > "%TEMP%\e2e_code.txt" 2>NUL
set /p PREDICT_CODE=<"%TEMP%\e2e_code.txt"
if "%PREDICT_CODE%"=="200" (
    echo   PASS  POST /predict returns 200 for valid payload
    set /a PASSED+=1
) else (
    echo   FAIL  POST /predict returns 200 ^(got %PREDICT_CODE%^)
    set /a FAILED+=1
)
set /a TOTAL+=1

findstr /C:"predictions" "%TEMP%\e2e_predict.json" >NUL 2>NUL
if !ERRORLEVEL!==0 (
    echo   PASS  Response contains 'predictions' array
    set /a PASSED+=1
) else (
    echo   FAIL  Response contains 'predictions' array
    set /a FAILED+=1
)
set /a TOTAL+=1

REM ── MCP Endpoint ────────────────────────────────────────────────────────

echo.
echo -- MCP Endpoint --

curl -s -o NUL -w "%%{http_code}" "%BASE_URL%/mcp" > "%TEMP%\e2e_code.txt" 2>NUL
set /p MCP_CODE=<"%TEMP%\e2e_code.txt"
if not "%MCP_CODE%"=="000" (
    echo   PASS  MCP endpoint responds ^(HTTP %MCP_CODE%^)
    set /a PASSED+=1
) else (
    echo   FAIL  MCP endpoint responds ^(connection refused^)
    set /a FAILED+=1
)
set /a TOTAL+=1

REM ── OpenAPI Schema ──────────────────────────────────────────────────────

echo.
echo -- OpenAPI Schema --

curl -s "%BASE_URL%/openapi.json" > "%TEMP%\e2e_schema.json" 2>NUL
findstr /C:"predict_stock" "%TEMP%\e2e_schema.json" >NUL 2>NUL
if !ERRORLEVEL!==0 (
    echo   PASS  OpenAPI schema contains 'predict_stock'
    set /a PASSED+=1
) else (
    echo   FAIL  OpenAPI schema contains 'predict_stock'
    set /a FAILED+=1
)
set /a TOTAL+=1

REM ── Error Handling — Missing Field ──────────────────────────────────────

echo.
echo -- Error Handling --

curl -s -o NUL -w "%%{http_code}" -X POST "%BASE_URL%/predict" -H "Content-Type: application/json" -d "{\"store_id\":\"STORE-A\",\"start_date\":\"2026-03-02\",\"end_date\":\"2026-03-04\"}" > "%TEMP%\e2e_code.txt" 2>NUL
set /p ERR_CODE=<"%TEMP%\e2e_code.txt"
if "%ERR_CODE%"=="422" (
    echo   PASS  Missing product_id returns 422
    set /a PASSED+=1
) else (
    echo   FAIL  Missing product_id returns 422 ^(got %ERR_CODE%^)
    set /a FAILED+=1
)
set /a TOTAL+=1

REM ── CORS Headers ────────────────────────────────────────────────────────

echo.
echo -- CORS Headers --

curl -s -I -X OPTIONS "%BASE_URL%/health" -H "Origin: http://localhost:3000" -H "Access-Control-Request-Method: GET" > "%TEMP%\e2e_cors.txt" 2>NUL
findstr /I /C:"access-control-allow-origin" "%TEMP%\e2e_cors.txt" >NUL 2>NUL
if !ERRORLEVEL!==0 (
    echo   PASS  CORS access-control-allow-origin header present
    set /a PASSED+=1
) else (
    echo   FAIL  CORS access-control-allow-origin header present
    set /a FAILED+=1
)
set /a TOTAL+=1

REM ── Summary ─────────────────────────────────────────────────────────────

echo.
echo ======================================
echo   Results: %PASSED% passed, %FAILED% failed / %TOTAL% total
echo ======================================
echo.

REM Clean up temp files
del "%TEMP%\e2e_code.txt" 2>NUL
del "%TEMP%\e2e_predict.json" 2>NUL
del "%TEMP%\e2e_schema.json" 2>NUL
del "%TEMP%\e2e_cors.txt" 2>NUL

if %FAILED% GTR 0 (
    echo Some checks failed. See details above.
    exit /b 1
) else (
    echo All checks passed!
    exit /b 0
)
