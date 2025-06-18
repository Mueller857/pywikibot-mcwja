from __future__ import annotations

import pywikibot
from pywikibot import pagegenerators

def main():
    tr_dict = make_dict()
    site = pywikibot.Site()
    bot = pywikibot.Bot()
    cat = pywikibot.Category(site,'Category:未確定な翻訳があるページ')
    #gen = pagegenerators.CategorizedPageGenerator(cat)
    gen = [pywikibot.Page(site, "Java Edition 1.21.2")]
    for page in gen:
        ns = page.namespace
        if ns in [0, 10]:#to test in sandbox, add 2 (user namespace)
            continue
        orig_text = page.text
        pattern = r'{{(?:tr|Tr|translate|Translate)(\|.*?)}}'
        new_text = re.sub(pattern, replink_cl(tr_dict), orig_text)
        explain = r'{{t|tr}}を該当バージョンでの日本語訳で置き換え' #'{{t|tr}}置換ボットのテスト'
        bot.userPut(page, orig_text, new_text, summary=explain)

if __name__ == '__main__':
    main()