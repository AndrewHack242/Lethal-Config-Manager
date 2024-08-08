from pathlib import Path
from configupdater import ConfigUpdater


def parse_cfg(cfg_path: Path) -> ConfigUpdater:
    config = ConfigUpdater()
    with open(cfg_path, 'r') as f:
        config.read_file(f)
    return config
