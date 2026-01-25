import subprocess
import sys
from pytictoc import TicToc

t = TicToc()
t.tic()
subprocess.run([sys.executable, "drivers.py"]) 
subprocess.run([sys.executable, "teams.py"])
t.toc()