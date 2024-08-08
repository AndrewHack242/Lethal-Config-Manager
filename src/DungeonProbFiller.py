import copy

from configupdater import ConfigUpdater

from src.NameGetters import get_moons, get_dungeons


def match(key: str, moon: str) -> bool:
    return key.lower() in moon.lower() or moon.lower() in key.lower()


def prob_entry(moon: str, prob: str):
    return f'{moon}:{prob}'


def split_key_value(kv, dungeon_section):
    if ':' not in kv:
        print(f'{kv} did not contain a \':\' in dungeon {get_clean_section_name(dungeon_section)}')
        return None, None
    split = kv.split(':')
    if len(split) != 2:
        print(f'{len(split)} != 2 for {kv} in dungeon {get_clean_section_name(dungeon_section)}')
        return None, None
    return split[0], split[1]


def populate_dungeon_section(config: ConfigUpdater, moons: set[str], dungeon_section: str):
    moons_to_find = copy.deepcopy(moons)
    key_values = config[dungeon_section]['Dungeon Injection Settings - Manual Level Names List'].value.split(',')
    new_key_values = []
    for kv in key_values:
        key, value = split_key_value(kv, dungeon_section)
        if key is None or value is None:
            continue
        moons_to_remove = []
        for moon in moons_to_find:
            if value != '0' and match(key, moon):
                new_key_values.append(prob_entry(moon, value))
                moons_to_remove.append(moon)
        for moon in moons_to_remove:
            moons_to_find.remove(moon)
    new_key_values.sort()

    moons_to_fill = []
    for leftover_moon in moons_to_find:
        moons_to_fill.append(prob_entry(leftover_moon, '0'))
    moons_to_fill.sort()
    for leftover_moon in moons_to_fill:
        new_key_values.append(leftover_moon)

    config[dungeon_section]['Dungeon Injection Settings - Manual Level Names List'].value = ",".join(new_key_values)


def translate_and_fill_all_moons(config: ConfigUpdater):
    moons = get_moons(config)
    dungeons = get_dungeons(config)
    for dungeon in dungeons:
        populate_dungeon_section(config, moons, dungeon)
