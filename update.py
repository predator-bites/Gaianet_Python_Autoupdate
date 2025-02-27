import paramiko

failed = []
successful = []
amount_of_server = int(input('Enter amount of nodes on each server: '))

def load_servers(file_path):
    servers = []
    with open(file_path, "r") as file:
        for line in file:
            parts = line.strip().split(":")
            if len(parts) == 2:
                servers.append((parts[0], parts[1]))
                print(parts)
    return servers

def execute_commands(host, username, password, commands,success_string):
    try:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(hostname=host, port=22, username=username, password=password)
        except:
            failed.append(f'{host}: failed to connect')
        i=0    

        for command in commands:
            print(f"Executing: {command} on {host}")
            stdin, stdout, stderr = client.exec_command(command)

            output = stdout.read().decode().strip()
            error = stderr.read().decode().strip()

            print(f"=== OUTPUT ({host}) ===")
            print(output if output else "No output")

            print(f"=== ERROR ({host}) ===")
            print(error if error else "No errors")
            if command==commands[-1]:
                last_line = output.splitlines()[-1] if output else ""
                if success_string == last_line:
                    successful.append(host)
                else:
                    failed.append(host)

        client.close()
    except Exception as e:
        print(f"Error on {host}: {e}")


if __name__ == "__main__":
    file_path = "servers.txt"  # Файл с IP:пароль
    if amount_of_server==1:
        commands = [
            '/root/gaianet/bin/gaianet stop',
            'curl -sSfL "https://github.com/GaiaNet-AI/gaianet-node/releases/latest/download/install.sh" | bash -s -- --upgrade',  # Full paths!
            '/root/gaianet/bin/gaianet init',
            '/root/gaianet/bin/gaianet start'
    ]

    elif amount_of_server==2:
        commands = [
            '/root/gaianet/bin/gaianet stop',
            '/root/gaianet-2/bin/gaianet stop --base $HOME/gaianet-2',
            'curl -sSfL "https://github.com/GaiaNet-AI/gaianet-node/releases/latest/download/install.sh" | bash -s -- --upgrade',  # Full paths!
            '/root/gaianet/bin/gaianet init',
            '/root/gaianet/bin/gaianet start',
            'curl -sSfL "https://github.com/GaiaNet-AI/gaianet-node/releases/latest/download/install.sh" | bash -s -- --upgrade --base $HOME/gaianet-2',
            '/root/gaianet-2/bin/gaianet init',
            '/root/gaianet-2/bin/gaianet start --base $HOME/gaianet-2'
    ]

    
    servers = load_servers(file_path)
    for server_ip, password in servers:
        execute_commands(server_ip, "root", password, commands, ">>> You can close this terminal window safely now <<<")



with open("successful.txt", "w") as file:  # "w" for write mode (overwrites if file exists)
    for item in successful:
        file.write(item + "\n")

with open("failed.txt", "w") as file:  # "w" for write mode (overwrites if file exists)
    for item in failed:
        file.write(item + "\n")


