from DungeonProbFiller import get_moons, get_dungeons, split_key_value, match
from MergeConfig import merge_config
from SplitConfig import get_clean_section_name, split_cfg


# inform

# -> empty fields for desired fields
def check_for_empty_fields(config, field_to_check):
    print()
    for section in config.sections():
        if field_to_check in str(config[section]):
            if 'Default Values Were Empty' in str(config[section][field_to_check].value.strip()):
                print(f'{get_clean_section_name(section)}: {str(config[section][field_to_check]).strip()}')


def check_for_all_zero(config, field_to_check):
    print()
    for section in config.sections():
        if field_to_check in str(config[section]):
            non_zero = False
            probs = config[section]['Dungeon Injection Settings - Manual Level Names List'].value.split(",")
            for kv in probs:
                key, value = split_key_value(kv, section)
                if key is None or value is None:
                    continue
                if value == '0':
                    continue
                if value != '0':
                    non_zero = True
            if not non_zero:
                print(f'{get_clean_section_name(section)}: Is set to 0 for all key/value pairs')


# -> a print-out if moon cost is different from the default
def check_non_default_route_prices(config):
    print()
    field_to_check = 'General Settings - Planet Route Price'
    for section in config.sections():
        if field_to_check in str(config[section]):
            if 'Default value: ' in str(config[section][field_to_check].previous_block):
                if ':' in str(config[section][field_to_check].previous_block):
                    start_index = str(config[section][field_to_check].previous_block).rindex(':') + 2
                    default = str(config[section][field_to_check].previous_block)[start_index:]
                    if default.strip() != config[section][field_to_check].value.strip():
                        print(
                            f'{get_clean_section_name(section)}: Default of {default.strip()} '
                            f'does not match {config[section][field_to_check].value.strip()}')
                else:
                    raise ValueError(': but also no :?')
            else:
                print(f'{get_clean_section_name(section)}: Default Comment not found')
    pass


def check_enable_content_config_true(config):
    print()
    field_to_check = 'Enable Content Configuration'
    for section in config.sections():
        if '- LethalLevelLoader Settings -' in str(section):
            continue
        if field_to_check not in str(config[section]):
            print(f'{get_clean_section_name(section)}: {field_to_check} not found')
            continue
        if config[section][field_to_check].value.strip().lower() != 'true':
            print(
                f'{get_clean_section_name(section)}: {field_to_check} was not true, value: '
                f'{config[section][field_to_check].value.strip()}')
            continue


def print_moon_dungeon_probs(config, moon):
    print_list = []
    dungeons = get_dungeons(config)
    for dungeon in dungeons:
        probs = config[dungeon]['Dungeon Injection Settings - Manual Level Names List'].value.split(",")
        for kv in probs:
            key, value = split_key_value(kv, dungeon)
            if key is None or value is None:
                continue
            if value == '0':
                continue
            if match(key, moon):
                print_list.append(f'{get_clean_section_name(dungeon)}:{value}')
                break
    print(f'{moon} = {",".join(print_list)}')


# -> a printout of each moon's non-zero probabilities | two-way substring match case-insensitive
def print_all_moon_dungeon_probs(config):
    print()
    moons = list(get_moons(config))
    moons.sort()
    for moon in moons:
        print_moon_dungeon_probs(config, moon)


def print_config_information(component_path):
    new_config = merge_config(component_path)
    split_cfg(new_config, component_path)
    print()
    print()
    check_enable_content_config_true(new_config)
    check_for_empty_fields(new_config, 'Dungeon Injection Settings - Manual Level Names List')
    check_for_all_zero(new_config, 'Dungeon Injection Settings - Manual Level Names List')
    check_non_default_route_prices(new_config)
    print_all_moon_dungeon_probs(new_config)
