from pathlib import Path
from configupdater import ConfigUpdater
import copy
import os

from .NameGetters import get_filename_for_section


def write_to_file(config, section_to_keep, component_path):
    if not component_path.exists():
        os.mkdir(component_path)
    hit = False
    for section in config.sections():
        if section != section_to_keep:
            config.remove_section(section)
        else:
            hit = True
    if not hit:
        raise ValueError(f'failed on {section_to_keep}')

    name = get_filename_for_section(section_to_keep)

    with open(component_path.joinpath(f'{name}.ini'), 'w') as configfile:
        config.write(configfile)


def delete_files(component_path: Path):
    for path in component_path.iterdir():
        Path.unlink(path)


def split_cfg(config, component_path):
    delete_files(component_path)
    for section in config.sections():
        config_copy = copy.deepcopy(config)
        write_to_file(config_copy, section, component_path)
