import json
from pprint import pprint 

INFECTED_INDEX = 8

def get_profile_info(profile_data, id):
    # find entry in profile data
    # char id > story text audio > first > stories > story text > codename etc.
    # ['[Code Name] ', '[Gender] ', '[Combat Experience] ', '[Place of Birth] ', '[Date of Birth] ', '[Race] ', '[Height] '
    return profile_data[id]["storyTextAudio"][0]["stories"][0]["storyText"].split('\n')

def get_infected_status(profile_info, name):
    infected_msg = ' '.join(profile_info[8:]).strip().lower()

    if infected_msg == '':
        infected_msg = ' '.join(profile_info[7:]).strip().lower()

    if "no infection" in infected_msg or "uninfected" in infected_msg or "non-infected" in infected_msg:
        infected = "No"
    elif "infection confirmed" in infected_msg or "confirmed infected" in infected_msg:
        infected = "Yes"
    else:
        # Outliers
        # Weird wording for first few
        if name == "Fang" or name == "Ptilopsis" or name == "Schwarz" or name == "Specter":
            infected = "Yes"
        # Ch'en being infected is spoilers so its unknown in her entry
        elif name == "Nian" or name == "Ch'en":
            infected = "Undisclosed"
        else: # Robots
            infected = "N/A"

    return infected

def get_group(info):
    group = "None" if info["groupId"] == None else info["groupId"]
    team = "Ægir" if info["teamId"] == "egir" else ("None" if info["teamId"] == None else info["teamId"])

    if team == "Ægir":
        print(info["name"])

    # if group then no team. If team then no group.
    if group != "None":
        group = group
    elif team != "None":
        group = team
    else:
        return ''

    group = group.strip()

    # Format
    if group == "rhodes":
        group = "Rhodes Island"
    elif group == "student":
        group = "Students of Ursus"
    elif group == "lee":
        group = "Lee's Detective Agency"
    elif group == "penguin":
        group = "Penguin Logistics"    
    elif group == "rainbow":
        group = "Rainbow 6" 
    elif group == "lgd":
        group = "LDG"
    elif group == "abyssal":
        group = "Abyssal Hunter"
    elif group == "rhine":
        group = "Rhine Lab"
    elif group == "rim":
        group = "Rim Billiton"
    elif group == "elite":
        group = "Elite Operators"
    elif group == "action4":
        group = "Action 4"
    elif "reserve" in group:
        group = "Reserve " + group[-1]
    else:
        group = group.capitalize()

    return group

def get_class(info):
    _class = info["profession"].lower()
    if _class == "pioneer":
        _class = "Vanguard"
    elif _class == "tank":
        _class = "Defender"
    elif _class == "warrior":
        _class = "Guard"
    elif _class == "special":
        _class = "Specialist"
    elif _class == "support":
        _class = "Supporter"
    else:
        _class = _class.lower().capitalize()

    return _class

def main():
    ignored = []
    allegiance_list = []
    with open('./operator_db/character_table.json', 'r', encoding="utf-8") as f:
        char_data = json.load(f)

        with open('./operator_db/profile_table.json', 'r', encoding="utf-8") as ff:
            profile_data = json.load(ff)["handbookDict"]

    operators = {}

    for id, info in char_data.items():
        name = info["name"]

        if not id.startswith('char'):
            continue
        
        try:
            profile_info = get_profile_info(profile_data, id)
        except:
            ignored.append(name)
            continue

        name = info["name"]
        infected = get_infected_status(profile_info, name)
        gender = profile_info[1].split(']')[1].strip()
        race = profile_info[5].split(']')[1].strip()
        if "unknown" in race.lower() or "undisclosed" in race.lower():
            race = "Unknown/Undisclosed"
        group = get_group(info)
        if group not in allegiance_list: allegiance_list.append(group)

        nation = "Ægir" if info["nationId"] == "egir" else ("None" if info["nationId"] == None else info["nationId"])
        nation = nation.capitalize()
        if nation not in allegiance_list: allegiance_list.append(nation)

        position = info["position"]

        profession = get_class(info)
        archetype = info["subProfessionId"].capitalize()
        rarity = info["rarity"] + 1
        e0_cost = info["phases"][0]["attributesKeyFrames"][0]["data"]["cost"]
        e2_cost = info["phases"][-1]["attributesKeyFrames"][0]["data"]["cost"]

        operators[name] = {
            "charId": id,
            "gender": gender,
            "race": race,
            "group": group,
            "nation": nation,
            "position": position,
            "profession": profession,
            "archetype": archetype,
            "rarity": rarity,
            "cost": (e0_cost, e2_cost),
            "infected": infected,
        }

    operators = dict(sorted(operators.items(), key=lambda item: item))

    # pprint(operators)
    # as of 19/11/2023, Mulsyse/Lone Trail isn't added to the Aceship Github
    # 277 ops added
    # 290 ops total
    # Missing 8 operators + 5 Reserve operators which makes up the difference
    # Shalem has 2 entries
    print("Ignored operators: " + str(len(ignored)))
    pprint(ignored)
    pprint(allegiance_list)
    print(len(operators))
    with open('./operator_db/operator_db.json', 'w', encoding='utf-8') as f:
        json.dump(operators, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()