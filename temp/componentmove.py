import pywikibot
from pywikibot import pagegenerators

SITE = pywikibot.Site()
TARGET_ROOT = 'データコンポーネント'
SUMMARY = r"コンポーネントに関する内容を[[データコンポーネント]]に移動"

TARGETS = [
	'アイテムフォーマット/banner patterns',
	'アイテムフォーマット/base color',
	'アイテムフォーマット/bees',
	'アイテムフォーマット/block entity data',
	'アイテムフォーマット/block state',
	'アイテムフォーマット/blocks attacks',
	'アイテムフォーマット/break sound',
	'アイテムフォーマット/bucket entity data',
	'アイテムフォーマット/bundle contents',
	'アイテムフォーマット/can break',
	'アイテムフォーマット/can place on',
	'アイテムフォーマット/charged projectiles',
	'アイテムフォーマット/consumable',
	'アイテムフォーマット/container',
	'アイテムフォーマット/container loot',
	'アイテムフォーマット/custom data',
	'アイテムフォーマット/custom model data',
	'アイテムフォーマット/custom name',
	'アイテムフォーマット/damage',
	'アイテムフォーマット/damage resistant',
	'アイテムフォーマット/death protection',
	'アイテムフォーマット/debug stick state',
	'アイテムフォーマット/dyed color',
	'アイテムフォーマット/enchantable',
	'アイテムフォーマット/enchantment glint override',
	'アイテムフォーマット/enchantments',
	'アイテムフォーマット/entity data',
	'アイテムフォーマット/equippable',
	'アイテムフォーマット/fire resistant',
	'アイテムフォーマット/firework explosion',
	'アイテムフォーマット/fireworks',
	'アイテムフォーマット/food',
	'アイテムフォーマット/glider',
	'アイテムフォーマット/hide additional tooltip',
	'アイテムフォーマット/hide tooltip',
	'アイテムフォーマット/instrument',
	'アイテムフォーマット/intangible projectile',
	'アイテムフォーマット/item model',
	'アイテムフォーマット/item name',
	'アイテムフォーマット/jukebox playable',
	'アイテムフォーマット/lock',
	'アイテムフォーマット/lodestone tracker',
	'アイテムフォーマット/lore',
	'アイテムフォーマット/map color',
	'アイテムフォーマット/map decorations',
	'アイテムフォーマット/map id',
	'アイテムフォーマット/max damage',
	'アイテムフォーマット/max stack size',
	'アイテムフォーマット/note block sound',
	'アイテムフォーマット/ominous bottle amplifier',
	'アイテムフォーマット/pot decorations',
	'アイテムフォーマット/potion contents',
	'アイテムフォーマット/potion duration scale',
	'アイテムフォーマット/profile',
	'アイテムフォーマット/provides banner patterns',
	'アイテムフォーマット/provides trim material',
	'アイテムフォーマット/rarity',
	'アイテムフォーマット/recipes',
	'アイテムフォーマット/repair cost',
	'アイテムフォーマット/repairable',
	'アイテムフォーマット/stored enchantments',
	'アイテムフォーマット/subcomponent/item effect',
	'アイテムフォーマット/subcomponent/status effect',
	'アイテムフォーマット/suspicious stew effects',
	'アイテムフォーマット/tool',
	'アイテムフォーマット/tooltip display',
	'アイテムフォーマット/tooltip style',
	'アイテムフォーマット/trim',
	'アイテムフォーマット/unbreakable',
	'アイテムフォーマット/use cooldown',
	'アイテムフォーマット/use remainder',
	'アイテムフォーマット/weapon',
	'アイテムフォーマット/writable book content',
	'アイテムフォーマット/written book content']

def main():
    for page_name in TARGETS:
        page = pywikibot.Page(SITE, page_name)
        title = page.title(with_ns=False).split('/', 1)[-1]
        page.move(TARGET_ROOT + '/' + title, reason=SUMMARY)

if __name__ == "__main__":
    main()