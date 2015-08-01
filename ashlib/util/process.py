import os
import sys
import re
import subprocess
import signal

def getServerPIDs(port):
    command = "lsof -i TCP:%s" % port
    try:
        output = subprocess.check_output(command.split())
    except subprocess.CalledProcessError as e:
        return []
    else:
        pids = []
        for line in output.split("\n")[1:]:
            matches = re.findall("[^ ]+ +(\d+)", line)
            if len(matches) > 0:
                pids.append(int(matches[0]))
        return pids
