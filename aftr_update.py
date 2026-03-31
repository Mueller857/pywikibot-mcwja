import pywikibot
from crowdin_api import CrowdinClient
from dotenv import load_dotenv
import os
import json
import argparse
import requests
from pathlib import Path
from collections import defaultdict
import re

BASE_DATA_PATH = "./scripts/userscripts/data/aftr/"
STRUCTURE_FILE = BASE_DATA_PATH + "structure.json" # 本プログラムの --output_structure_template モードで生成できる構造ファイル。コマンドラインからでは例外調整のための確認が行いにくいため、ファイルとして書き出しています。
LINK_OVERRIDES = BASE_DATA_PATH + "link_overrides.json" # リンク先が英名そのものではなく、Hoge (bar) のようにしたい文字列について、翻訳キー → bar の辞書のJSONとして指定できます。
CATEGORY_EXCECPTIONS = BASE_DATA_PATH + "category_exceptions.json" # 翻訳キーの第1部分から割り当てられるカテゴリとは異なる位置に配置したい文字列について、第2部分以降の前方一致文字列 → 配置先（misc.hoge.foo.barなど）の辞書のJSONとして指定できます。
OVERRIDES_EN = BASE_DATA_PATH + "overrides_en.json" # 英語の追加・上書き文字列。翻訳キー → 英語 の辞書JSONで記述し、既存の翻訳キーを使った場合はその文字列を上書きする。
OVERRIDES_JA = BASE_DATA_PATH + "overrides_ja.json" # 同上、日本語。

load_dotenv() # .env からCrowdinのトークンを取得

client = CrowdinClient(
    token = os.environ['CROWDIN_TOKEN'],
    project_id= 777584 # mcaf-resourcepack
)

files = client.source_files.with_fetch_all().list_files()

def build_source_dict() -> dict: # ファイル別のサブ辞書を持つ辞書を出力（原文用）
    files = client.source_files.with_fetch_all().list_files()
    file_map = {f["data"]["id"]: f["data"]["name"] for f in files["data"]}

    all_strings = client.source_strings.with_fetch_all().list_strings()

    result = defaultdict(dict)
    for item in all_strings["data"]:
        s = item["data"]
        file_name = file_map.get(s["fileId"], str(s["fileId"]))
        if args.target_files != [] and file_name not in args.target_files:
            continue
        result[file_name][s["identifier"].strip('"')] = s["text"]
    
    overrides_en: dict = json.loads(Path(OVERRIDES_EN).read_text(encoding="utf-8"))
    for file_name, strings in overrides_en.items():
        for key, text in strings.items():
            result[file_name][key] = text

    return dict(result)

def parse_lang(text: str) -> dict: # .lang ファイル用の簡易辞書化関数
    result = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):  # 空行・コメント行をスキップ
            continue
        key, _, value = line.partition("=")
        result[key.strip()] = value.strip()
    return result

def build_dict(language_id: str, en_dict: dict) -> dict: # ファイル別のサブ辞書を持つ辞書を出力（翻訳用）
    result = {}

    for item in files["data"]:
        f = item["data"]
        file_id = f["id"]
        file_name = f["name"]

        if args.target_files != [] and file_name not in args.target_files:
            continue

        export = client.translations.export_project_translation(
            targetLanguageId=language_id,
            fileIds=[file_id],
        )
        download_url = export["data"]["url"]
        response = requests.get(download_url)
        response.encoding = "utf-8"

        # json / lang 分岐
        ext = os.path.splitext(file_name)[1]
        if ext == ".json":
            raw = response.json()
            result[file_name] = {k.strip('"'): v for k, v in raw.items()}
        elif ext == ".lang":
            result[file_name] = parse_lang(response.text)

    overrides: dict = json.loads(Path(OVERRIDES_JA).read_text(encoding="utf-8"))
    for file_name, strings in overrides.items():
        for key, text in strings.items():
            result[file_name][key] = text

    link_overrides: dict = json.loads(Path(LINK_OVERRIDES).read_text(encoding="utf-8"))
    for file_name, strings in result.items():
        for key, text in strings.items():
            if key in link_overrides:
                strings[key] = f'{en_dict[file_name][key]} ({link_overrides[key]})|{text}'

    return result

CATEGORY_PREFIXES = { # 第1部分からカテゴリを推定するための対応表
    "tile": "BlockSprite",
    "block": "BlockSprite",
    "item": "ItemSprite",
    "biome": "BiomeSprite",
    "effect": "EffectSprite",
    "entity": "EntitySprite",
    "mob": "EntitySprite",
}

def output_structure_template(en_dict: dict): # 辞書構造出力モードのメイン動作
    """
    翻訳キー → Autolink辞書での掲載位置 のJSONを出力します。
    掲載位置は BlockSprite などサブ辞書名で記載され、コメントとインデントによるサブカテゴリを持つ場合は misc.advancement のようになります。
    """
    structure = {}

    category_exceptions: dict = json.loads(Path(CATEGORY_EXCECPTIONS).read_text(encoding="utf-8"))

    # en_dict の全キーを収集（ファイルをまたいで重複しうるが翻訳キーはユニーク想定）
    all_keys = {}
    for file_name, strings in en_dict.items():
        for key in strings:
            all_keys[key] = file_name  # キー → 元ファイル名

    for key, file_name in sorted(all_keys.items()):
        segments = key.split(".")
        first = segments[0].lower()

        len_element = 2
        if segments[1] == 'minecraft':
            len_element = 3

        category = CATEGORY_PREFIXES.get(first, "misc")

        # EnvSprite・misc はサブカテゴリとして残りのセグメントを入れておく
        if category in ("EnvSprite", "misc"):
            placement = f"{category}.{first}"
        else:
            placement = category
            if category != 'misc' and len(segments) > len_element:
                placement = 'misc.' + first
            if category in category_exceptions:
                for pattern in category_exceptions[category]:
                    if key.startswith(pattern):
                        placement = category_exceptions[category][pattern]

        structure[key] = placement

    Path(STRUCTURE_FILE).write_text(
        json.dumps(structure, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )
    print(f"構造ファイルを出力しました: {STRUCTURE_FILE} (翻訳キー数：{len(structure)})")

KNOWN_FILES = ["15w14a.lang", "1.RV-Pre1.lang", "3D_Shareware_v1.34.json", "20w14infinite.json", "22w13oneblockatatime.json", "23w13a_or_b.json", "24w14potato.json", "25w14craftmine.json"]

CATEGORIES = ["BlockSprite", "ItemSprite", "BiomeSprite", "EffectSprite", "EntitySprite", "EnvSprite", "misc"]

def construct_lua(ja_dict: dict, en_dict: dict) -> str: # 取得した英・日辞書と構造ファイルから、置き換え先のLuaを生成する
    if not Path(STRUCTURE_FILE).exists():
        raise FileNotFoundError(f"{STRUCTURE_FILE} が見つかりません。先に --output_structure_template を実行してください。")

    structure: dict = json.loads(Path(STRUCTURE_FILE).read_text(encoding="utf-8"))

    # en_dict のキー → ファイル名マップ
    key_to_file = {}
    file_order = KNOWN_FILES

    for file_name in en_dict:
        if file_name not in file_order:
            file_order.append(file_name)
    
    for file_name in file_order:
        if file_name not in en_dict:
            continue
        strings = en_dict[file_name]
        for key in strings:
            key_to_file[key] = file_name

    # 構造: category → file_name → subcategory(Noneも可) → [(en_lower, ja)]
    organized = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for key, placement in structure.items():
        # structure.jsonに存在するキーのみ処理（削除されたキーはスキップ）
        parts = placement.split(".", 1)
        category = parts[0]
        subcategory = parts[1] if len(parts) > 1 else None

        file_name = key_to_file.get(key, "unknown")
        en_text = en_dict.get(file_name, {}).get(key)
        ja_text = ja_dict.get(file_name, {}).get(key)

        if not en_text or not ja_text:
            continue

        organized[category][file_name][subcategory].append((en_text.lower(), ja_text))

    # Lua文字列を構築
    lines = ["return {"]

    for category in CATEGORIES:
        lines.append(f"\t['{category}'] = {{")
        file_map = organized.get(category, {})

        for file_name, sub_map in sorted(file_map.items()):
            for subcategory, entries in sorted(sub_map.items(), key=lambda x: (x[0] is None, x[0])):

                if subcategory is not None:
                    lines.append(f"\t\t-- {file_name} / {subcategory}")
                else:
                    lines.append(f"\t\t-- {file_name}")

                for en_lower, ja_text in sorted(entries):
                    en_escaped = en_lower.replace("\\", "\\\\").replace("'", "\\'").replace("\n", " ")
                    ja_escaped = re.sub(r'%(\d+\$)?s', '〇', ja_text.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "<br>"))
                    lines.append(f"\t\t['{en_escaped}'] = '{ja_escaped}',")

        lines.append("\t},")

    lines.append("}")
    return "\n".join(lines)

def edit(result): # 構築したLuaでモジュールを置き換え
    orig = MODULE.text
    BOT.userPut(MODULE, orig, result, summary=SUMMARY)

def create_redirects(ja_dict: dict, en_dict: dict): # 英名がコンテンツページになっている場合に、その日本語訳がそこへのリダイレクトになっていなければ作成 or 修正
    for file_name, strings in en_dict.items():
        for key, en_link in strings.items():
            ja_link = ja_dict.get(file_name, {}).get(key)
            if '|' in ja_link:
                en_link = ja_link.split('|')[0]
            en_link = " ".join(word.capitalize() for word in en_link.split(" ")) # 語頭の大文字化
            en_page = pywikibot.Page(SITE, en_link)
            if not en_page.exists() or en_page.isRedirectPage():
                continue
            ja_page = pywikibot.Page(SITE, ja_link)
            if not ja_page.exists() or (ja_page.isRedirectPage() and ja_page.getRedirectTarget() == en_page):
                text = f'#転送 [[{en_link}]]'
                BOT.userPut(ja_page, ja_page.text, text, summary=REDIRECT_SUMMARY)

def main():
    en_dict = build_source_dict()
    ja_dict = build_dict("ja", en_dict)
    if args.output_structure_template:
        output_structure_template(en_dict)
        return
    result = construct_lua(ja_dict, en_dict)
    edit(result)
    create_redirects(ja_dict, en_dict)

if __name__ == '__main__':
    SITE = pywikibot.Site()
    BOT = pywikibot.Bot()
    #MODULE = pywikibot.Page(SITE, 'モジュール:サンドボックス/Müller857') 
    MODULE = pywikibot.Page(SITE, 'Module:Autolink/Joke')
    SUMMARY = 'Crowdinからの更新'
    REDIRECT_SUMMARY = '翻訳変更・追加によるリダイレクト作成'
    parser = argparse.ArgumentParser()
    parser.add_argument('--target_files', nargs='*', default=[], help='辞書に登録するファイル名を1つ以上指定します。省略した場合、すべてのファイルを登録します。')
    parser.add_argument('--output_structure_template', action='store_true', help=f'辞書構造ファイルを {STRUCTURE_FILE} として出力します。編集は行いません。')
    args = parser.parse_args()
    main()