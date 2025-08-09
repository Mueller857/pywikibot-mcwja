from __future__ import annotations
import argparse
import re
import pywikibot
import mwparserfromhell as mw

anchor_map = {
    'その他のデバッグキー': 'ショートカット',
    'デバッグキーの詳細': 'ショートカット'
}

text_map = {
}

def get_pages(page_name):
    base_page = pywikibot.Page(SITE, page_name)
    print(f'collecting redirects for {page_name}...')
    pages = [base_page]
    for page in base_page.getReferences(filter_redirects=True):
        if '#' not in page.getRedirectTarget().title():
            pages.append(page)
    return pages

def fix_link(title, anchor, text):
    if args.after:
        title = args.after.replace('_', ' ')
    if str(text) in text_map:
        text = text_map[str(text)]
    if anchor in anchor_map:
        anchor = anchor_map[anchor]
        if r'|' in anchor:
            text_split = anchor.split(r"|")
            anchor = text_split[0]
            text = text_split[-1]
        if re.match(r'^:', anchor):
            if r'#' in anchor:
                title_split = anchor.split(r'#')
                title = re.sub(r'^:', '', title_split[0])
                anchor = title_split[-1]
            else:
                title = re.sub(r'^:', '', anchor)
                anchor = None
                if title == text:
                    text = None
    return (title, anchor, text)

def linktitle_parse(title):
    if '#' in title:
        title_split = title.split('#')
        title = title_split[0]
        anchor = title_split[-1]
    else:
        title = title
        anchor = None
    return (title, anchor)

def wikilink(parsed, target_name):
    for wikilink in parsed.filter_wikilinks():
        title_parsed = linktitle_parse(wikilink.title)
        if title_parsed[0] != target_name:
            continue
        newlink = fix_link(title_parsed[0], title_parsed[1], wikilink.text)
        wikilink.title = f'{newlink[0]}#{newlink[1]}' if newlink[1] else newlink[0]
        wikilink.text = newlink[2]
    return parsed

def t_spritelink(template, target_name):
    if template.has('link'):
        if template.get('link').value != 'none':
            title_parsed = linktitle_parse(template.get('link').value)
        else: 
            return template
    elif template.has('1'):
        title_parsed = linktitle_parse(template.get('1').value)
    else: return template
    if title_parsed[0] != target_name:
        return template
    
    if template.has('2'):
        text = template.get('2').value
    elif template.has('text'):
        text = template.get('text').value
    elif template.has('link') and template.has('1'):
        text = template.get('1')
    else:
        text = None
    
    newlink = fix_link(title_parsed[0], title_parsed[1], text)

    title = f'{newlink[0]}#{newlink[1]}' if newlink[1] else newlink[0]
    if template.has('link'):
        template.add('link', title)
    else:
        if not template.has('id'):
            template.add('link', title)
        else:
            template.add('1', title)
    if newlink[2]:
        if template.has('text'):
            template.remove('text')
        template.add('2', str(newlink[2]))
    return template
     
def t_main_seealso(template, target_name):
    n = 1
    while template.has(str(n)):
        title_parsed = linktitle_parse(template.get(str(n)).value)
        if title_parsed[0] != target_name:
            n += 1
            continue
        if template.has('title'+str(n)):
            text = template.get('title'+str(n).value)
        else:
            text = None
        newlink = fix_link(title_parsed[0], title_parsed[1], text)
        template.add(str(n), f'{str(newlink[0])}#{str(newlink[1])}' if newlink[1] else str(newlink[0]))
        if newlink[2]:
            template.add('title'+str(n), str(newlink[2]))
        n += 1
    return template
    
def t_disambig(template, target_name, name):
    if name == 'for':
        n = 2
    else:
        n = 3
    while template.has(str(n)):
        title_parsed = linktitle_parse(template.get(str(n)).value)
        if title_parsed[0] != target_name:
            n += 2
            continue
        newlink = fix_link(title_parsed[0], title_parsed[1], None)
        template.add(str(n), f'{str(newlink[0])}#{str(newlink[1])}' if newlink[1] else str(newlink[0]))
        n += 2
    return template

def t_slink(template, target_name):
    if template.has('1'):
        title = template.get('1').value
        if template.has('2'):
            anchor = template.get('2').value
        else:
            title_parsed = linktitle_parse(title)
            title = title_parsed[0]
            anchor = title_parsed[1]
        if title != target_name:
            return template
        newlink = fix_link(title, anchor, None)
        template.add('1', str(newlink[0]))
        if newlink[1]:
            template.add('2', str(newlink[1]))
    return template

def linktemplate(parsed, target_name):
    for template in parsed.filter_templates():
        name = (template.name[0].lower() + template.name[1:]).replace(' ', '_')
        if name in ['biomeLink', 'blockLink', 'effectLink', 'entityLink', 'envLink', 'itemLink', 'personaLink', 'invLink', 'legacyBlockLink']:
            template = t_spritelink(template, target_name)
        if name in ['main', 'see_also']:
            template = t_main_seealso(template, target_name)
        if name in ['about', 'for', 'redirect']:
            template = t_disambig(template, target_name, name)
        if name in ['slink', 'section_link']:
            template = t_slink(template, target_name)
    return parsed

def edit(page, target_name):
    orig = page.text
    parsed = mw.parse(page.text)
    parsed = wikilink(parsed, target_name)
    parsed = linktemplate(parsed, target_name)
    BOT.userPut(page, orig, str(parsed), summary=args.summary)
    '''if orig != str(parsed):
        page.text = str(parsed)
        page.save(summary=explain)'''

def main():
    page_name = args.before
    targets = get_pages(page_name)
    for target in targets:
        gen = target.getReferences(namespaces=[0, 10])
        target_name = target.title()
        for page in gen:
            edit(page, target_name)

if __name__ == '__main__':
    SITE = pywikibot.Site()
    BOT = pywikibot.Bot()

    parser = argparse.ArgumentParser()
    parser.add_argument('before', help='name of the page whither links should be fixed')
    parser.add_argument('after', nargs="?", default=False, help='name of the page whither the link should be')
    parser.add_argument('--summary', required=True, help='name of the page whither links should be fixed')
    args = parser.parse_args()
    main()