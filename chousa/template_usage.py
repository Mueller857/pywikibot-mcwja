from __future__ import annotations

import re
from collections import OrderedDict
import pywikibot
from pywikibot import textlib

def getstats(text, pattern):
    for usage in re.finditer(pattern, text):
        raw_text = usage.group(0) # テンプレートの元ウィキテキスト
        extracted = textlib.extract_templates_and_params(raw_text, strip=True)[0][1]
        if 'title' in extracted:
            return True

def main():
    # ボット動作環境
    site = pywikibot.Site()
    bot = pywikibot.Bot()
    # 汎用引数定義
    template_name = 'Template:Block'
    template = pywikibot.Page(site, template_name)
    match_builder = textlib.MultiTemplateMatchBuilder(site)
    pattern = match_builder.pattern(template, flags=re.DOTALL)
    # 対象ページリスト生成
    usages = template.getReferences(only_template_inclusion=True)
    #usages = [pywikibot.Page(site, "User:Müller857/Sandbox2")]
    #usages = pywikibot.Category(site,'Category:未確定な翻訳があるページ')
    for page in usages:
        ns = page.namespace
        if ns in [0, 10]:
            continue
        if getstats(page.text, pattern):
            print(page.title())

if __name__ == '__main__':
    main()