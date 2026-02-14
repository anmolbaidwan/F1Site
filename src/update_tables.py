import subprocess
import sys
from pytictoc import TicToc

#basically runs drivers and teams.py, will add schedule when done
t = TicToc()
t.tic()
subprocess.run([sys.executable, "src/drivers.py"]) 
subprocess.run([sys.executable, "src/teams.py"])
t.toc()