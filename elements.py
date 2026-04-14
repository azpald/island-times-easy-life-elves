# pyright: reportUndefinedVariable=false
# pylint: disable=undefined-variable

###################################
# Write page for elements
###################################
(dist / dir_elements).mkdir(parents=True, exist_ok=True)
for slug, item in json_data["elements"].items():
    page_content = page_template
    page_content = page_content.replace("{{post_title}}", item["text"])

    text_content = f"""
        <nav class="breadcrumb" aria-label="Breadcrumb">
            <ol>
                <li><a href="/">Home</a></li>
                <li><a href="/{dir_elements}/">Elements</a></li>
                <li aria-current="page">{item["text"]}</li>
            </ol>
        </nav>
        <header class="post-header card two-column">
            <h1 class="title"><img class="inline-icon" src="{ item.get("iconUrl") }"> { item["text"] }</h1>
        </header>
    """
    
    # Elves
    text_content += '<div class="two-column">'
    text_content += f'<h2 class="in-blue">Elves</h2>'
    e = elves_by_element.get(slug, [])
    if len(e) == 0:
        text_content += f'<p>No elf with {item["text"]} element.</p>'
    else:
        for elf in e:
            if elf.get("isUnlisted", False):
                continue
            text_content += render_elf_item(elf, "h3")
    text_content += '</div>'
    
    # Passive skills
    text_content += '<div class="two-column">'
    text_content += f'<h2 class="in-blue">Passive Skills</h2>'
    e = skills_by_element_which_passive.get(slug, [])
    if len(e) == 0:
        pass
        # text_content += f'<p>No elf with {item["text"]} element.</p>'
    else:
        for skill in e:
            if skill.get("isUnlisted", False):
                continue
            text_content += render_skill(skill["key"], True)
    text_content += '</div>'
    
    # Passive skills
    text_content += '<div class="two-column">'
    text_content += f'<h2 class="in-blue">Active Skills</h2>'
    e = skills_by_element_which_active.get(slug, [])
    if len(e) == 0:
        pass
        # text_content += f'<p>No elf with {item["text"]} element.</p>'
    else:
        for skill in e:
            if skill.get("isUnlisted", False):
                continue
            text_content += render_skill(skill["key"], True)
    text_content += '</div>'

    page_content = page_content.replace("{{page_content}}", text_content)

    save_html(dist / dir_elements / f"{slug}.html", page_content)


# Create Elements index page
elements_text = ""
elements_text += '<div class="two-column container-multicolumns">'
for _, element in json_data["elements"].items():
    elements_text += f'<div class="mugshot"><a href="/{dir_elements}/{element["key"]}.html"><img class="icon-medium" src="{element["iconUrl"]}"/><div>{element["text"]}</div></a></div>'
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

page_content = page_content.replace("{{post_description}}", "Elements in Island Times: Easy Life.")
save_html(dist / dir_elements / "index.html", page_content)

