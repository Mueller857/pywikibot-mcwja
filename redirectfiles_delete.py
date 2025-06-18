import pywikibot
import re

def main():
    site = pywikibot.Site()
    ensite = pywikibot.Site('en')
    page_list = open('./delete.txt')
    pages = [re.search(r"#\s*\[\[(.*?)\]\]", s.rstrip()).group(1) for s in page_list.readlines()]
    for page_name in pages:
        print('checking deleted page "' + page_name +'" ...')
        page = pywikibot.Page(site, page_name)
        if page.namespace().id != 6:
            continue
        redirects = page.getReferences(filter_redirects=True)
        for redirect in redirects:
            if redirect.namespace().id != 6:
                continue
            redirect_name = redirect.title(with_ns=False)
            print('checking redirect page "' + redirect_name +'" ...')
            redirect_en = pywikibot.Page(ensite, 'File:' + redirect_name)
            if redirect_en.exists():
                redirect.delete(reason='削除されたページへのリダイレクト', prompt=False)
            else:
                print('skipped due to no same page on en')

if __name__ == '__main__':
    main()