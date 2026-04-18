import os
import json
import shutil
import glob
import sys
from pathlib import Path
from scripts.generatesitemap import get_url_priority
from datetime import datetime, timezone

def is_github_action():
    # Returns True if running in GitHub Actions, False otherwise
    return os.getenv('GITHUB_ACTIONS') == 'true'

# Vars
dir_elves = "elves"
dir_elements = "elements"
dir_skills = "skills"
dir_continents = "continents"

# Load jsons
folder_json = Path("json")
json_data = {}
for file in folder_json.glob("*.json"):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
        if isinstance(data, dict):
            for slug, d in data.items():
                if isinstance(d, dict):
                    d["key"] = slug
        json_data[file.stem] = data

elves = [elf for slug, elf in json_data["elves"].items()]
elves.sort(key=lambda x: x['name'])
elements = [element for slug, element in json_data["elements"].items()]
elements.sort(key=lambda x: x['text'])
skills = [skill for slug, skill in json_data["skills"].items()]
skills.sort(key=lambda x: x['name'])

with open("patchlocations.py") as f:
    exec(f.read())
with open("patchskills.py") as f:
    exec(f.read())
with open("json/elves.json", "w", encoding="utf-8") as f:
    f.write(json.dumps(json_data["elves"], indent=4))
# for i in json_data["continents"]:
#     print(i)

skills_by_element_which_active = {}
skills_by_element_which_passive = {}
elves_by_element = {}
elves_by_continent = {}
elves_by_skill = {}
for elf in elves:
    if elf["element"] not in elves_by_element:
        elves_by_element[elf["element"]] = []
    elves_by_element[elf["element"]].append(elf)

    if elf["element"] not in skills_by_element_which_active:
        skills_by_element_which_active[elf["element"]] = []

    if elf["element"] not in skills_by_element_which_passive:
        skills_by_element_which_passive[elf["element"]] = []

    for s in elf["skills"]:
        skill = json_data["skills"].get(s, False)
        if skill and skill.get("isActive", False):
            skills_by_element_which_active[elf["element"]].append(s)
        elif skill:
            skills_by_element_which_passive[elf["element"]].append(s)
        if s not in elves_by_skill:
            elves_by_skill[s] = []
        elves_by_skill[s].append(elf["key"])
    
    for c in elf.get("continents", []):
        if c["id"] not in elves_by_continent:
            elves_by_continent[c["id"]] = []
        elves_by_continent[c["id"]].append(elf)

for e in skills_by_element_which_active:
    skills_by_element_which_active[e] = [json_data["skills"][s] for s in set(skills_by_element_which_active[e])]
for e in skills_by_element_which_passive:
    skills_by_element_which_passive[e] = [json_data["skills"][s] for s in set(skills_by_element_which_passive[e])]

skills_which_active = []
skills_which_passive = []
skills_by_summon = {}
for skill in skills:
    if skill.get("isActive", False):
        skills_which_active.append(skill)
    else:
        skills_which_passive.append(skill)

    for e in skill.get("summon", []):
        if e not in skills_by_summon:
            skills_by_summon[e] = []
        skills_by_summon[e].append(skill["key"])


elves_by_master_continent = {}
continents_by_summon = {}
for summon, skills in skills_by_summon.items():
    for skill in skills:
        for master in elves_by_skill.get(skill, []):
            for c in json_data["elves"][master].get("continents", []):
                continent = c["id"]
                if continent not in elves_by_master_continent:
                    elves_by_master_continent[continent] = []
                elves_by_master_continent[continent].append({
                    "summon": summon,
                    "master": master,
                })

                if summon not in continents_by_summon:
                    continents_by_summon[summon] = []
                continents_by_summon[summon].append({
                    "master": master,
                    "continent": continent,
                })


# Prepare output folder
dist = Path("dist")
shutil.rmtree(dist, ignore_errors=True)
dist.mkdir(parents=True, exist_ok=True)

# Copy css, img, js
for d in ["css", "img", "js"]:
    src_dir = Path(d)
    dst_dir = dist / src_dir
    if src_dir.exists():
        # dirs_exist_ok=True allows copying into an existing folder 
        # instead of throwing an error.
        shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)

# Redirect 404 to home
with open(dist / "404.html", "w", encoding="utf-8") as f:
    f.write('<script>location.href="/";</script>')

# Hardcoded google-site-verification
google_code = "google27d3aaf513c20177.html"
with open(dist / google_code, "w", encoding="utf-8") as f:
    f.write(f'google-site-verification: {google_code}')

def get_dom_skill_id(skill):
    return f'{dir_skills}_{skill["key"]}'

def get_dom_skill_link(skill_name):
    skill = json_data["skills"].get(skill_name, {})
    name = skill.get("name", skill_name)
    link = ""
    if "key" in skill:
        link = f'/{dir_skills}/#{dir_skills}_{skill["key"]}'
    return f'<a href="{link}">{name}</a>' if link else f'<span>{name}</span>'

def get_dom_continent_link(continent_name):
    continent = json_data["continents"].get(continent_name, {})
    name = continent.get("text", continent_name)
    link = ""
    if "key" in continent:
        link = f'/{dir_continents}/{continent["key"]}.html'
    return f'<a href="{link}">{name}</a>' if link else f'<span>{name}</span>'

def get_dom_elf_link(elf_name):
    elf = json_data["elves"][elf_name]
    return f'<a href="/{dir_elves}/{elf_name}.html"><img alt="{elf["name"]}" class="inline-icon" src="{ json_data["elements"][elf["element"]]["iconUrl"] }">{elf["name"]}</a>'

def render_skill (skill_name, show_elves=False):
    if skill_name not in json_data["skills"]:
        print(f"Skill not found: {skill_name}", file=sys.stderr)
        return f' <div>[{skill_name}]</div> '

    skill = json_data["skills"][skill_name]
    skill_title = f'{skill["name"]}'
    skill_subtitle = f'Level: {skill["levelMax"]}/{skill["levelMax"]}'
    skill_description = skill["description"]

    # notes
    notes_copy = ""
    notes = skill.get("notes", [])
    if len(notes) > 0:
        notes_copy += "<blockquote><ul>"
        notes_copy += "".join([f'<li>{n}</li>' for n in notes])
        notes_copy += "</ul></blockquote>"

    # elves
    elves_copy = ""
    if show_elves:
        elves_copy += f"""<div><b class="green">Elves:</b> {", ".join([
            f'<a href="/{dir_elves}/{e}.html"><img alt="{json_data["elves"][e]["name"]}" class="inline-icon" src="{ json_data["elements"][json_data["elves"][e]["element"]]["iconUrl"] }">{json_data["elves"][e]["name"]}</a>' for e in elves_by_skill.get(skill_name, [])
        ])}</div>"""

    # summon
    summon_copy = ""
    skill_summon = skill.get("summon", [])
    if len(skill_summon) > 0:
        summon_copy += '<div><b class="green">Summons:</b> '
        summon_copy += ", ".join([
            f'<a href="/{dir_elves}/{s}.html"><img alt="{ json_data["elves"][s]["name"] }" class="inline-icon" src="{json_data["elves"][s]["imgUrl"]}">{ json_data["elves"][s]["name"] }</a>' for s in skill_summon
        ])
        summon_copy += "</div>"

    blockquote = ""
    if summon_copy or elves_copy:
        blockquote = f"""
            <blockquote>
                {summon_copy}
                {elves_copy}
            </blockquote>
        """

    # value
    i = 0
    while i < len(skill["valuesBase"]):
        value = skill["valuesBase"][i] + (skill["levelMax"] - 1) * skill["valuesIncrement"][i]
        skill_description = skill_description.replace("({{value" + str(i + 1) + "}})", "<span class=\"green\">({{value" + str(i + 1) + "}})</span>")
        skill_description = skill_description.replace("{{value" + str(i + 1) + "}}", str(value))
        i += 1
    return f"""
        <div class="skill-panel">
            <div class="skill-row">
                <div><img alt="{ skill_title }" class="icon-small" src="{skill["iconUrl"]}"/></div>
                <div>
                    <h3 id="{get_dom_skill_id(skill)}">{ skill_title }</h3>
                    <div>{ skill_subtitle }</div>
                    <div>{ skill_description }</div>
                </div>
            </div>
            {notes_copy}
            {blockquote}
        </div>
    """

def render_elf_item(elf, h="h2", show_locations=True):
    content = f'<div>{", ".join([json_data["stats"][stat_name]["text"] + ": " + str(stat_data["value"]) for stat_name, stat_data in elf["stats"].items()])}</div>'
    content += f'<div><b class="green">Skills:</b> {", ".join([get_dom_skill_link(s) for s in elf["skills"]])}</div>'
    if show_locations:
        # content += f"""
        #     <div><b class="green">Locations:</b> {", ".join(
        #         [get_dom_continent_link(s["id"]) for s in elf.get("continents", [])]
        #         + [get_dom_continent_link(s["continent"]) + f' (summoned by {get_dom_elf_link(s["master"])})' for s in continents_by_summon.get(elf["key"], [])]
        #     )}</div>
        # """
        content += f"""
            <div><b class="green">Locations:</b><ul> {" ".join(
                [f'<li>{get_dom_continent_link(s["id"])}</li>' for s in elf.get("continents", [])]
                + [f'<li>{get_dom_continent_link(s["continent"])} (summoned by {get_dom_elf_link(s["master"])})</li>' for s in continents_by_summon.get(elf["key"], [])]
            )}</ul></div>
        """
    elves_text = '<div>'
    elves_text += f'<{h}><a href="/{dir_elves}/{elf["key"]}.html"><img alt="{json_data["elements"][elf["element"]]["text"]} Element" class="inline-icon" src="{json_data["elements"][elf["element"]]["iconUrl"]}">{ "[BOSS] " if elf.get("isBoss") else "" }{ elf["name"] }</a></{h}>'
    elves_text += f'<div class="elf-row"><div><img alt="{ elf["name"] }" class="icon-medium" src="{elf["imgUrl"]}"/></div><div>{content}</div></div>'
    elves_text += '</div>'
    return elves_text

# Load page template
page_template = ""
with open("html/page.html", "r", encoding="utf-8") as f:
    page_template = f.read()

sitemap = []
def save_html(path, page_content):
    # sitemap
    # https://www.sitemaps.org/protocol.html
    url_path = path.relative_to(path.parts[0]).as_posix().removesuffix("index.html").rstrip('/')
    url = f"""{json_data["vars"]["site_origin"].rstrip('/')}/{url_path}"""
    priority = get_url_priority(url)
    lastmod = datetime.now(timezone.utc).isoformat(timespec='seconds')
    changefreq = "daily"
    sitemap.append({
        "loc": url,
        "priority": priority,
        "lastmod": lastmod,
        "changefreq": changefreq,
    })

    for placeholder, value in json_data["vars"].items():
        page_content = page_content.replace("{{" + placeholder + "}}", value)
    if not is_github_action():
        page_content += '<script src="/js/debug.js"></script>'
    with open(path, "w", encoding="utf-8") as f:
        f.write(page_content)

# Landing page
page_content = page_template
page_content = page_content.replace("{{post_title}}", "Home")
text_content = ""
text_content += '<div class="card two-column article" style="text-align: center;">'
text_content += f"""
    <img alt="Island TImes: Elves Library" src="/img/hero.jpg" style="width: 400px; max-width: 90vw;">
    <h1>Island Times: Elves Library</h1>
    <p>The unofficial wiki for elves</p>
    <p>A simple reference for the elves in Island Times: Easy Life.</p>
"""
text_content += '</div>'

text_content += '<div class="card two-column article container-multicolumns">'
text_content += f"""
    <div class="mugshot"><a href="/{dir_elves}/"><img alt="Elves" class="icon-medium" src="{json_data["vars"]["icon_menu_elves"]}"/><div>Elves</div></a></div>
    <div class="mugshot"><a href="/{dir_elements}/"><img alt="Elements" class="icon-medium" src="{json_data["vars"]["icon_menu_elements"]}"/><div>Elements</div></a></div>
    <div class="mugshot"><a href="/{dir_skills}/"><img alt="Skills" class="icon-medium" src="{json_data["vars"]["icon_menu_skills"]}"/><div>Skills</div></a></div>
    <div class="mugshot"><a href="/{dir_continents}/"><img alt="Continents" class="icon-medium" src="{json_data["vars"]["icon_menu_continents"]}"/><div>Continents</div></a></div>
"""
text_content += '</div>'
page_content = page_content.replace("{{page_content}}", text_content)
save_html(dist / "index.html", page_content)

###################################
# Write page for elves
###################################
with open("elves.py") as f:
    exec(f.read())

###################################
# Write page for elements
###################################
with open("elements.py") as f:
    exec(f.read())


###################################
# Write page for skills
###################################
(dist / dir_skills).mkdir(parents=True, exist_ok=True)
# for slug, item in json_data["skiils"].items():
#     page_content = page_template
#     page_content = page_content.replace("{{post_title}}", item["text"])

#     text_content = f"""
#         <nav class="breadcrumb" aria-label="Breadcrumb">
#             <ol>
#                 <li><a href="/">Home</a></li>
#                 <li><a href="/{dir_elements}/">Elements</a></li>
#                 <li aria-current="page">{item["text"]}</li>
#             </ol>
#         </nav>
#         <header class="post-header card two-column">
#             <h1 class="title"><img class="inline-icon" src="{ item.get("iconUrl") }"> { item["text"] }</h1>
#         </header>
#     """
#     # text_content += '<div class="card article">'
#     # text_content += f"""
#     #     <div class="mugshot"><img src="{item["iconUrl"]}"/></div>
#     # """
#     # text_content += '</div>'
    
#     text_content += '<div class="two-column">'
#     text_content += f'<h2>Elves</h2>'
#     e = elves_by_element.get(slug, [])
#     if len(e) == 0:
#         text_content += f'<p>No elf with {item["text"]} element.</p>'
#     else:
#         for elf in elves_by_element.get(slug, []):
#             text_content += render_elf_item(elf, "h3")
#     text_content += '</div>'

#     page_content = page_content.replace("{{page_content}}", text_content)

#     with open(dist / dir_elements / f"{slug}.html", "w", encoding="utf-8") as f:
#         f.write(page_content)

# Create Skills index page
skills_text = ""
skills_text += '<div class="two-column"><h2 class="in-blue">Active Skills</h2></div>'
for s in skills_which_active:
    if s.get("isUnlisted", False):
        continue
    skills_text += f'<div>{render_skill(s["key"], True)}</div>'

skills_text += '<div class="two-column"><h2 class="in-blue">Passive Skills</h2></div>'
for s in skills_which_passive:
    if s.get("isUnlisted", False):
        continue
    skills_text += f'<div>{render_skill(s["key"], True)}</div>'

page_content = page_template
page_content = page_content.replace("{{post_title}}", "Elements")

text_content = f"""
    <nav class="breadcrumb" aria-label="Breadcrumb">
        <ol>
            <li><a href="/">Home</a></li>
            <li aria-current="page">Skills</li>
        </ol>
    </nav>
    <header class="post-header card two-column">
        <h1 class="title">Skills</h1>
    </header>
"""
text_content += skills_text

page_content = page_content.replace("{{page_content}}", text_content)
save_html(dist / dir_skills / "index.html", page_content)


###################################
# Write page for continents
###################################
(dist / dir_continents).mkdir(parents=True, exist_ok=True)
for slug, item in json_data["continents"].items():
    page_content = page_template
    page_content = page_content.replace("{{post_title}}", item["text"])

    text_content = f"""
        <nav class="breadcrumb" aria-label="Breadcrumb">
            <ol>
                <li><a href="/">Home</a></li>
                <li><a href="/{dir_continents}/">Continents</a></li>
                <li aria-current="page">{item["text"]}</li>
            </ol>
        </nav>
        <header class="post-header card two-column">
            <h1 class="title"><img alt="{ item["text"] }" class="inline-icon" src="{ item.get("iconUrl") }"> { item["text"] }</h1>
        </header>
    """
    
    # Elves    
    text_content += '<div class="two-column">'
    text_content += f'<h2 class="in-blue">Elves</h2>'
    e = elves_by_continent.get(slug, [])
    set_elves = set()
    if len(e) == 0:
        text_content += f'<p>No elf in {item["text"]}.</p>'
    else:
        for elf in e:
            if elf["key"] in set_elves:
                continue
            set_elves.add(elf["key"])
            if elf.get("isUnlisted", False):
                continue
            text_content += render_elf_item(elf, "h3", show_locations=False)
    for d in elves_by_master_continent.get(slug, []):
        elf = json_data["elves"][d["summon"]]
        if elf["key"] in set_elves:
            continue
        set_elves.add(elf["key"])
        if elf.get("isUnlisted", False):
            continue
        text_content += render_elf_item(elf, "h3", show_locations=False)
    text_content += '</div>'

    page_content = page_content.replace("{{page_content}}", text_content)

    save_html(dist / dir_continents / f"{slug}.html", page_content)

# Create Continents index page
continents_text = '<div class="two-column container-multicolumns">'
for slug, item in json_data["continents"].items():
    continents_text += f"""
        <div class="mugshot">
            <a href="/{dir_continents}/{item["key"]}.html"><img alt="{item["text"]}" class="icon-medium" src="{item["iconUrl"]}"/><div>{item["text"]}</div></a>
        </div>
    """
continents_text += '</div>'

page_content = page_template
page_content = page_content.replace("{{post_title}}", "Elements")

text_content = f"""
    <nav class="breadcrumb" aria-label="Breadcrumb">
        <ol>
            <li><a href="/">Home</a></li>
            <li aria-current="page">Continents</li>
        </ol>
    </nav>
    <header class="post-header card two-column">
        <h1 class="title">Continents</h1>
    </header>
"""
text_content += continents_text

page_content = page_content.replace("{{page_content}}", text_content)
save_html(dist / dir_continents / "index.html", page_content)


# generate sitemap
# print(sitemap)
sitemap_copy = [f"""
    <url>
        <loc>{s["loc"]}</loc>
        <lastmod>{s["lastmod"]}</lastmod>
        <changefreq>{s["changefreq"]}</changefreq>
        <priority>{s["priority"]}</priority>
   </url> """ for s in sitemap
]
save_html(
    dist / "sitemap.xml",
    f"""<?xml version="1.0" encoding="UTF-8"?>
        <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
            {"".join(sitemap_copy)}
        </urlset> 
    """
)
