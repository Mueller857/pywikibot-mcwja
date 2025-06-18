import pywikibot
import mwparserfromhell as mw
from scripts.userscripts import tr_replace
from scripts.userscripts import fixlinks

def move(page):
    parsed = mw.parse(page.text)
    target_name = ""
    afterroot = ""
    for template in parsed.filter_templates(matches=lambda t: tr_replace.normalize_template_name(t.name) in ALIASES):
        if template.has('1'):
            target_name = template.get('1').value
        else:
            if page.title().find('/') != -1:
                target_name, afterroot = page.title().split('/', 1)
            else:
                target_name = page.title()
    target_name = tr_replace.normalize_arg(target_name)
    target_name = tr_replace.autolink(target_name, False, SITE) + afterroot
    
    try:
        if input(f'{page.title()}を{target_name}に動かしますか？') == "y":
            return page.move(target_name, reason=SUMMARY_MOVE)
    except pywikibot.exceptions.PageRelatedError as e:
        print(f'ページの移動に失敗しました：{page.title()}→{target_name}')
    #return pywikibot.Page(SITE, target_name)

def update_redirect(page, old_name, new_name):
    orig = page.text
    parsed = mw.parse(orig)
    def fix_link_alt(title, anchor, text):
        return (new_name, anchor, text)
    fixlinks.fix_link = fix_link_alt
    parsed = fixlinks.wikilink(parsed, old_name)
    BOT.userPut(page, page.text, str(parsed), summary=SUMMARY_FIXREDIRECT)

def remove_template(page):
    orig = page.text
    parsed = mw.parse(orig)
    for template in parsed.filter_templates(matches=lambda t: tr_replace.normalize_template_name(t.name) in ALIASES):
        parent = parsed.get_parent(template)
        if not parent:
            parent = parsed
        index = parent.index(template)
        parent.remove(template)
        if index < len(parent.nodes):
            next_node = parent.nodes[index]
            if isinstance(next_node, mw.nodes.Text):
                next_node.value = next_node.value.lstrip('\n')
        break
    BOT.userPut(page, orig, str(parsed), summary=SUMMARY_REMOVAL)

def main():
    targets = TEMPLATE.getReferences(only_template_inclusion=True, namespaces=[0, 10])
    for page in targets:
        redirects = page.getReferences(filter_redirects=True)
        new_page = move(page)
        if new_page:
            for redirect in redirects:
                if redirect == new_page:
                    continue
                update_redirect(redirect, page.title(), new_page.title())
            remove_template(new_page)

if __name__ == '__main__':
    SITE = pywikibot.Site()
    BOT = pywikibot.Bot()
    TEMPLATE = pywikibot.Page(SITE, 'Template:Translate title')
    ALIASES = ['translate_title']
    SKIP_LIST = tr_replace.make_skip_list()
    SUMMARY_MOVE = '正式バージョンリリースに伴う移動'
    SUMMARY_FIXREDIRECT = '移動に伴うリダイレクト修正'
    SUMMARY_REMOVAL = r'{{t|translate title}}の除去'
    main()