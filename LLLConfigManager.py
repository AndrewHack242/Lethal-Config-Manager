import copy
import sys
from pathlib import Path
import argparse

from DungeonProbFiller import translate_and_fill_all_moons
from InformationProviders import print_config_information
from MergeConfig import merge_config
from ParseLLLConfig import parse_cfg
from SplitConfig import split_cfg
from datetime import datetime
import os
from configupdater import ConfigUpdater

backup_path = Path('backups')
component_path = Path('component_configs')


def parse_args():
    parser = argparse.ArgumentParser(description='Helper for LLL config management')
    parser.add_argument('-f', '--cfg-path', help='Path to the LLL config', type=Path, required=True)
    return parser.parse_args()


# split the config into its sections in different files
# wait for input to continue, allow edits to the components
# re-combine the components and save in the original location and in the backup folder
def make_backup_dir() -> Path:
    today = datetime.now()
    if not backup_path.exists():
        os.mkdir(backup_path)

    dir_path = backup_path.joinpath(today.strftime('%Y%m%d-%H%M%S'))

    os.mkdir(dir_path)

    return dir_path


def save_config_backup(config, filename, backup_dir):
    with open(backup_dir.joinpath(filename), 'w') as configfile:
        config.write(configfile)


def overwrite_main_config(config, cfg_path: Path):
    with open(cfg_path, 'w') as configfile:
        config.write(configfile)


def main(cfg_path: Path) -> int:
    config = parse_cfg(cfg_path)
    backup_dir = make_backup_dir()
    save_config_backup(config, 'LethalLevelLoader_original_backup.cfg', backup_dir)
    translate_and_fill_all_moons(config)
    split_cfg(config, component_path)

    input_str = ''
    # y to continue, else inform again
    while input_str != 'y':
        print_config_information(component_path)
        input_str = input("\nEnter y to confirm changes, otherwise another information stream will be printed.\n> ")

    new_config = merge_config(component_path)
    save_config_backup(new_config, 'LethalLevelLoader_new.cfg', backup_dir)
    overwrite_main_config(new_config, cfg_path)

    return 0


if __name__ == '__main__':
    args = parse_args()
    sys.exit(main(args.cfg_path))
