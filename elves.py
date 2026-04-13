# pyright: reportUndefinedVariable=false
# pylint: disable=undefined-variable

###################################
# Write page for elves
###################################
(dist / dir_elves).mkdir(parents=True, exist_ok=True)
for slug, elf in json_data["elves"].items():
    page_content = page_template
    # page_content = page_content.replace("{{page_title}}", "<img class=\"inline-icon\" src=\"" + json_data["elements"][elf["element"]]["iconUrl"] + "\"> " + elf["name"])
    page_content = page_content.replace("{{post_title}}", elf["name"])

    stat_text = ""
    for stat_name, stat_data in elf["stats"].items():
        stat_text += f'<div class="form-row"><b>{ json_data["stats"][stat_name]["text"] }</b><span>{ stat_data["value"] }</span></div>'


    element = json_data["elements"][elf["element"]]
    text_content = f"""
        <nav class="breadcrumb" aria-label="Breadcrumb">
            <ol>
                <li><a href="/">Home</a></li>
                <li><a href="/{dir_elves}/">Elves</a></li>
                <li aria-current="page">{elf["name"]}</li>
            </ol>
        </nav>
        <header class="post-header card two-column">
            <h1 class="title"><img class="inline-icon" src="{ json_data["elements"][elf["element"]]["iconUrl"] }"> { "[BOSS] " if elf.get("isBoss") else "" }{ elf["name"] }</h1>
        </header>
    """
    text_content += '<div class="card article">'
    text_content += f"""
        <div class="mugshot"><img src="{elf["imgUrl"]}"/></div>
    """
    # text_content += '</div>'
    # text_content += '<div class="card article">'
    text_content += f"""
        <div>
            <div class="form-row"><b>Element</b><a href="/{dir_elements}/{elf["element"]}.html">{element["text"]}</a></div>
            {stat_text}
        </div>
    """
    text_content += '</div>'

    skill_text = ""
    for skill_name in elf["skills"]:
        skill_text += render_skill(skill_name)

    text_content += '<div class="card article">'
    text_content += '<h2 class="in-blue">Skills</h2>'
    text_content += f"""
        <div>
            {skill_text}
        </div>
    """
    text_content += '</div>'

    summon_text = ""
    for s in skills_by_summon.get(slug, []):
        for m in elves_by_skill.get(s, []):
            elf_master = json_data["elves"][m]
            summon_text += f'<div>'
            summon_text += f'Summoned by: <a href="/{dir_elves}/{m}.html"><img class="inline-icon" src="{ json_data["elements"][elf_master["element"]]["iconUrl"] }">{elf_master["name"]}</a>'
            if len(elf_master.get("continents", [])) > 0:
                summon_text += f' (at {", ".join([json_data["continents"][s["id"]]["text"] for s in elf_master["continents"]])})'
            summon_text += f'</div>'
    location_text = ""
    for c in elf.get("continents", []):
        location_text += f'<div>At {json_data["continents"][c["id"]]["text"]} {"("+c["note"]+")" if c["note"] else ""}</div>'
        # location_text += f' (at {", ".join([json_data["continents"][s["id"]]["text"] for s in elf["continents"]])})'
    text_content += '<div class="card article two-column">'
    text_content += '<h2 class="in-blue">Locations</h2>'
    text_content += f"""
        <div>
            {summon_text}
            {location_text}
        </div>
    """
    text_content += '</div>'

    page_content = page_content.replace("{{page_content}}", text_content)

    with open(dist / dir_elves / f"{slug}.html", "w", encoding="utf-8") as f:
        f.write(page_content)

# Create index page
elves_text = ""
elves_text += '<div class="card two-column">'
for elf in elves:
    if elf.get("isUnlisted", False):
        continue
    elves_text += render_elf_item(elf)
elves_text += '</div>'

page_content = page_template
# page_content = page_content.replace("{{page_title}}", "Elves")
page_content = page_content.replace("{{post_title}}", "Elves")

text_content = f"""
    <nav class="breadcrumb" aria-label="Breadcrumb">
        <ol>
            <li><a href="/">Home</a></li>
            <li aria-current="page">Elves</li>
        </ol>
    </nav>
    <header class="post-header card two-column">
        <h1 class="title">Elves</h1>
    </header>
"""
text_content += elves_text

page_content = page_content.replace("{{page_content}}", text_content)
with open(dist / dir_elves / "index.html", "w", encoding="utf-8") as f:
    f.write(page_content)
