from __future__ import annotations

import re
import pywikibot
from pywikibot import pagegenerators

def main():
    # ボット動作環境
    slink_list = {}
    site = pywikibot.Site()
    bot = pywikibot.Bot()
    # 汎用変数定義
    page_name = "レコード"
    link_to = pywikibot.Page(site, page_name)
    # ページ集合生成
    gen = link_to.getReferences()
    print('Collecting section link instances ...')
    for page in gen:
        print('in ' + page.title() + ':')
        orig_text = page.text
        pattern = r'\[\[' + page_name + r'#(.*?)\|'
        instances = re.findall(pattern, orig_text)
        for slink in instances:
            if slink not in slink_list:
                slink_list[slink] = 1
            else:
                slink_list[slink] += 1
    if slink_list != {}:
        for item in slink_list:
            print(item + ': ' + str(slink_list[item]))
    else:
        print('No section link instances found!')
if __name__ == '__main__':
    main()