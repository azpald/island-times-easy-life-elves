a = []

##################################################################
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
##################################################################

for b in a:
    slug = b[1]
    land = b[0]
    floor = b[2]
    note = f'Floor {floor}'
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