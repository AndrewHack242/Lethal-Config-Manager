override_map = {'57 Asteroid13': 'Asteroid', '25 FissionC': 'Fission', '127 EveM': 'Eve'}


def get_clean_section_name(section_name):
    if ':' in section_name:
        start_index = str(section_name).index(':') + 3
        clean_name = section_name[start_index:]
        if clean_name in override_map:
            clean_name = override_map[clean_name]
        return clean_name
    else:
        return section_name


def get_filename_for_section(section_name):
    filename = ""
    if ' Level' in section_name:
        filename = "Moon - "
    elif ' Dungeon' in section_name:
        filename = "Dungeon - "
    filename += get_clean_section_name(section_name)
    return filename


def get_moons(config):
    moons = set[str]()
    for section in config.sections():
        if ' Level' in section:
            moons.add(get_clean_section_name(section))
    return moons


def get_dungeons(config):
    moons = []
    for section in config.sections():
        if ' Dungeon' in section:
            moons.append(section)
    return moons
