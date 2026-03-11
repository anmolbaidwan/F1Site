import subprocess
import sys
from pytictoc import TicToc

t = TicToc()
t.tic()
subprocess.run([sys.executable, "src/drivers.py"]) 
subprocess.run([sys.executable, "src/teams.py"])
t.toc()