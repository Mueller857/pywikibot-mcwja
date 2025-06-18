import pywikibot
from pywikibot import pagegenerators
import mwparserfromhell

# 設定
SITE = pywikibot.Site()
TEMPLATE_NAME = 'LootChestItem'
BOT = pywikibot.Bot()
SUMMARY = r"[[MCT:スタイルガイド/セクション#「チェストから」について|節名統一の議論]]による"

def modify_sections():
    template = pywikibot.Page(SITE, 'Template:'+TEMPLATE_NAME)
    gen = template.getReferences(only_template_inclusion=True)
    for page in gen:
        text = page.text
        orig = text
        parsed = mwparserfromhell.parse(text)
        changed = False

        for section in parsed.get_sections(include_lead=False, include_headings=True, levels=[3]):
            headings = section.filter_headings()
            
            if not headings:
                continue

            heading = headings[0]
            section_title = heading.title.strip()
            
            # 節内に特定のテンプレートがあるかチェック
            templates = section.filter_templates(recursive=False)
            if any(tpl.name.matches(TEMPLATE_NAME) for tpl in templates):
                # 見出しを変更
                new_heading = "=== 宝箱から ==="
                text = text.replace(str(heading), new_heading, 1)
                changed = True

        # 変更があれば保存
        if changed:
            #BOT.userPut(page, orig, text, summary=SUMMARY)
            page.text = text
            page.save(summary=SUMMARY)

if __name__ == "__main__":
    modify_sections()
