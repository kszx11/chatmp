def read_config_settings(filename="config.cfg"):
    """
    Reads a config file with simple key=value lines and returns a dict of settings.
    Lines starting with '#' or empty lines are ignored.
    Whitespace around keys and values is stripped.
    """
    settings = {}
    try:
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue  # skip blank lines and comments
                if '=' not in line:
                    continue
                key, value = line.split('=', 1)
                key = key.strip()
                value = value.strip()
                settings[key] = value
    except Exception as e:
        print("Error reading config file:", e)
    return settings
