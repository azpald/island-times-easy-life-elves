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
    # text_content += '<div class="card article">'
    # text_content += f"""
    #     <div class="mugshot"><img src="{item["iconUrl"]}"/></div>
    # """
    # text_content += '</div>'
    
    text_content += '<div class="two-column">'
    text_content += f'<h2>Elves</h2>'
    e = elves_by_element.get(slug, [])
    if len(e) == 0:
        text_content += f'<p>No elf with {item["text"]} element.</p>'
    else:
        for elf in elves_by_element.get(slug, []):
            text_content += render_elf_item(elf, "h3")
    text_content += '</div>'

    page_content = page_content.replace("{{page_content}}", text_content)

    with open(dist / dir_elements / f"{slug}.html", "w", encoding="utf-8") as f:
        f.write(page_content)



# Create Elements index page
elements_text = ""
elements_text += '<div class="two-column container-multicolumns">'
for element in elements:
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
with open(dist / dir_elements / "index.html", "w", encoding="utf-8") as f:
    f.write(page_content)

