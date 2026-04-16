a = []

##################################################################
a.append(["land-of-wind", "phantom-figurine", "1, 2"])
a.append(["land-of-wind", "elf-archer", "1, 2, 7"])
a.append(["land-of-wind", "slime", "1, 2"])
a.append(["land-of-wind", "bat", "1, 2, 5, 6, 8"])
a.append(["land-of-wind", "little-skeleton", "1, 2, 3, 4, 9"])
a.append(["land-of-wind", "tree-guard", "3, 4, 8"])
a.append(["land-of-wind", "statue", "3, 4, 9"])
a.append(["land-of-wind", "skeleton-archer", "3, 4, 9"])
a.append(["land-of-wind", "goblin-assassin", "3, 4"])
a.append(["land-of-wind", "wolf-cavalry-a", "5, 6, 7"])
a.append(["land-of-wind", "orc-flamen", "5, 6"])
a.append(["land-of-wind", "duel-axe-orc", "5, 6"])
a.append(["land-of-wind", "wolf-orc", "5, 6"])
a.append(["land-of-wind", "zombie", "7"])
a.append(["land-of-wind", "wolf-cavalry-b", "7"])
a.append(["land-of-wind", "deer-spirit", "7"])
a.append(["land-of-wind", "skeleton-mage", "8"])
a.append(["land-of-wind", "cyclops", "8"])
a.append(["land-of-wind", "ghost-mage", "8"])
a.append(["land-of-wind", "succubus-oni", "9"])
a.append(["land-of-wind", "fire-statue", "9"])
a.append(["land-of-wind", "spar-giant", "10"])
a.append(["land-of-summer", "bat", "1, 2, 4"])
a.append(["land-of-summer", "statue", "1, 2"])
a.append(["land-of-summer", "slime", "1"])
a.append(["land-of-summer", "water-element", "1, 2"])
a.append(["land-of-summer", "elf-archer", "1, 7, 8"])
a.append(["land-of-summer", "wolf-cavalry-a", "2"])
a.append(["land-of-summer", "wolf-cavalry-b", "2"])
a.append(["land-of-summer", "cyclops", "3, 4"])
a.append(["land-of-summer", "claw-beast", "3"])
a.append(["land-of-summer", "fire-beast", "3"])
a.append(["land-of-summer", "fire-spirit", "3, 4"])
a.append(["land-of-summer", "fire-element", "3, 4"])
a.append(["land-of-summer", "fire-statue", "4"])
a.append(["land-of-summer", "skeleton-mage", "5, 6"])
a.append(["land-of-summer", "zombie", "5, 6"])
a.append(["land-of-summer", "skeleton-archer", "5, 6"])
a.append(["land-of-summer", "ghost-mage", "5, 6"])
a.append(["land-of-summer", "sword-ghost", "5, 6"])
a.append(["land-of-summer", "dark-knight", "5, 6"])
a.append(["land-of-summer", "flower-elf", "7, 8"])
a.append(["land-of-summer", "tree-elder", "7, 8"])
a.append(["land-of-summer", "deer-spirit", "7, 8"])
a.append(["land-of-summer", "light", "7, 8"])
a.append(["land-of-summer", "duel-axe-orc", "9"])
a.append(["land-of-summer", "dog-headed-orc", "9"])
a.append(["land-of-summer", "wolf-orc", "9"])
a.append(["land-of-summer", "tree-guard", "9"])
a.append(["land-of-summer", "orc-flamen", "9"])
a.append(["land-of-forest", "bat", "1, 2, 5"])
a.append(["land-of-forest", "goblin-assassin", "1, 2"])
a.append(["land-of-forest", "duel-axe-orc", "1, 2"])
a.append(["land-of-forest", "slime", "1"])
a.append(["land-of-forest", "cyclops", "1"])
a.append(["land-of-forest", "phantom-figurine", "2, 6"])
a.append(["land-of-forest", "wolf-cavalry-b", "2"])
a.append(["land-of-forest", "claw-beast", "3, 4"])
a.append(["land-of-forest", "succubus-oni", "3, 4"])
a.append(["land-of-forest", "fire-spirit", "3, 4"])
a.append(["land-of-forest", "fire-beast", "3, 4"])
a.append(["land-of-forest", "demon-lord", "3"])
a.append(["land-of-forest", "fire-element", "4"])
a.append(["land-of-forest", "elf-archer", "5, 7"])
a.append(["land-of-forest", "flower-elf", "5"])
a.append(["land-of-forest", "tree-guard", "5"])
a.append(["land-of-forest", "light", "5"])
a.append(["land-of-forest", "dog-headed-orc", "6"])
a.append(["land-of-forest", "wolf-orc", "6"])
a.append(["land-of-forest", "ghost", "6, 8, 9"])
a.append(["land-of-forest", "moonlight-flamen", "6"])
a.append(["land-of-forest", "skeleton-archer", "7"])
a.append(["land-of-forest", "statue", "7"])
a.append(["land-of-forest", "fire-statue", "7"])
a.append(["land-of-forest", "little-skeleton", "7"])
a.append(["land-of-forest", "ghost-mage", "8, 9"])
a.append(["land-of-forest", "skeleton-mage", "8, 9"])
a.append(["land-of-forest", "butcher-zombie", "8, 9"])
a.append(["land-of-forest", "zombie", "8, 9"])
##################################################################

for b in a:
    slug = b[1]
    land = b[0]
    floor = b[2]
    note = f'Spawns on Floor {floor}'
    if land == "land-of-chaos":
        note = f'May appear on Floor {floor}'
    elf = json_data["elves"].get(slug, {})
    elf["continents"] = elf.get("continents", [])
    for c in elf["continents"]:
        if c["id"] == land:
            c["note"] = note
            break
    else:
        elf["continents"].append({
            "id": land,
            "note": note,
        })

# print(json_data["elves"])
# print(elves)