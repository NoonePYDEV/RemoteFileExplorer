@echo off
echo ==================================================================
echo        /!\                  ATTENTION             /!\
echo ==================================================================
echo.
echo N'utilise Build.bat uniquement pour compiler ton client.py (situé dans ./Client/client.py) une fois
echo qu'il est bien configure.
echo.
echo Si tu ne sais pas comment utiliser, envoie un DM a @main.enc sur Discord.
echo.
echo Si tu as deja configure, alors tu n'as qu'a appuyer sur une touche
echo pour lancer la compilation du client vers un executable.
echo.
echo.

pause >nul

echo [+] Lancement de la compilation...
echo.
pyinstaller --onefile --icon="..\Src\Assets\executable.png" --windowed --noconfirm --specpath=".\tmp" --workpath=".\tmp" --distpath=".\Built" ./Client/client.py
echo.
echo.
echo.
echo [+] Compilation terminée ! Le fichier compilé est situé dans ./Built/client.exe
echo.

pause
