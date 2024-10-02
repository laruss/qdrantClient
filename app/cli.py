import subprocess

from app.errors import ApplicationError


def run_cli_command(command: str):
    """
    Run command in the terminal.

    Parameters:
        - command: str - command to run

    Returns:
        - str - output of the command
    """
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, error = process.communicate()
    if error:
        raise ApplicationError(str(error))

    return output
