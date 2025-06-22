import pywikibot
from pywikibot import pagegenerators as gen
import requests
import re
import mwparserfromhell as mw
from scripts.userscripts import tr_replace

def edit(page):
    # タイトルからバージョン名を抽出して正規化
    ver = page.title()
    ver = ver.replace('Java Edition ', '')  # 先頭の削除
    ver = re.sub(r' Pre-release (\d+)', r'-pre\1', ver)
    ver = re.sub(r' Pre-Release (\d+)', r'-pre\1', ver)
    ver = re.sub(r' Release Candidate (\d+)', r'-rc\1', ver)

    # 言語ファイルのURL
    base_url = f'https://assets.mcasset.cloud/{ver}/assets/minecraft/lang'
    ja_url = f'{base_url}/ja_jp.json'
    en_url = f'{base_url}/en_us.json'

    try:
        ja_lang = requests.get(ja_url).json()
        en_lang = requests.get(en_url).json()
    except Exception as e:
        print(f'Failed to load language files for {ver}: {e}')
        return

    # 英→日翻訳辞書を構成
    translation_dict = {}
    for key, en_text in en_lang.items():
        ja_text = ja_lang.get(key)
        if ja_text:
            translation_dict[en_text] = ja_text
    
    code = mw.parse(page.text)
    # --- ノードごとの翻訳置換処理 ---
    for node in code.filter(recursive=True):
        if not isinstance(node, mw.nodes.Text):  # テキストノードのみ処理
            continue

        original_text = str(node)
        current_text = original_text
        node_modified = False

        # 置換対象候補を、キーの長さで降順ソートして探索
        for en_phrase in sorted(translation_dict.keys(), key=len, reverse=True):
            if en_phrase in ["Edit", "server", "chat", "Sign"]:
                continue
            ja_phrase = translation_dict[en_phrase]
            if en_phrase in current_text:
                proposed_text = current_text.replace(en_phrase, ja_phrase)
                if proposed_text != current_text:
                    print("\n--- 翻訳候補が見つかりました ---")
                    print(f"英語フレーズ: \"{en_phrase}\"")
                    print(f"変更前:\n{current_text}")
                    print(f"変更後:\n{proposed_text}")
                    user_input = input("この変更を反映しますか？ (f/d): ")
                    if user_input.lower() == 'f':
                        current_text = proposed_text
                        node_modified = True

        if node_modified:
            node.value = current_text
            modified = True

    for template in code.filter_templates(matches=lambda t: tr_replace.normalize_template_name(t.name) in ["訳註", "訳注", "翻訳途中", "要翻訳", "作業中", "wip", "work in process"]):
        parent = code.get_parent(template)
        if not parent:
            parent = code
        index = parent.index(template)
        parent.remove(template)
        if index < len(parent.nodes):
            next_node = parent.nodes[index]
            if isinstance(next_node, mw.nodes.Text):
                next_node.value = next_node.value.lstrip('\n')
    
   # --- 〔中括弧〕の削除（確認不要） ---
    final_text = str(code)
    final_text = re.sub(r'〔[^〕]*〕', '', final_text)

    BOT.userPut(page, page.text, final_text, summary=SUMMARY)
    


def main():
    targets = gen.CategorizedPageGenerator(CAT)
    for page in targets:
        if pywikibot.Page(SITE, 'カテゴリ:Java Editionのバージョン') in page.categories():
            edit(page)

if __name__ == '__main__':
    SITE = pywikibot.Site()
    BOT = pywikibot.Bot()
    CAT = pywikibot.Category(SITE, 'カテゴリ:未確定な翻訳があるページ')
    SUMMARY = r'新方針で書き換え'
    main()