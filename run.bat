@echo on
cd %~dp0
call ".\venv\Scripts\activate.bat"
echo "Virtual Environment Activated (venv)"

color 0A
echo Running Python scripts...
py __main__.py
echo Python scripts executed.

cmd /k
