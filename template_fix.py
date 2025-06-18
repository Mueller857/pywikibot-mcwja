from __future__ import annotations

import re
from collections import OrderedDict
import pywikibot
from pywikibot import textlib

def fix_rule(params):
    if 'showcontent' in params[1]:
        params[1].pop("showcontent", None)
    
    content_keys = [f'content{i}' if i > 1 else 'content' for i in range(1, 7)]
    merged_content = ','.join(params[1].pop(key) for key in content_keys if key in params[1])
    
    if merged_content:
        params[1]['content'] = merged_content
    
    return params

def fix_params(match):
    raw_text = match.group(0) # テンプレートの元ウィキテキスト
    extracted = textlib.extract_templates_and_params(raw_text, strip=True)[0] #テンプレートの値を含むOrdered辞書。
    extracted = fix_rule(extracted)
    result = textlib.glue_template_and_params(extracted) # 辞書をウィキテキストに変換
    result = re.sub(r'\n\s*\n', '\n', result)
    #result = re.sub(r'\n}}', '}}', result)
    return result or raw_text

def edit(orig_text, pattern):
    return re.sub(pattern, fix_params, orig_text) or orig_text

def main():
    # ボット動作環境
    site = pywikibot.Site()
    bot = pywikibot.Bot()
    # 汎用引数定義
    template_name = 'Template:Feature ID'
    template = pywikibot.Page(site, template_name)
    match_builder = textlib.MultiTemplateMatchBuilder(site)
    pattern = match_builder.pattern(template, flags=re.DOTALL)
    explain = r'[[Template:Feature ID]]形式更新' #'テスト'
    #対象ページリスト生成
    usages = template.getReferences(only_template_inclusion=True)
    #usages = [pywikibot.Page(site, "User:Müller857/Sandbox2")]
    #usages = pywikibot.Category(site,'Category:未確定な翻訳があるページ')
    for page in usages:
        ns = page.namespace()
        if ns in [2]:
            continue
        orig_text = page.text
        new_text = edit(orig_text, pattern)
        bot.userPut(page, orig_text, new_text, summary=explain)
        #page.text = edit(orig_text, pattern)
        #page.save(summary=explain)

if __name__ == '__main__':
    main()