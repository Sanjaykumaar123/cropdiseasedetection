@echo off
cd /d "%~dp0"
echo Starting Plant Disease Detection App...

echo Launching Backend...
start "Backend Server" cmd /k "cd backend && ..\.venv\Scripts\python app.py || echo BACKEND FAILED & pause"

echo Launching Frontend...
start "Frontend Client" cmd /k "cd frontend && npm run dev || echo FRONTEND FAILED & pause"

echo.
echo Application starting...
echo Frontend will be at: http://localhost:5173
echo Backend will be at: http://localhost:5000
echo.
echo If windows close immediately, there was an error.
pause
