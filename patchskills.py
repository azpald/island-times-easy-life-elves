a = []

##################################################################
# a.append(["phantom-figurine", "thump-water", "aim", "combo-turbo"])
# a.append(["gold-golem", "stone-pointing", "toughness-breaking", "suppress-earth"])
# a.append(["statue", "rockfall", "abnormal-resistance", "blade-armor"])
# a.append(["fire-statue", "fire-rain", "ignite", "light-up"])
# a.append(["water-element", "ice-attack", "ice-armor", "ice-freezing"])
# a.append(["moonlight-flamen", "moonlight-spreading", "position", "moonlight-piercing"])
# a.append(["half-goat", "ice-explosion", "ice-burst", "wisdom"])
# a.append(["mucus", "bubble-attack", "sacrifice", ""])
# a.append(["fire-spider", "combo", "convert-block", "crit-combo"])
# a.append(["fire-beast", "fireball", "aim", "ignite"])
# a.append(["demon-lord", "fatal-blow", "strong", "bloodshed"])
# a.append(["fire-spirit", "guarding", "cheer-up", "courage"])
# a.append(["guard-a", "charged-blow", "courage", ""])
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