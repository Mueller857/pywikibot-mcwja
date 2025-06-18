import pywikibot
from pywikibot import pagegenerators
from pywikibot import textlib
import mwparserfromhell as mw
import re

site = pywikibot.Site()
bot = pywikibot.Bot()

sprite_templates_names = ['Biome',
                          'Block',
                          'DungeosEffect',
                          'DungeonsEnchantment',
                          'DungeonsEntity',
                          'DungeonsItem',
                          'Effect',
                          'Entity',
                          'Env',
                          'Inv',]

match_builder = textlib.MultiTemplateMatchBuilder(site)

def fix_links(text, title):
    #normal link
    #sprite link
    pattern = match_builder.pattern(template, flags=re.DOTALL)
    #main link

def main():
    gen = pagegenerators.PrefixingPageGenerator('チュートリアル/', namespace='')
    for page in gen:
        refers = page.getReferences(namespaces='Template')
        source = r'{}#(.*?)\|(.*?)\]\]'.format(page.title())
        target = r'[[チュートリアル:{}#\1|\2]]'.format(page.title()[8:])
        for refer in refers:
            orig_text = refer.text
            new_text = (orig_text, page.title)
            explain = 'リンク置き換え'
            bot.userPut(refer, orig_text, new_text, summary=explain)
            '''if orig_text != new_text:
                page.put(new_text, summary=explain, show_diff=True)'''

if __name__ == '__main__':
    main()