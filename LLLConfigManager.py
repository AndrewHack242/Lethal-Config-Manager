import sys
from pathlib import Path
import argparse

from src.DungeonProbFiller import translate_and_fill_all_moons
from src.FileIO import make_backup_dir, save_config_backup, overwrite_main_config
from src.InformationProviders import print_config_information
from src.MergeConfig import merge_config
from src.ParseLLLConfig import parse_cfg
from src.SplitConfig import split_cfg
from datetime import datetime
import os

backup_path = Path('backups')
component_path = Path('component_configs')


def parse_args():
    parser = argparse.ArgumentParser(description='Helper for LLL config management')
    parser.add_argument('-f', '--cfg-path', help='Path to the LLL config', type=Path, required=True)
    return parser.parse_args()


def main(cfg_path: Path) -> int:
    config = parse_cfg(cfg_path)
    backup_dir = make_backup_dir(backup_path)
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
