import configparser
import argparse

def get_config():
    DEFAULT_INI_FILE = "digiham-stats.ini"
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--config", default = DEFAULT_INI_FILE)
    args, _ = parser.parse_known_args()
    config_filepath = args.config
    print(config_filepath, DEFAULT_INI_FILE, config_filepath != DEFAULT_INI_FILE)
    if not os.path.exists(config_filepath):
        if config_filepath != DEFAULT_INI_FILE:
            print(f"Config file not found: {config_filepath}")
            sys.exit(1)

    print(f"Reading options from {config_filepath}")
    config = configparser.ConfigParser()
    config.read(config_filepath)
    return config

def get_config_option(config, section, option, default):
    if (config.has_option(section, option)):
        return config.get(section, option)
    else:
        return default




