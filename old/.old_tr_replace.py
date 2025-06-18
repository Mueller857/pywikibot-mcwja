'''
this script does all necessary edits regarding Template:Translate and Template:Translatetitle when a new version is released.
What it does:

* moves all the pages in the list
* replaces all the Template:Translate usages with corresponding Japanese translation in pages on Category:未確定な翻訳があるページ.

this script retrieves data from a text file './data/tr_replace.txt' which should include partial copies of Module:Autolink subpages
'''

from __future__ import annotations

import re
import pywikibot
from pywikibot import pagegenerators
from pywikibot import textlib

def make_dict():
    tr_dict = {}
    data = open('./scripts/userscripts/data/tr_replace.txt')
    data_lines = [s.rstrip() for s in data.readlines()]
    for l in data_lines:
        if not re.match(r'\s*--.*', l):
            match = re.search(r"\s*\['(.*?)'\]\s*=\s*'(.*?)'", l)
            k = match.group(1)
            v = match.group(2)
            tr_dict[k] = v
    return tr_dict
        
def replink_cl(tr_dict):
    def replink(match):
        raw_input = match.group(1)
        link = False
        string = ''
        if re.search(r'\|link=[^\|]*', raw_input):
            link = True
        string = re.sub(r'\|[^\|]*?=[^\|]*', '', raw_input)
        string = re.search(r'\|([^\|]*)', string).group(1)
        string = autolink(string, tr_dict, link)
        if string == False:
            return r'{{tr' + raw_input + r'}}'
        if link == True:
            return '[[' + string + ']]'
        else:
            if r'|' in string:
                return re.search(r'(?<=\|).*', string).group()
            else:
                return string
    return replink

def autolink(string, tr_dict, link):
    arg = string.replace('-', ' ').lower()
    nolower = string.replace('-', ' ')
    suffix = ''
    # check for spawn egg
    if re.search(r' spawn egg$', arg):
        mob = tr_dict.get(arg[0:-10]) or False
        if not mob:
            return False
        mob = re.sub(r'.*?\|(.*)', r'\1', mob) or mob
        if mob:
            return 'スポーンエッグ|' + mob + 'のスポーンエッグ'
        else:
            return False
    be = False
    lce = False
    # check for version suffix
    if re.search(r' pe$', arg) or re.search(r' be$', arg):
        be = True
        arg = arg[0:-3]
    if re.search(r' lce$', arg):
        lce = True
        arg = arg[0:-4]
    
    # check for 'spawn'    
    if re.search(r'^spawn', arg):
        mob = tr_dict.get(arg[6:]) or False
        mob = re.sub(r'.*?\|(.*)', r'\1', mob) or mob
        if mob:
            result = 'スポーンエッグ|' + mob + 'のスポーンエッグ'
        else:
            result = False
        if be:
            suffix = '（Bedrock Edition）'
        if lce:
            suffix = '（Legacy Console Edition）'
        if result:
            if suffix != '':
                if r'|' in result:
                    result = result + suffix
                else:
                    result = result + '|' + result + suffix
            return result
        else:
            return False
    
    colors = {
    'black ': '黒色',
    'blue ': '青色',
    'brown ': '茶色',
    'cyan ': '青緑色',
    'gray ': '灰色',
    'green ': '緑色',
    'light blue ': '空色',
    'light gray ': '薄灰色',
    'lime ': '黄緑色',
    'magenta ': '赤紫色',
    'orange ': '橙色',
    'pink ': '桃色',
    'purple ': '紫色',
    'red ': '赤色',
    'silver ': '薄灰色',
    'white ': '白色',
    'yellow ': '黄色'
    }

    coloreditems = ['firework star', 'hardened clay', 'stained clay', 'banner', 'carpet', 'concrete',
	'concrete powder', 'glazed terracotta', 'terracotta', 'shield', 'shulker box', 'stained glass',
	'stained glass pane', 'wool', 'bed', 'hardened glass', 'hardened stained glass', 'balloon',
	'glow stick', 'hardened glass pane', 'hardened glass', 'sparkler', 'candle', 'bundle', 'harness']
    
    # check for color prefix
    color = ''
    for k, v in colors.items():
        pattern = r'^' + k
        if re.search(pattern, arg):
            item = arg[len(k)+1]
            if item in coloreditems:
                color = v
                arg = item
                break
    
    result = tr_dict.get(arg) or tr_dict.get(arg[0:-2]) or False
    if color != '':
        result = result + '|' + color + 'の' + result
    if be:
        suffix = '（Bedrock Edition）'
    if lce:
        suffix = '（Legacy Console Edition）'
    if result:
        if suffix != '':
            if r'|' in result:
                result = result + suffix
            else:
                result = result + '|' + result + suffix
    return result

def main():
    tr_dict = make_dict()
    site = pywikibot.Site()
    bot = pywikibot.Bot()
    #cat = pywikibot.Category(site,'Category:未確定な翻訳があるページ')
    #gen = pagegenerators.CategorizedPageGenerator(cat)
    template_name = 'Template:Translate'
    template = pywikibot.Page(site, template_name)
    gen = template.getReferences(only_template_inclusion=True)
    for page in gen:
        ns = page.namespace
        if ns in [0, 10]:#to test in sandbox, add 2 (user namespace)
            continue
        orig_text = page.text
        pattern = r'{{(?:tr|Tr|translate|Translate)(\|.*?)}}'
        new_text = re.sub(pattern, replink_cl(tr_dict), orig_text)
        explain = r'{{t|tr}}を該当バージョンでの日本語訳で置き換え' 
        #explain = r'{{t|tr}}置換ボットのテスト'
        #if page.text != new_text:
        #    page.text = new_text
        #    page.save(summary=explain)
        bot.userPut(page, orig_text, new_text, summary=explain)

if __name__ == '__main__':
    main()