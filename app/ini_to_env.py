import configparser

def ini_to_env(ini_file, env_file):
    config = configparser.ConfigParser()
    config.read(ini_file)

    with open(env_file, 'w') as f:
        for section in config.sections():
            if section == 'users':
                users = []
                for key, value in config[section].items():
                    username, password = value.split(',')
                    users.append(f"{username.strip()},{password.strip()}")
                f.write(f"USERS='{';'.join(users)}'\n")
            else:
                for key, value in config[section].items():
                    f.write(f"{key.upper()}='{value.strip()}'\n")


if __name__ == "__main__":
    ini_to_env('.ini', '.env')