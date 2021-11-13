import subprocess


def execute(*command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    if stderr is not None and len(stderr) != 0:
        raise RuntimeError(stderr.decode('utf-8'))
    return stdout.decode('utf-8')
