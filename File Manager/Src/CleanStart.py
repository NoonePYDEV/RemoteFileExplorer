import threading
import subprocess
import sys

def Start():
    subprocess.Popen("cmd /c cd .\\Src && python .\\server.py", creationflags=subprocess.CREATE_NO_WINDOW)

threading.Thread(target=Start, daemon=False).start()
sys.exit(0)