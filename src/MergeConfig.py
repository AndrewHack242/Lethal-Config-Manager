import copy
from configupdater import ConfigUpdater

from .DungeonProbFiller import translate_and_fill_all_moons
from .ParseLLLConfig import parse_cfg


def merge_config(component_path):
    merged_config = ConfigUpdater()
    for path in component_path.glob('*.ini'):
        component_config = parse_cfg(path)
        for section in component_config.sections():
            merged_config.add_section(section)
            merged_config[section] = copy.deepcopy(component_config[section])
    translate_and_fill_all_moons(merged_config)
    return merged_config
