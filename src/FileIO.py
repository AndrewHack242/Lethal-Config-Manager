# split the config into its sections in different files
# wait for input to continue, allow edits to the components
# re-combine the components and save in the original location and in the backup folder
from os import mkdir
from datetime import datetime
from pathlib import Path


def make_backup_dir(backup_path: Path) -> Path:
    today = datetime.now()
    if not backup_path.exists():
        mkdir(backup_path)
    dir_path = backup_path.joinpath(today.strftime('%Y%m%d-%H%M%S'))
    mkdir(dir_path)
    return dir_path


def save_config_backup(config, filename, backup_dir):
    with open(backup_dir.joinpath(filename), 'w') as configfile:
        config.write(configfile)


def overwrite_main_config(config, cfg_path: Path):
    with open(cfg_path, 'w') as configfile:
        config.write(configfile)
