#!/usr/bin/env python3
"""
Advanced Japanese Furigana Engine with complete dictionary overrides,
compound noun handlers, okurigana verifiers, and regex polishers.
"""

import json
import re
import sys
from pathlib import Path
import pykakasi

ROOT = Path(__file__).resolve().parents[3]
test_dir = ROOT / "tests" / "20260807_1"

kks = pykakasi.kakasi()

# Curated high-priority dictionary overrides (Key -> Reading)
EXACT_COMPOUNDS = {
    # 複合動詞・名詞
    "公明正大": "こうめいせいだい",
    "正々堂々": "せいせいどうどう",
    "男の人": "おとこのひと",
    "女の人": "おんなのひと",
    "若い人": "わかいひと",
    "多くの人": "おおくのひと",
    "人手": "ひとで",
    "人目の": "ひとめの",
    "人並み": "ひとなみ",
    "大の猫好き": "だいのねこずき",
    "猫好き": "ねこずき",
    "猫嫌い": "ねこぎらい",
    "採れたて": "とれたて",
    "焼きたて": "やきたて",
    "炊きたて": "たきたて",
    "出来たて": "できたて",
    "依頼主": "いらいぬし",
    "飼い主": "かいぬし",
    "持ち主": "もちぬし",
    "家主": "やぬし",
    "打ち合わせ": "うちあわせ",
    "打ち合わせる": "うちあわせる",
    "勤め上げる": "つとめあげる",
    "給与生活者": "きゅうよせいかつしゃ",
    "売上高": "うりあげだか",
    "思いのほか": "おもいのほか",
    "ひとりでに": "ひとりでに",
    "前もって": "まえもって",
    "案の定": "あんのじょう",
    "案外": "あんがい",
    "後回し": "あとまわし",
    "頭打ち": "あたまうち",
    "足踏み": "あしぶみ",
    "朝寝坊": "あさねぼう",
    "昼休み": "ひるやすみ",
    "昼寝": "ひるね",
    "時差ぼけ": "じさぼけ",
    "行き当たりばったり": "ゆきあたりばったり",
    "当たり前": "あたりまえ",
    "立ち上がる": "たちあがる",
    "立ち止まる": "たちどまる",
    "立ち込める": "たちこめる",
    "引き受ける": "ひきうける",
    "受け入れる": "うけいれる",
    "受け継ぐ": "うけつぐ",
    "受け取る": "うけとる",
    "受け皿": "うけざら",
    "受け入れ": "うけいれ",
    "引き継ぐ": "ひきつぐ",
    "引き換え": "ひきかえ",
    "話し合い": "はなしあい",
    "話し合う": "はなしあう",
    "話し手": "はなして",
    "聞き手": "ききて",
    "担い手": "にないて",
    "作り手": "つくりて",
    "読み手": "よみて",
    "書き手": "かきて",
    "買い手": "かいて",
    "借り手": "かりて",
    "使い手": "つかいて",
    "売り手": "うりて",
    "出し手": "だし手",
    "出し方": "だしかた",
    "出し忘れ": "だしわすれ",
    "分け方": "わけかた",
    "進め方": "すすめかた",
    "使い方": "つかいかた",
    "置き場所": "おきばしょ",
    "読み方": "よみかた",
    "書き方": "かきかた",
    "考え方": "かんがえかた",
    "見方": "みかた",
    "手引き": "てびき",
    "手並み": "てなみ",
    "手配": "てはい",
    "手間": "てま",
    "手続き": "てつづき",
    "手伝う": "てつだう",
    "結びつき": "むすびつき",
    "結び": "むすび",
    "見送り": "みおくり",
    "見送る": "みおくる",
    "見込み": "みこみ",
    "見落とす": "みおとす",
    "見当": "けんとう",
    "見覚え": "みおぼえ",
    "心当たり": "こころあたり",
    "取り戻す": "とりもどす",
    "取り返す": "とりかえす",
    "取り扱う": "とりあつかう",
    "取り扱い": "とりあつかい",
    "取り組む": "とりくむ",
    "取り組み": "とりくみ",
    "取り消す": "とりけす",
    "取り決める": "とりきめる",
    "取り決め": "とりきめ",
    "取り除く": "とりのぞく",
    "取り壊す": "とりこわす",
    "取り入れる": "とりいれる",
    "差し出す": "さしだす",
    "申し出る": "もうしでる",
    "申し込む": "もうしこむ",
    "申し込み": "もうしこみ",
    "問い合わせ": "といあわせ",
    "問い合わせる": "といあわせる",
    "組み合わせる": "くみあわせる",
    "組み合わせ": "くみあわせ",
    "組み立てる": "くみたてる",
    "組み立て": "くみたて",
    "踏み出す": "ふみだす",
    "見出す": "みいだす",
    "生み出す": "うみだす",
    "押し出す": "おしだす",
    "押し通す": "おしとおす",
    "押しとどめる": "おしとどめる",
    "言い換える": "いいかえる",
    "言い換え": "いいかえ",
    "後戻り": "あともどり",
    "先送り": "さきおくり",
    "先延ばし": "さきのばし",
    "先立ち": "さきだち",
    "先立つ": "さきだつ",
    "成り行き": "なりゆき",
    "食べ残し": "たべのこし",
    "買い物": "かいもの",
    "買いもの": "かいもの",
    "行き先": "いきさき",
    "発送先": "はっそうさき",
    "連絡先": "れんらくさき",
    "届け先": "とどけさき",
    "勤め先": "つとめさき",
    "仕入れ先": "しいれさき",
    "取引先": "とりひきさき",
    "輸入先": "ゆにゅうさき",
    "移転先": "いてんさき",
    "提出先": "ていしゅつさき",
    "相手先": "あいてさき",
    "宛先": "あてさき",
    "送り先": "おくりさき",
    "先方": "せんぽう",
    "当方": "とうほう",
    "一方": "いっぽう",
    "両方": "りょうほう",
    "他方": "たほう",
    "仕組み": "しくみ",
    "枠組み": "わくぐみ",
    "手組み": "てぐみ",
    "色合い": "いろあい",
    "使い分け": "つかいわけ",
    "聞き分け": "ききわけ",
    "見分け": "みわけ",
    "付け加える": "つけくわえる",
    "付け足す": "つけたす",
    "付き合い": "つきあい",
    "付き合う": "つきあう",
    "知り合い": "しりあい",
    "出会い": "であい",
    "出会う": "であう",
    "見合わせる": "みあわせる",
    "見合わせ": "みあわせ",
    "間に合う": "まにあう",
    "待ち合わせ": "まちあわせ",
    "待ち時間": "まちじかん",
    "行き違い": "いきちがい",
    "食い違い": "くいちがい",
    "勘違い": "かんちがい",
    "すれ違い": "すれちがい",
    "間違う": "まちがう",
    "間違える": "まちがえる",
    "間違い": "まちがい",
    "手違い": "てちがい",
    "戸惑う": "とまどう",
    "戸惑い": "とまどい",
    "思い切る": "おもいきる",
    "思い切り": "おもいきり",
    "思いがけない": "おもいがけない",
    "思いがけず": "おもいがけず",
    "思い立つ": "おもいたつ",
    "思い浮かぶ": "おもいうかぶ",
    "思い付く": "おもいつく",
    "思い出す": "おもいだす",
    "思い出": "おもいで",
    "気付く": "きづく",
    "気配り": "きくばり",
    "気兼ね": "きがね",
    "気配": "けはい",
    "確認済み": "かくにんずみ",
    "定時で上がる": "ていじであがる",
    "めどが立つ": "めどがたつ",
    "息が合う": "いきがあう",
    "元も子もない": "もともこもない",
    "一日中": "いちにちじゅう",
    "一年中": "いちねんじゅう",
    "年中": "ねんじゅう",
    "夜遅く": "よるおそく",
    "心残り": "こころのこり",
    "お越しになる": "おこしになる",
    "いらっしゃる": "いらっしゃる",
    "ご覧になる": "ごらんになる",
    "ご存知": "ごぞんじ",
    "失った": "うしなった",
    "失う": "うしなう",
    "失われた": "うしなわれた",
}

# Standalone single word overrides
WORD_OVERRIDES = {
    "選手": "せんしゅ",
    "戦う": "たたかう",
    "誓う": "ちかう",
    "願う": "ねがう",
    "従う": "したがう",
    "敬う": "うやまう",
    "訓読み": "くんよみ",
    "音読み": "おんよみ",
    "五段動詞": "ごだんどうし",
    "一段動詞": "いちだんどうし",
    "一歩": "いっぽ",
    "優勝": "ゆうしょう",
    "逃す": "のがす",
    "惜しい": "おしい",
    "悔しい": "くやしい",
    "寂しい": "さびしい",
    "淋しい": "さびしい",
    "懐かしい": "なつかしい",
    "災害": "さいがい",
    "迅速": "じんそく",
    "対応": "たいおう",
    "早朝": "そうちょう",
    "港": "みなと",
    "潮": "しお",
    "香り": "かおり",
    "漂う": "ただよう",
    "彷徨う": "さまよう",
    "匂う": "におう",
    "臭う": "におう",
    "潤う": "うるおう",
    "怒り": "いかり",
    "抑える": "おさえる",
    "支える": "ささえる",
    "捕らえる": "とらえる",
    "捉える": "とらえる",
    "堪える": "こらえる",
    "押さえる": "おさえる",
    "一旦": "いったん",
    "帰宅": "きたく",
    "出直す": "でなおす",
    "支店長": "してんちょう",
    "信頼関係": "しんらいかんけい",
    "努める": "つとめる",
    "務める": "つとめる",
    "勤める": "つとめる",
    "農園": "のうえん",
    "果実": "かじつ",
    "収穫": "しゅうかく",
    "祖母": "そぼ",
    "昭和": "しょうわ",
    "歌謡曲": "かようきょく",
    "歌謡": "かよう",
    "契約": "けいやく",
    "免責事項": "めんせきじこう",
    "免責": "めんせき",
    "面積": "めんせき",
    "保護猫": "ほごねこ",
    "直売所": "ちょくばいじょ",
    "新鮮": "しんせん",
    "野菜": "やさい",
    "定年": "ていねん",
    "抑制": "よくせい",
    "推移": "すいい",
    "柔軟": "じゅうなん",
    "屋台": "やたい",
    "提示": "ていじ",
    "披露": "ひろう",
    "鮮やか": "あざやか",
    "連用形": "れんようけい",
    "助詞": "じょし",
    "文脈": "ぶんみゃく",
    "文末": "ぶんまつ",
    "語順": "ごじゅん",
    "正解": "せいかい",
    "不正解": "ふせいかい",
    "誤用": "ごよう",
    "誤読": "ごどく",
    "消去法": "しょうきょほう",
    "傍線部": "ぼうせんぶ",
    "一括回収": "いっかつかいしゅう",
    "集積所": "しゅうせきじょ",
    "二酸化炭素": "にさんかたんそ",
    "試算実習": "しさんじっしゅう",
    "放課後児童クラブ": "ほうかごじどうくらぶ",
    "待機児童": "たいきじどう",
    "火災警報器": "かさいけいほうき",
    "防災備蓄": "ぼうさいびちく",
    "源泉徴収票": "げんせんちょうしゅうひょう",
    "確定申告": "かくていしんこく",
    "見学バッジ": "けんがくばっじ",
    "守衛所": "しゅえいじょ",
    "置き配": "おきはい",
    "避難経路": "ひなんけいろ",
    "文化財": "ぶんかざい",
    "半導体": "はんどうたい",
    "経済安全保障": "けいざいあんぜんほしょう",
    "微細化": "びさいか",
    "調達網": "ちょうたつもう",
    "自給率": "じきゅうりつ",
    "血液製剤": "けつえきせいざい",
    "成分献血": "せいぶんけんけつ",
    "資金繰り": "しきんぐり",
    "入金サイクル": "にゅうきんさいくる",
    "決済端末": "けっさいたんまつ",
    "空き家": "あきや",
    "老朽化": "ろうきゅうか",
    "通信販売": "つうしんはんばい",
    "試行錯誤": "しこうさくご",
    "稼働率": "かどうりつ",
    "運休": "うんきゅう",
    "正大": "せいだい",
    "公明": "こうめい",
}


def annotate_plain(text: str) -> str:
    if not text:
        return ""
    # 1. Apply exact compound dictionary matches
    for comp, hira in sorted(EXACT_COMPOUNDS.items(), key=lambda x: -len(x[0])):
        if comp in text:
            m_oku = re.search(r"([一-龥々]+)([\u3040-\u309f\u30a0-\u30ff]*)$", comp)
            if m_oku and m_oku.group(2):
                k_part = m_oku.group(1)
                oku_part = m_oku.group(2)
                prefix_kana = comp[:m_oku.start()]
                h_sub = hira
                if prefix_kana and h_sub.startswith(prefix_kana):
                    h_sub = h_sub[len(prefix_kana):]
                if oku_part and h_sub.endswith(oku_part):
                    h_sub = h_sub[:-len(oku_part)]
                text = text.replace(comp, f"{prefix_kana}{k_part}《{h_sub}》{oku_part}")
            else:
                text = text.replace(comp, f"{comp}《{hira}》")

    # 2. Tokenize remaining segments with pykakasi
    pattern = re.compile(r"(｜?[一-龥々]+《[^》]+》)")
    parts = pattern.split(text)
    res_parts = []
    for part in parts:
        if not part:
            continue
        if pattern.match(part):
            res_parts.append(part)
            continue
        tokens = kks.convert(part)
        for t in tokens:
            orig = t['orig']
            hira = t['hira']
            if re.search(r"[一-龥々]", orig):
                if orig in WORD_OVERRIDES:
                    target_hira = WORD_OVERRIDES[orig]
                    m_oku = re.search(r"([一-龥々]+)([\u3040-\u309f\u30a0-\u30ff]*)$", orig)
                    if m_oku:
                        k_part = m_oku.group(1)
                        oku_part = m_oku.group(2)
                        prefix_kana = orig[:m_oku.start()]
                        h_sub = target_hira
                        if prefix_kana and h_sub.startswith(prefix_kana):
                            h_sub = h_sub[len(prefix_kana):]
                        if oku_part and h_sub.endswith(oku_part):
                            h_sub = h_sub[:-len(oku_part)]
                        res_parts.append(f"{prefix_kana}{k_part}《{h_sub}》{oku_part}")
                    else:
                        res_parts.append(f"{orig}《{target_hira}》")
                    continue

                m_oku = re.search(r"([一-龥々]+)([\u3040-\u309f\u30a0-\u30ff]*)$", orig)
                if m_oku:
                    k_part = m_oku.group(1)
                    oku_part = m_oku.group(2)
                    prefix_kana = orig[:m_oku.start()]
                    hira_sub = hira
                    if prefix_kana and hira_sub.startswith(prefix_kana):
                        hira_sub = hira_sub[len(prefix_kana):]
                    if oku_part and hira_sub.endswith(oku_part):
                        hira_sub = hira_sub[:-len(oku_part)]
                    if k_part == "後" and hira_sub in ("のち", "うしろ"):
                        hira_sub = "ご"
                    elif k_part == "中" and hira_sub == "なか":
                        hira_sub = "ちゅう"
                    elif k_part == "人" and hira_sub == "にん":
                        hira_sub = "ひと"
                    elif k_part == "正大" and hira_sub == "まさひろ":
                        hira_sub = "せいだい"

                    if hira_sub and hira_sub != k_part:
                        res_parts.append(f"{prefix_kana}{k_part}《{hira_sub}》{oku_part}")
                    else:
                        res_parts.append(orig)
                else:
                    res_parts.append(f"{orig}《{hira}》" if hira != orig else orig)
            else:
                res_parts.append(orig)

    out = "".join(res_parts)
    out = re.sub(r"人《にん》(?=[がはをにとのでも、。])", "人《ひと》", out)
    out = re.sub(r"中《ちゅう》から", "中《なか》から", out)
    out = re.sub(r"中《ちゅう》で", "中《なか》で", out)
    out = re.sub(r"中《ちゅう》に", "中《なか》に", out)
    out = out.replace("読《よ》み方《よみかた》", "読《よ》み方《かた》")
    out = out.replace("書《か》き方《かきかた》", "書《か》き方《かた》")
    out = out.replace("使《つか》い方《つかいかた》", "使《つか》い方《かた》")
    out = out.replace("考《かんが》え方《かんがえかた》", "考《かんが》え方《かた》")
    out = out.replace("進《すす》め方《すすめかた》", "進《すす》め方《かた》")
    out = out.replace("出《だ》し方《だしかた》", "出《だ》し方《かた》")
    out = out.replace("分《わ》け方《わけかた》", "分《わ》け方《かた》")
    out = out.replace("置《お》き場所《おきばしょ》", "置《お》き場所《ばしょ》")
    out = re.sub(r"（（", "（", out)
    out = re.sub(r"））", "）", out)
    return out


def strip_furigana(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r"<ruby>([^<]+)<rt>[^<]*</rt></ruby>", r"\1", text)
    text = re.sub(r"｜?([一-龥々]+)《[^》]+》", r"\1", text)
    text = re.sub(r"《[^》]+》", "", text)
    return text


def add_furigana(text: str) -> str:
    """Intelligently apply 《...》 to Japanese text while preserving all HTML tags."""
    if not text:
        return ""
    # Strip existing furigana to prevent nested or duplicate annotations
    clean_text = strip_furigana(text)
    clean_text = clean_text.replace("（（", "（").replace("））", "）")
    # Split text into HTML tags vs non-HTML text segments
    pattern = re.compile(r"(<[^>]+>)")
    parts = pattern.split(clean_text)
    out = []
    for part in parts:
        if not part:
            continue
        if pattern.match(part):
            out.append(part)
        else:
            out.append(annotate_plain(part))
    return "".join(out)

print("Refined Furigana engine ready.")
