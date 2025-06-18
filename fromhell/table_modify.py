import mwparserfromhell as mw
import re

text = r"""
{|class="wikitable sortable" style="width:100%;text-align:center;font-size:smaller" data-description="Music tracks"
!Filename<br>in ''Minecraft''
![[Gameplay]]
!Soundtrack Title
!Soundtrack
!Artist
!Length
! class="unsortable" |Track preview
|-
!aerie.ogg
|[[Forest]], [[Old Growth Taiga]], [[Lush Caves]] and [[Swamp]]
|"[[Aerie]]"
|{{sort|W02|''[[Minecraft: The Wild Update (Original Game Soundtrack)]]'' No. 2}}
|Lena Raine
|4:56
|[[File:Aerie.ogg]]
|-
!aria_math.ogg<wbr>{{only|je|short=1}}<br>creative4.ogg<wbr>{{only|be|short=1}}
|[[Creative]] mode
|"[[Aria Math]]"
|{{sort|B13|''[[Minecraft - Volume Beta]]'' No. 13}}
|C418
|5:09
|[[File:Aria math.ogg]]
|-
!ancestry.ogg
|[[Deep Dark]]
|"[[Ancestry]]"
|{{sort|C03|''[[Minecraft: Caves & Cliffs (Original Game Soundtrack)]]'' No. 3}}
|Lena Raine
|5:43
|[[File:Ancestry.ogg]]
|-
!a_familiar_room.ogg
|[[Creative]] and [[Survival]] {{in|je}}{{Note|"A Familiar Room" does not play in [[Survival]] mode on {{el|BE}} due to a bug.<ref>{{bug|MCPE-175998||"A Familiar Room" doesn't play in Survival mode}}</ref>}}
|"[[A Familiar Room]]"
|{{sort|Tra02|''[[Minecraft: Trails & Tales (Original Game Soundtrack)]]'' No. 2}}
|Aaron Cherof
|4:01
|[[File:A Familiar Room.ogg]]
|-
!an_ordinary_day.ogg
|[[Dripstone Caves]], [[Lush Caves]], and [[Snowy Slopes]]
|"[[An Ordinary Day]]"
|{{sort|C10|''[[Minecraft: Caves & Cliffs (Original Game Soundtrack)]]'' No. 10}}
|Kumi Tanioka
|5:31
|[[File:An ordinary day.ogg]]
|-
!below_and_above.ogg
||[[Survival]] {{in|java|bedrock}}, [[Creative]] {{in|java}}, and [[Main Menu]]; further emphasized in [[Cherry Grove]]s.{{upcoming|java 1.21.6}}
|"[[Below and Above]]"
|{{sort|25SD02|''[[Minecraft: Game Drop 2 - 2025 (Original Game Soundtrack)]]'' No. 2}}
|Amos Roddy
|3:32
|[[File:Below and Above.ogg]]
|-
!biome_fest.ogg<wbr>{{only|je|short=1}}<br>creative1.ogg<wbr>{{only|be|short=1}}
|[[Creative]] mode
|"[[Biome Fest]]"
|{{sort|B08|''[[Minecraft - Volume Beta]]'' No. 8}}
|C418
|6:17
|[[File:Biome fest.ogg]]
|-
!blind_spots.ogg<wbr>{{only|je|short=1}}<br>creative2.ogg<wbr>{{only|be|short=1}}
|[[Creative]] mode
|"[[Blind Spots]]"
|{{sort|B04|''[[Minecraft - Volume Beta]]'' No. 4}}
|C418
|5:31
|[[File:Blind spots.ogg]]
|-
!broken_clocks.ogg
||[[Survival]] {{in|java|bedrock}}, [[Creative]] {{in|java}}, and [[Main Menu]]; further emphasized in [[Forest]]s.{{upcoming|java 1.21.6}}
|"[[Broken Clocks]]"
|{{sort|25SD04|''[[Minecraft: Game Drop 2 - 2025 (Original Game Soundtrack)]]'' No. 4}}
|Amos Roddy
|3:33
|[[File:Broken Clocks.ogg]]
|-
!bromeliad.ogg
|[[Bamboo Jungle]], [[Cherry Grove]], [[Flower Forest]], [[Forest]], [[Jungle]], and [[Sparse Jungle]]
|"[[Bromeliad]]"
|{{sort|Tra03|''[[Minecraft: Trails & Tales (Original Game Soundtrack)]]'' No. 3}}
|Aaron Cherof
|5:12
|[[File:Bromeliad.ogg]]
|-
!clark.ogg<wbr>{{only|je|short=1}}<br>calm2.ogg<wbr>{{only|be|short=1}}
|[[Survival]] {{in|java|bedrock}}, and [[Creative]] {{in|java}}
|"[[Clark]]"
|{{sort|A14|''[[Minecraft - Volume Alpha]]'' No. 14}}
|C418
|3:11
|[[File:Clark.ogg]]
|-
!comforting_memories.ogg
||[[Survival]] {{in|java|bedrock}}, and [[Creative]] {{in|java}}; further emphasized in [[Grove]]s.
|"[[Comforting Memories]]"
|{{sort|C09|''[[Minecraft: Caves & Cliffs (Original Game Soundtrack)]]'' No. 9}}
|Kumi Tanioka
|4:35
|[[File:Comforting memories.ogg]]
|-
!crescent_dunes.ogg
|[[Badlands]] and [[Desert]]
|"[[Crescent Dunes]]"
|{{sort|Tra04|''[[Minecraft: Trails & Tales (Original Game Soundtrack)]]'' No. 4}}
|Aaron Cherof
|4:08
|[[File:Crescent Dunes.ogg]]
|-
!danny.ogg<wbr>{{only|je|short=1}}<br>hal4.ogg<wbr>{{only|be|short=1}}
|[[Survival]] {{in|java|bedrock}}, and [[Creative]] {{in|java}}
|"[[Danny]]"
|{{sort|A21|''[[Minecraft - Volume Alpha]]'' No. 21}}
|C418
|4:14
|[[File:Danny.ogg]]
|-
!deeper.ogg
|[[Main Menu]], [[Deep Dark]], [[Dripstone Caves]]
|"[[Deeper]]"
|{{sort|Tri07|''[[Minecraft: Tricky Trials (Original Game Soundtrack)]]'' No. 7}}
|Lena Raine
|5:03
|[[File:Deeper.ogg]]
|-
!dreiton.ogg<wbr>{{only|je|short=1}}<br>creative5.ogg<wbr>{{only|be|short=1}}
|[[Creative]] mode
|"[[Dreiton]]"
|{{sort|B18|''[[Minecraft - Volume Beta]]'' No. 18}}
|C418
|8:16
|[[File:Dreiton.ogg]]
|-
!dry_hands.ogg<wbr>{{only|je|short=1}}<br>piano1.ogg<wbr>{{only|be|short=1}}
|[[Survival]] {{in|java|bedrock}}, and [[Creative]] {{in|java}}
|"[[Dry Hands]]"
|{{sort|A12|''[[Minecraft - Volume Alpha]]'' No. 12}}
|C418
|1:08
|[[File:Dry hands.ogg]]
|-
!echo_in_the_wind.ogg
|[[Badlands]], [[Cherry Grove]], [[Flower Forest]], and [[Lush Caves]]
|"[[Echo in the Wind]]"
|{{sort|Tra01|''[[Minecraft: Trails & Tales (Original Game Soundtrack)]]'' No. 1}}
|Aaron Cherof
|4:56
|[[File:Echo in the Wind.ogg]]
|-
!eld_unknown.ogg
|[[Main Menu]], [[Dripstone Caves]], [[Grove]], [[Jagged Peaks]], and [[Stony Peaks]]
|"[[Eld Unknown]]"
|{{sort|Tri08|''[[Minecraft: Tricky Trials (Original Game Soundtrack)]]'' No. 8}}
|Lena Raine
|4:56
|[[File:Eld Unknown.ogg]]
|-
!endless.ogg
|[[Main Menu]], [[Dripstone Caves]], [[Grove]], [[Jagged Peaks]], and [[Stony Peaks]]
|"[[Endless]]"
|{{sort|Tri09|''[[Minecraft: Tricky Trials (Original Game Soundtrack)]]'' No. 9}}
|Lena Raine
|6:42
|[[File:Endless.ogg]]
|-
!featherfall.ogg
|[[Survival]] {{in|java|bedrock}}, [[Creative]] {{in|java}}, and [[Main Menu]]; further emphasized in [[Badlands]], [[Cherry Grove|Cherry Grove]], [[Flower Forest|Flower Forests]], and [[Lush Caves]]
|"[[Featherfall]]"
|{{sort|Tri01|''[[Minecraft: Tricky Trials (Original Game Soundtrack)]]'' No. 1}}
|Aaron Cherof
|5:45
|[[File:Featherfall.ogg]]
|-
!firebugs.ogg
|[[Forest]], [[Old Growth Taiga]], [[Lush Caves]] and [[Swamp]]
|"[[Firebugs]]"
|{{sort|W01|''[[Minecraft: The Wild Update (Original Game Soundtrack)]]'' No. 1}}
|Lena Raine
|5:12
|[[File:Firebugs.ogg]]
|-
!fireflies.ogg
||[[Survival]] {{in|java|bedrock}}, [[Creative]] {{in|java}}, and [[Main Menu]]; further emphasized in [[Desert]]s.{{upcoming|java 1.21.6}}
|"[[Fireflies (song)|Fireflies]]"
|{{sort|25SD05|''[[Minecraft: Game Drop 2 - 2025 (Original Game Soundtrack)]]'' No. 5}}
|Amos Roddy
|2:35
|[[File:fireflies.ogg]]
|-
!floating_dream.ogg
|[[Survival]] {{in|java|bedrock}}, and [[Creative]] {{in|java}}; further emphasized in [[Jagged Peaks]] and [[Lush Caves]].
|"[[Floating Dream]]"
|{{sort|C08|''[[Minecraft: Caves & Cliffs (Original Game Soundtrack)]]'' No. 8}}
|Kumi Tanioka
|3:26
|[[File:Floating dream.ogg]]
|-
!haggstrom.ogg<wbr>{{only|je|short=1}}<br>hal3.ogg<wbr>{{only|be|short=1}}
|[[Survival]] {{in|java|bedrock}}, and [[Creative]] {{in|java}}
|"[[Haggstrom]]"
|{{sort|A07|''[[Minecraft - Volume Alpha]]'' No. 7}}
|C418
|3:24
|[[File:Haggstrom.ogg]]
|-
!haunt_muskie.ogg<wbr>{{only|je|short=1}}<br>creative3.ogg<wbr>{{only|be|short=1}}
|[[Creative]] mode
|"[[Haunt Muskie]]"
|{{sort|B10|''[[Minecraft - Volume Beta]]'' No. 10}}
|C418
|6:00
|[[File:Haunt muskie.ogg]]
|-
!infinite_amethyst.ogg
|[[Dripstone Caves]] and [[Grove]]
|"[[Infinite Amethyst]]"
|{{sort|C05|''[[Minecraft: Caves & Cliffs (Original Game Soundtrack)]]'' No. 5}}
|Lena Raine
|4:31
|[[File:Infinite amethyst.ogg]]
|-
!key.ogg<wbr>{{only|je|short=1}}<br>nuance1.ogg<wbr>{{only|be|short=1}}
|[[Survival]] {{in|java|bedrock}}, and [[Creative]] {{in|java}}
(Shortest track in the game)
|"[[Key (song)|Key]]"
|{{sort|A01|''[[Minecraft - Volume Alpha]]'' No. 1}}
|C418
|1:05
|[[File:Key.ogg]]
|-
!komorebi.ogg
|[[Survival]] {{in|java|bedrock}}, [[Creative]] {{in|java}}, and [[Main Menu]]
|"[[komorebi]]"
|{{sort|Tri04|''[[Minecraft: Tricky Trials (Original Game Soundtrack)]]'' No. 4}}
|Kumi Tanioka
|4:48
|[[File:Komorebi.ogg]]
|-
!labyrinthine.ogg
|[[Forest]], [[Old Growth Taiga]], [[Lush Caves]] and [[Swamp]]
|"[[Labyrinthine]]"
|{{sort|W03|''[[Minecraft: The Wild Update (Original Game Soundtrack)]]'' No. 3}}
|Lena Raine
|5:24
|[[File:Labyrinthine.ogg]]
|-
!left_to_bloom.ogg
|[[Survival]] {{in|java|bedrock}}, and [[Creative]] {{in|java}}; further emphasized in [[Meadow]]s and [[Lush Caves]].
|"[[Left to Bloom]]"
|{{sort|C02|''[[Minecraft: Caves & Cliffs (Original Game Soundtrack)]]'' No. 2}}
|Lena Raine
|5:42
|[[File:Left to bloom.ogg]]
|-
!lilypad.ogg
||[[Survival]] {{in|java|bedrock}}, [[Creative]] {{in|java}}, and [[Main Menu]]; further emphasized in [[Grove]]s and [[Frozen Peaks]].{{upcoming|java 1.21.6}}
|"[[Lilypad (song)|Lilypad]]"
|{{sort|25SD01|''[[Minecraft: Game Drop 2 - 2025 (Original Game Soundtrack)]]'' No. 1}}
|Amos Roddy
|3:55
|[[File:lilypad.ogg]]
|-
!living_mice.ogg<wbr>{{only|je|short=1}}<br>hal2.ogg<wbr>{{only|be|short=1}}
|[[Survival]] {{in|java|bedrock}}, and [[Creative]] {{in|java}}
|"[[Living Mice]]"
|{{sort|A05|''[[Minecraft - Volume Alpha]]'' No. 5}}
|C418
|2:57
|[[File:Living mice.ogg]]
|-
!mice_on_venus.ogg<wbr>{{only|je|short=1}}<br>piano3.ogg<wbr>{{only|be|short=1}}
|[[Survival]] {{in|java|bedrock}}, and [[Creative]] {{in|java}}
|"[[Mice on Venus]]"
|{{sort|A11|''[[Minecraft - Volume Alpha]]'' No. 11}}
|C418
|4:41
|[[File:Mice on venus.ogg]]
|-
!minecraft.ogg<wbr>{{only|je|short=1}}<br>calm1.ogg<wbr>{{only|be|short=1}}<
|[[Survival]] {{in|java|bedrock}}, and [[Creative]] {{in|java}}
|"[[Minecraft (song)|Minecraft]]"
|{{sort|A08|''[[Minecraft - Volume Alpha]]'' No. 8}}
|C418
|4:14
|[[File:Minecraft.ogg]]
|-
!one_more_day.ogg
|[[Survival]] {{in|java|bedrock}}, and [[Creative]] {{in|java}}; further emphasized in [[Meadow]]s, [[Snowy Slopes]], and [[Lush Caves]].
|"[[One More Day]]"
|{{sort|C06|''[[Minecraft: Caves & Cliffs (Original Game Soundtrack)]]'' No. 6}}
|Lena Raine
|4:38
|[[File:One more day.ogg]]
|-
!os_piano.ogg
||[[Survival]] {{in|java|bedrock}}, [[Creative]] {{in|java}}, and [[Main Menu]]; further emphasized in [[Lush Caves]].{{upcoming|java 1.21.6}}
|"[[O's Piano]]"
|{{sort|25SD03|''[[Minecraft: Game Drop 2 - 2025 (Original Game Soundtrack)]]'' No. 3}}
|Amos Roddy
|4:35
|[[File:O's Piano.ogg]]
|-
!oxygene.ogg<wbr>{{only|je|short=1}}<br>nuance2.ogg<wbr>{{only|be|short=1}}
|[[Survival]] {{in|java|bedrock}}, and [[Creative]] {{in|java}}
(Longer than "Key" by 125 ms)
|"[[Oxygène]]"
|{{sort|A09|''[[Minecraft - Volume Alpha]]'' No. 9}}
|C418
|1:05
|[[File:Oxygene.ogg]]
|-
!pokopoko.ogg
|[[Main Menu]], [[Dripstone Caves]], [[Grove]], [[Jagged Peaks]], and [[Snowy Slopes]]
|"[[pokopoko]]"
|{{sort|Tri05|''[[Minecraft: Tricky Trials (Original Game Soundtrack)]]'' No. 5}}
|Kumi Tanioka
|5:04
|[[File:Pokopoko.ogg]]
|-
!puzzlebox.ogg
|[[Survival]] {{in|java|bedrock}}, [[Creative]] {{in|java}}, and [[Main Menu]]
|"[[Puzzlebox]]"
|{{sort|Tri03|''[[Minecraft: Tricky Trials (Original Game Soundtrack)]]'' No. 3}}
|Aaron Cherof
|4:59
|[[File:Puzzlebox.ogg]]
|-
!stand_tall.ogg
|[[Frozen Peaks]], [[Jagged Peaks]], [[Snowy Slopes]], and [[Stony Peaks]]
|"[[Stand Tall]]"
|{{sort|C01|''[[Minecraft: Caves & Cliffs (Original Game Soundtrack)]]'' No. 1}}
|Lena Raine
|5:08
|[[File:Stand tall.ogg]]
|-
!subwoofer_lullaby.ogg<wbr>{{only|je|short=1}}<br>hal1.ogg<wbr>{{only|be|short=1}}<br>
|[[Survival]] {{in|java|bedrock}}, and [[Creative]] {{in|java}}
|"[[Subwoofer Lullaby]]"
|{{sort|A03|''[[Minecraft - Volume Alpha]]'' No. 3}}
|C418
|3:28
|[[File:Subwoofer lullaby.ogg]]
|-
!sweden.ogg<wbr>{{only|je|short=1}}<br>calm3.ogg<wbr>{{only|be|short=1}}
|[[Survival]] {{in|java|bedrock}}, and [[Creative]] {{in|java}}
|"[[Sweden]]"
|{{sort|A18|''[[Minecraft - Volume Alpha]]'' No. 18}}
|C418
|3:35
|[[File:Sweden.ogg]]
|-
!taswell.ogg<wbr>{{only|je|short=1}}<br>creative6.ogg<wbr>{{only|be|short=1}}
|[[Creative]] mode
|"[[Taswell]]"
|{{sort|B16|''[[Minecraft - Volume Beta]]'' No. 16}}
|C418
|8:34
|[[File:Taswell.ogg]]
|-
!watcher.ogg
|[[Survival]] {{in|java|bedrock}}, [[Creative]] {{in|java}}, and [[Main Menu]]
|"[[Watcher]]"
|{{sort|Tri02|''[[Minecraft: Tricky Trials (Original Game Soundtrack)]]'' No. 2}}
|Aaron Cherof
|5:32
|[[File:Watcher.ogg]]
|-
!wending.ogg
|[[Dripstone Caves]], [[Grove]], [[Jagged Peaks]], and [[Stony Peaks]]
|"[[Wending]]"
|{{sort|C04|''[[Minecraft: Caves & Cliffs (Original Game Soundtrack)]]'' No. 4}}
|Lena Raine
|5:14
|[[File:Wending.ogg]]
|-
!wet_hands.ogg<wbr>{{only|je|short=1}}<br>piano2.ogg<wbr>{{only|be|short=1}}
|[[Survival]] {{in|java|bedrock}}, and [[Creative]] {{in|java}}
|"[[Wet Hands]]"
|{{sort|A13|''[[Minecraft - Volume Alpha]]'' No. 13}}
|C418
|1:30
|[[File:Wet hands.ogg]]
|-
!yakusoku.ogg
|[[Survival]] {{in|java|bedrock}}, [[Creative]] {{in|java}}, and [[Main Menu]]
|"[[yakusoku]]"
|{{sort|Tri06|''[[Minecraft: Tricky Trials (Original Game Soundtrack)]]'' No. 6}}
|Kumi Tanioka
|4:31
|[[File:Yakusoku.ogg]]
|}
"""

row_delimiter = '''|-
'''
wikicode = mw.parse(text)
tables = wikicode.filter_tags(matches=lambda node: node.tag == 'table', recursive=False)

for table in tables:
    rows = mw.parse(table.contents).filter_tags(matches=lambda node: node.tag == 'tr', recursive=False)
    new_rows = []

    for row_index, row in enumerate(rows):
        cells = mw.parse(row.contents).filter_tags(matches=lambda node: node.tag in ["td", "th"], recursive=False)
        if len(cells) < 7:
            continue

        indices = [2, 4, 1, 3, 5, 6, 0]
        new_cells = [cells[i] for i in indices]
        

        new_rows.append("".join(str(cell) for cell in new_cells))

    # テーブルに再代入
    table.contents = "".join(str(row) + row_delimiter for row in new_rows)

# 結果をファイルに出力
with open('temp.txt', 'a', encoding='utf-8') as f:
    f.write(str(wikicode))