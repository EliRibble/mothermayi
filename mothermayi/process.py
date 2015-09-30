import logging
import subprocess

LOGGER = logging.getLogger(__name__)

def execute(command):
    LOGGER.debug("Executing %s", ' '.join(command))
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate(input=None)
    if proc.returncode != 0:
        raise subprocess.CalledProcessError(proc.returncode, command, "Failed to execute comand")
    LOGGER.debug("stdout %s", stdout)
    LOGGER.debug("stderr %s", stderr)
    return stdout, stderr

