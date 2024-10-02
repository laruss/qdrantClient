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
    process = subprocess.Popen(['cmd'], stdin=subprocess.PIPE)
    output, error = process.communicate(command.encode())

    if error:
        raise ApplicationError(f"Error in stderr: {error}")

    if output and "error:" in output.lower():
        raise ApplicationError(f"Error in stdout: {output}")

    return output
