a = []

##################################################################
a.append(["phantom-figurine", "thump-water", "aim", "combo-turbo"])
a.append(["gold-golem", "stone-pointing", "toughness-breaking", "suppress-earth"])
a.append(["statue", "rockfall", "abnormal-resistance", "blade-armor"])
a.append(["fire-statue", "", "", ""])
a.append(["water-element", "", "", ""])
a.append(["moonlight-flamen", "", "", ""])
a.append(["half-goat", "", "", ""])
a.append(["mucus", "", "", ""])
a.append(["fire-spider", "", "", ""])
a.append(["fire-beast", "", "", ""])
a.append(["demon-lord", "", "", ""])
a.append(["fire-spirit", "", "", ""])
a.append(["guard-a", "", "", ""])
a.append(["deer-spirit", "", "", ""])
a.append(["elf-mage", "", "", ""])
a.append(["flower-elf", "", "", ""])
a.append(["light", "", "", ""])
a.append(["sword-ghost", "", "", ""])
a.append(["dark-knight", "", "", ""])
a.append(["ghost", "", "", ""])
a.append(["ghost-mage", "", "", ""])
a.append(["skeleton-mage", "", "", ""])
a.append(["sickle-ghost", "", "", ""])
a.append(["zombie", "", "", ""])
a.append(["skeleton-archer", "", "", ""])
a.append(["little-skeleton", "", "", ""])
a.append(["claw-beast", "", "", ""])
##################################################################

for b in a:
    mo = b[0]
    elf = json_data["elves"].get(mo, {})
    sk = b[1:]
    for s in sk:
        if s in json_data["skills"]:
            print("New skill possibly dupe: ", s)
    elf["skills"] = [c for c in sk if c]

# print(json_data["elves"])
# print(elves)