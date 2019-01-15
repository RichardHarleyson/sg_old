import subprocess
import sys

DETACHED_PROCESS = 0x00000008
pid = subprocess.Popen([sys.executable, "C:\\Python\\sg_main.py"], creationflags=DETACHED_PROCESS).pid
