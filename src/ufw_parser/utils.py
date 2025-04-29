import os
import fnmatch
import logging
import paramiko


logger = logging.getLogger("ufw_parser_log")


def find_files(directory, pattern):
    """Search recursively for files matching a given pattern.

    Args:
        directory (str): The root directory from where the search will begin.
        pattern (str): The pattern to match the filenames against.

    Returns:
        list of str: A list containing the full paths to the files that match the pattern.
    """
    matches = []
    for root, dirs, files in os.walk(directory):
        for filename in fnmatch.filter(files, pattern):
            matches.append(os.path.join(root, filename))
    logger.debug(f"Files found: {matches}")
    return matches


def read_remote_files_sudo(hostname, username, remote_path, password=None):
    # Initialize SSH client
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        # Connect to the remote server
        if password:
            ssh.connect(hostname, username=username, password=password)
        else:
            ssh.connect(hostname, username=username, look_for_keys=True, allow_agent=True)
        logger.info(f"Connected to {hostname}")

        # Prepare command to find and cat .rules files with sudo
        command = f"sudo find {remote_path} -name '*.rules' -exec cat {{}} +"
        stdin, stdout, stderr = ssh.exec_command(command)
        file_contents = stdout.read().decode('utf-8').splitlines()
        error = stderr.read().decode('utf-8')

        if error:
            raise Exception(f"Error executing command: {error}")

        # Close the SSH connection
        ssh.close()

        return file_contents

    except Exception as e:
        logger.info(f"Failed to connect or read from {hostname}: {e}")
        if 'ssh' in locals():
            ssh.close()
        return []