import os
import json
import shutil
import glob
from pathlib import Path

# Load jsons
folder_json = Path("json")
json_data = {}
for file in folder_json.glob("*.json"):
    with open(file, "r", encoding="utf-8") as f:
        json_data[file.stem] = json.load(f)

# Prepare output folder
dist = Path("dist")
shutil.rmtree(dist, ignore_errors=True)
dist.mkdir(parents=True, exist_ok=True)

# Copy css, img
for d in ["css", "img"]:
    src_dir = Path(d)
    dst_dir = dist / src_dir
    if src_dir.exists():
        # dirs_exist_ok=True allows copying into an existing folder 
        # instead of throwing an error.
        shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)

# Redirect 404 to home
with open(dist / "404.html", "w", encoding="utf-8") as f:
    f.write('<script>location.href="/";</script>')

def render_skill (skill_name):
    skill = json_data["skills"][skill_name]
    skill_title = f'{skill["name"]}'
    skill_subtitle = f'Level: {skill["levelMax"]}/{skill["levelMax"]}'
    skill_description = skill["description"]
    i = 0
    while i < len(skill["valuesBase"]):
        value = skill["valuesBase"][i] + (skill["levelMax"] - 1) * skill["valuesIncrement"][i]
        skill_description = skill_description.replace("{{value" + str(i + 1) + "}}", str(value))
        i += 1
    return f'<div class="skill-row"><div><img class="icon-medium" src="{skill["iconUrl"]}"/></div><div><h3>{ skill_title }</h3><div>{ skill_subtitle }</div> <div>{ skill_description }</div></div></div>'

def render_elf_item(elf):
    elves_text = '<div>'
    elves_text += f'<h2><a href="{elf["key"]}.html"><img class="inline-icon" src="{json_data["elements"][elf["element"]]["iconUrl"]}">{ elf["name"] }</a></h2>'
    elves_text += f'<div class="skill-row"><div><img class="icon-medium" src="{elf["imgUrl"]}"/></div><div>-</div></div>'
    elves_text += '</div>'
    return elves_text

# Load page template
page_template = ""
with open("html/page.html", "r", encoding="utf-8") as f:
    page_template = f.read()
for placeholder, value in json_data["vars"].items():
    page_template = page_template.replace("{{" + placeholder + "}}", value)

# Landing page
page_content = page_template
# page_content = page_content.replace("{{page_title}}", "Home")
page_content = page_content.replace("{{post_title}}", "Home")
text_content = ""
text_content += '<div class="card two-column article container-multicolumns">'
text_content += f"""
    <div class="mugshot"><a href="/elves/"><img class="icon-medium" src="{1}"/><div>Elves</div></a></div>
    <div class="mugshot"><a href="/elements/"><img class="icon-medium" src="{1}"/><div>Elements</div></a></div>
    <div class="mugshot"><a href="/continents/"><img class="icon-medium" src="{1}"/><div>Continents</div></a></div>
    <div class="mugshot"><a href="/skills/"><img class="icon-medium" src="{1}"/><div>Skills</div></a></div>
"""
text_content += '</div>'
page_content = page_content.replace("{{page_content}}", text_content)
with open(dist / "index.html", "w", encoding="utf-8") as f:
    f.write(page_content)



###################################
# Write page for elves
###################################
dir_elves = "elves"
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
                <li><a href="/elves/">Elves</a></li>
                <li aria-current="page">{elf["name"]}</li>
            </ol>
        </nav>
        <header class="post-header card two-column">
            <h1 class="title"><img class="inline-icon" src="{ json_data["elements"][elf["element"]]["iconUrl"] }"> { elf["name"] }</h1>
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
            <div class="form-row"><b>Element</b><a href="/elements/{elf["element"]}.html">{element["text"]}</a></div>
            {stat_text}
        </div>
    """
    text_content += '</div>'

    skill_text = ""
    for skill_name in elf["skills"]:
        skill_text += render_skill(skill_name)

    text_content += '<div class="card article">'
    text_content += '<h2>Skills</h2>'
    text_content += f"""
        <div>
            {skill_text}
        </div>
    """
    text_content += '</div>'

    page_content = page_content.replace("{{page_content}}", text_content)

    with open(dist / dir_elves / f"{slug}.html", "w", encoding="utf-8") as f:
        f.write(page_content)

# Create index page
elves = [{ "key": slug, **elf } for slug, elf in json_data["elves"].items()]
elves.sort(key=lambda x: x['name'])
elves_text = ""
elves_text += '<div class="card two-column">'
for elf in elves:
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


###################################
# Write page for elements
###################################
dir_elements = "elements"
(dist / dir_elements).mkdir(parents=True, exist_ok=True)
for slug, item in json_data["elements"].items():
    page_content = page_template
    page_content = page_content.replace("{{post_title}}", item["text"])

    text_content = f"""
        <nav class="breadcrumb" aria-label="Breadcrumb">
            <ol>
                <li><a href="/">Home</a></li>
                <li><a href="/elements/">Elements</a></li>
                <li aria-current="page">{item["text"]}</li>
            </ol>
        </nav>
        <header class="post-header card two-column">
            <h1 class="title"><img class="inline-icon" src="{ item.get("iconUrl") }"> { item["text"] }</h1>
        </header>
    """
    text_content += '<div class="card article">'
    text_content += f"""
        <div class="mugshot"><img src="{item["iconUrl"]}"/></div>
    """
    text_content += '</div>'

    page_content = page_content.replace("{{page_content}}", text_content)

    with open(dist / dir_elements / f"{slug}.html", "w", encoding="utf-8") as f:
        f.write(page_content)



# Create index page
elements = [{ "key": slug, **element } for slug, element in json_data["elements"].items()]
elements.sort(key=lambda x: x['text'])
elements_text = ""
elements_text += '<div class="two-column container-multicolumns">'
for element in elements:
    elements_text += f'<div class="mugshot"><a href="/elements/{element["key"]}.html"><img class="icon-medium" src="{element["iconUrl"]}"/><div>{element["text"]}</div></a></div>'
elements_text += '</div>'

page_content = page_template
page_content = page_content.replace("{{post_title}}", "Elements")

text_content = f"""
    <nav class="breadcrumb" aria-label="Breadcrumb">
        <ol>
            <li><a href="/">Home</a></li>
            <li aria-current="page">Elements</li>
        </ol>
    </nav>
    <header class="post-header card two-column">
        <h1 class="title">Elements</h1>
    </header>
"""
text_content += elements_text

page_content = page_content.replace("{{page_content}}", text_content)
with open(dist / dir_elements / "index.html", "w", encoding="utf-8") as f:
    f.write(page_content)




