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
    # dst_dir.mkdir(parents=True, exist_ok=True)
    # for src_file in src_dir.iterdir():
    #     if src_file.is_file():
    #         shutil.copy2(src_file, dst_dir / src_file.name)
    if src_dir.exists():
        # dirs_exist_ok=True allows copying into an existing folder 
        # instead of throwing an error.
        shutil.copytree(src_dir, dst_dir, dirs_exist_ok=True)

# Load page template
page_template = ""
with open("html/page.html", "r", encoding="utf-8") as f:
    page_template = f.read()
for placeholder, value in json_data["vars"].items():
    page_template = page_template.replace("{{" + placeholder + "}}", value)

output_file = dist / "index.html"
with open(output_file, "w", encoding="utf-8") as f:
    f.write(page_template)

# Write page for elves
dir_elves = "elves"
(dist / dir_elves).mkdir(parents=True, exist_ok=True)
for slug, elf in json_data["elves"].items():
    page_content = page_template
    # page_content = page_content.replace("{{page_title}}", json_data["elements"][elf["element"]]["text"] + " " + elf["name"])
    # page_content = page_content.replace("{{page_title}}", elf["name"])
    page_content = page_content.replace("{{page_title}}", "<img class=\"inline-icon\" src=\"" + json_data["elements"][elf["element"]]["iconUrl"] + "\"> " + elf["name"])

    stat_text = ""
    for stat_name, stat_data in elf["stats"].items():
        stat_text += f'<div class="form-row"><b>{ json_data["stats"][stat_name]["text"] }</b><span>{ stat_data["value"] }</span></div>'


    element = json_data["elements"][elf["element"]]
    text_content = '<div class="card article">'
    text_content += f"""
        <div class="mugshot"><img src="{elf["imgUrl"]}"/></div>
    """
    # text_content += '</div>'
    # text_content += '<div class="card article">'
    text_content += f"""
        <div>
            <div class="form-row"><b>Element</b><span>{element["text"]}</span></div>
            {stat_text}
        </div>
    """
    text_content += '</div>'

    skill_text = ""
    for skill_name in elf["skills"]:
        skill = json_data["skills"][skill_name]
        skill_title = f'{skill["name"]}'
        skill_subtitle = f'Level: {skill["levelMax"]}/{skill["levelMax"]}'
        skill_description = skill["description"]
        i = 0
        while i < len(skill["valuesBase"]):
            value = skill["valuesBase"][i] + (skill["levelMax"] - 1) * skill["valuesIncrement"][i]
            skill_description = skill_description.replace("{{value" + str(i + 1) + "}}", str(value))
            i += 1
        skill_text += f'<div class="skill-row"><div><img src="{skill["iconUrl"]}"/></div><div><h3>{ skill_title }</h3><div>{ skill_subtitle }</div> <div>{ skill_description }</div></div></div>'

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
