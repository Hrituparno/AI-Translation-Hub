@echo off
echo ========================================
echo Translation Quality Test
echo ========================================
echo.
call venv\Scripts\activate.bat
python test_translation_quality.py
echo.
echo ========================================
echo Test Complete!
echo ========================================
pause
