import subprocess


def execute(command):
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    output = output.decode('utf-8') if output is not None else None
    error = error.decode('utf-8') if error is not None else None
    return output, error
