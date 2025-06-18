import argparse
import pywikibot
from pywikibot import pagegenerators

LOCAL = pywikibot.Site()
EN = pywikibot.Site('en')
BOT = pywikibot.Bot()

def get_enpage(local_page):
    ns = local_page.namespace()
    en_nsname = EN.namespace()
    

def fix_missing_files(filepage, ensite):
    if not isinstance(filepage, pywikibot.FilePage):
        return
    
    return

def delete_dupfiles(filepage, ensite):
    if not isinstance(filepage, pywikibot.FilePage):
        return
    hash = filepage.get_file_info.sha1
    filepage_en = pywikibot.page(ensite, filepage.title())
    return

def main(args):
    # 動作環境定義
    if args['mode'] == 'moved':
        missings = pagegenerators.WantedPagesPageGenerator(namespace=6)
        for filepage in missings:
            fix_missing_files(filepage)
    if args['mode'] == 'dup':
        all_files = pagegenerators.AllpagesPageGenerator(namespace=6)
        for filepage in all_files:
            delete_dupfiles(filepage)
    else:
        print('unknown mode!')
    return

if __name__ == '__main__':
    parser = argparse = argparse.ArgumentParser()
    parser.add_argument('mode', default='moved', help = 'mode of fixing')
    args = parser.parser_args()
    main(args)