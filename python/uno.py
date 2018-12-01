import sys
import os.path
import system
import dirutils
import tempfile
from itertools import takewhile
import shutil

temp_path = os.path.abspath(sys.argv[1])
directory = os.path.abspath(sys.argv[2])
csv       = os.path.abspath(sys.argv[3])
exe       = sys.argv[4]
if (len(sys.argv) > 5):
    opts      = sys.argv[5]
else:
    opts = ""

# create temporary dir to run the analyzer
tmpdir_path = os.path.join("/home","itc","tmp", "uno-" + next(tempfile._get_candidate_names()))
shutil.copytree(directory, tmpdir_path)
    
print("======Running uno=======")
# print("Working dir:", directory)
# print("CSV file:", csv)
# print("Excutable:", exe)
# print("Executable options:", opts)
print("[CWD]:", tmpdir_path)
print("[CSV]:", csv)
print("[EXE]:", exe)
print("[EXE OPTIONS]:", opts)

if os.path.exists(csv):
    os.remove(csv)
sys.stdout = open(csv, "w")
print("File, Line, Error")
sys.stdout = sys.__stdout__

source_files = dirutils.list_files(tmpdir_path, '.c') + dirutils.list_files(tmpdir_path, '.cpp')
for source_file in source_files:
    uno = exe + " " + opts + " " + source_file
    (output, err, exit, time) = system.system_call(uno, tmpdir_path)
    lines = output.splitlines()
    sys.stdout = open(csv, "a")
    for line in lines:
        a = line.decode("utf-8").strip().split(":")
        if (len(a) >= 4) and (a[0] == 'uno'):
            if len(a[2]) > 10: # hack to work around bug in printint wrong array indexing
                print(os.path.basename(a[1]), ",", ''.join(takewhile(str.isdigit, a[2].strip())), ",", a[2])
            else:
                print(os.path.basename(a[1]), ",", a[2], ",", a[3])
    sys.stdout = sys.__stdout__            

print("[CLEANUP]: removing ", tmpdir_path)
shutil.rmtree(tmpdir_path)
print("======[DONE WITH UNO]=======")

