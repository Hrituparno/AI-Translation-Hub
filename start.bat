@echo off
REM Startup script for IndiaTranslate (Windows)
REM Starts both API and UI servers

echo Starting IndiaTranslate...
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Virtual environment not found!
    echo Please run: python -m venv venv
    echo Then: venv\Scripts\activate
    echo Then: pip install -r requirements.txt
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate

REM Start API server
echo Starting API server on port 8000...
start "IndiaTranslate API" cmd /k uvicorn api.main:app --host 0.0.0.0 --port 8000

REM Wait for API to start
timeout /t 3 /nobreak >nul

REM Start Streamlit UI
echo Starting UI on port 8501...
start "IndiaTranslate UI" cmd /k streamlit run ui/app.py --server.port 8501

echo.
echo IndiaTranslate is running!
echo.
echo API: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo UI: http://localhost:8501
echo.
echo Close the command windows to stop the servers
