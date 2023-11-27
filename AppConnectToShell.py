"""
App connects to shell via ssh (e.g. kali linux)

"""


import paramiko
import sys
import threading
import queue

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

    def run_shell(self):
        thread = threading.Thread(target=self.read_input, daemon=True)
        thread.start()

        try:
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

def SSH_interactive_shell(hostname, port, username, password):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname, port, username=username, password=password)

        channel = client.invoke_shell()
        ssh_shell = SSHShell(client, channel)
        ssh_shell.run_shell()

    except paramiko.AuthenticationException:
        print("Błąd uwierzytelniania. Sprawdź nazwę użytkownika i hasło.")
    except paramiko.SSHException as e:
        print(f"Błąd połączenia SSH: {str(e)}")
    except Exception as e:
        print(f"Inny błąd: {str(e)}")
    finally:
        client.close()

if __name__ == "__main__":
    try:
        ip = "192.168.1.101"
        username = "kali"
        password = "kali"

        SSH_interactive_shell(ip, 22, username, password)
    except Exception as e:
        print(f"Wystąpił błąd: {str(e)}")
