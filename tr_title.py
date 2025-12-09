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
    if target_name in SKIP_LIST:
        return
    target_name = tr_replace.autolink(target_name, False, page.title(), False, SITE) + afterroot
    
    try:
        if input(f'{page.title()}を{target_name}に動かしますか？[y/n]\n') == "y":
            return page.move(target_name, reason=SUMMARY_MOVE)
    except pywikibot.exceptions.ArticleExistsConflictError as e:
        if input(f'記事「{target_name}」は既に存在し、2回以上の履歴があります。\n削除して再度移動を試みますか？[y/n]\n') == "y":
            target_page = pywikibot.Page(SITE, target_name)
            target_page.delete(reason=SUMMARY_DELETE, prompt=False)
    except pywikibot.exceptions.PageRelatedError as e:
        print(f'ページの移動に失敗しました：{page.title()}→{target_name}\n')
    #return pywikibot.Page(SITE, target_name) # for debug, bypasses move failure 

def update_redirect(page, old_name, new_name):
    orig = page.text
    parsed = mw.parse(orig)
    def fix_link_alt(title, anchor, text):
        return (new_name, anchor, text)
    fixlinks.fix_link = fix_link_alt
    parsed = fixlinks.wikilink(parsed, old_name)
    BOT.userPut(page, page.text, str(parsed), summary=SUMMARY_FIXREDIRECT)

def remove_template(parsed):
    for template in parsed.filter_templates(matches=lambda t: tr_replace.normalize_template_name(t.name) in ALIASES):
        parent = parsed.get_parent(template) #テンプレートの削除は親ノードに対して行う必要がある
        if not parent:
            parent = parsed
        index = parent.index(template)
        parent.remove(template)
        if index < len(parent.nodes):
            next_node = parent.nodes[index]
            if isinstance(next_node, mw.nodes.Text):
                next_node.value = next_node.value.lstrip('\n')
        break
    return parsed

def add_sortkey(parsed, title):
    last_section = parsed.filter_headings()[-1]
    length = len(parsed.nodes)
    index = parsed.index(last_section)
    while index <= length -1:
        next_node = parsed.nodes[index]
        if isinstance(next_node, mw.nodes.Wikilink):
            confirm = False
            while confirm == False:
                sortkey = input(f'{title}に対する適切なソートキーを指定してください。\n')
                if input(f'{title}のソートキーは{sortkey}でよろしいですか？[y/n]\n') == 'y':
                    confirm = True
            parsed.insert_before(next_node, f'{{{{デフォルトソートキー:{sortkey}}}}}\n\n')
            return parsed
        index += 1
    return parsed

def page_update(page):
    orig = page.text
    parsed = mw.parse(orig)
    parsed = remove_template(parsed)
    parsed = add_sortkey(parsed, page.title())
    BOT.userPut(page, orig, str(parsed), summary=SUMMARY_UPDATE)

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
            page_update(new_page)

if __name__ == '__main__':
    SITE = pywikibot.Site()
    BOT = pywikibot.Bot()
    TEMPLATE = pywikibot.Page(SITE, 'Template:Translate title')
    ALIASES = ['translate_title']
    SKIP_LIST = tr_replace.make_list('skip')
    SUMMARY_MOVE = '正式バージョンリリースに伴う移動'
    SUMMARY_DELETE = '正式バージョンリリースに伴う移動に先立つ、移動先削除'
    SUMMARY_FIXREDIRECT = '移動に伴うリダイレクト修正'
    SUMMARY_UPDATE = r'{{t|translate title}}の除去とソートキーの追加'
    main()