from __future__ import annotations

import re
import pywikibot
import mwparserfromhell as mw

def make_list(type):
    list = []
    data = open(f'./scripts/userscripts/data/tr_{type}.txt')
    data_lines = [s.rstrip() for s in data.readlines()]
    for l in data_lines:
        if not re.match(r'\s*--.*', l):
            match = re.search(r"\s*\['(.*?)'\]\s*=\s*'(.*?)'", l)
            if match:
                k = match.group(1)
                list.append(k)
    return list

def normalize_template_name(name):
    name = name.strip().replace(" ", "_")
    if not name:
        return ""
    return name[0].lower() + name[1:]

def normalize_arg(arg):
    arg = str(arg).strip().replace("-", " ").lower()
    if not arg:
        return ""
    return arg

def extentional_tag_parse(parsed):
    for tag in parsed.filter_tags():
        if tag.contents:
            tag.contents = extentional_tag_parse(mw.parse(str(tag.contents)))
    return parsed

def replace_link(parsed, title):
    parsed = extentional_tag_parse(parsed)
    for template in parsed.filter_templates(matches=lambda t: normalize_template_name(t.name) in ALIASES):
        if template.has('1'):
            string = template.get('1').value
        else:
            string = title
        norm = normalize_arg(string)
        if norm in SKIP_LIST:
            continue
        if norm in USELINK_LIST:
            uselink = True
        else:
            uselink = False
        if template.has('link'):
            link = True
        else:
            link = False
        parsed.replace(template, autolink(string, link, uselink, SITE))
    return parsed

def autolink(string, link, uselink, site):
    if link:
        if uselink:
            text = f"{{{{tr|raw=1|link=1|{string}}}}}"
        else:
            text = f"[[{{{{tr|raw=1|{string}}}}}]]"
    else:
        text = f"{{{{tr|raw=1|{string}}}}}"
    query_params = {
        "action": "expandtemplates",
        "text": text,
        "prop": "wikitext",
        "format": "json"
    }
    if site:
        SITE = site
    data = SITE.simple_request(**query_params).submit()
    expanded = data['expandtemplates']['wikitext']
    return expanded

def edit(page):
    orig = page.text
    parsed = mw.parse(orig)
    parsed = replace_link(parsed, page.title())
    BOT.userPut(page, orig, str(parsed), summary=SUMMARY)
    '''if orig != str(parsed):
        page.text = str(parsed)
        page.save(summary=explain)'''

def main():
    targets = TEMPLATE.getReferences(only_template_inclusion=True, namespaces=[0, 10])
    for page in targets:
        if page != pywikibot.Page(SITE, 'Template:Translate/doc'):
            edit(page)

if __name__ == '__main__':
    SITE = pywikibot.Site()
    BOT = pywikibot.Bot()
    TEMPLATE = pywikibot.Page(SITE, 'Template:Translate')
    ALIASES = ['tr', 'translate']
    SKIP_LIST = make_list('skip')
    USELINK_LIST = make_list('use_link')
    SUMMARY = r'{{t|tr}}を該当バージョンでの日本語訳で置き換え'
    main()