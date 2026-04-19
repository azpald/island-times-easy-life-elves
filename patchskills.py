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
# a.append(["deer-spirit", "unusual-rain", "self-healing", "resistance"])
# a.append(["elf-mage", "recovery", "position", "demon-hunting"])
# a.append(["flower-elf", "purification-therapy", "group-dance", "slow-dance"])
# a.append(["light", "resonance", "shine", "last-words-wind"])
# a.append(["sword-ghost", "phantom-attack", "cold", "storm-attack"])
# a.append(["dark-knight", "darkness-falls", "excessive-damage", "buff"])
# a.append(["ghost", "ghost-strike", "stealing", "dodging"])
# a.append(["ghost-mage", "bad-luck", "aim", "share-suffering"])
# a.append(["skeleton-mage", "double-guards", "feed-back", "power-in-numbers"])
# a.append(["sickle-ghost", "reaper", "kill-to-protect", "last-gasp"])
# a.append(["zombie", "bite-poison", "poisonous-blow", "dead-draw"])
# a.append(["skeleton-archer", "continuous-fire", "crit-combo", ""])
# a.append(["little-skeleton", "thump", "reincarnation", ""])
# a.append(["claw-beast", "combo", "cheer-up", "convert-critical"])
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