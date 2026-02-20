@echo off
title Tahiti Business Group - Serveur Django
color 0A
cls

echo.
echo  ============================================
echo   TAHITI BUSINESS GROUPE - Serveur Django
echo  ============================================
echo.
echo  Demarrage du serveur...
echo.
echo  Site disponible sur :
echo  http://127.0.0.1:8000/
echo.
echo  Admin Django :
echo  http://127.0.0.1:8000/admin/
echo.
echo  Identifiants admin :
echo  Email    : mathyscocogames@gmail.com
echo  Mot passe: CocoGames25@
echo.
echo  [Appuie sur CTRL+C pour arreter le serveur]
echo  ============================================
echo.

cd /d "%~dp0"
python manage.py runserver

pause