import win32com.client

# ソース [1] に基づく顧客リスト
""" customers = [
    {
        "company": "中和羊毛工業株式会社",
        "range": "中和ゴルフクラブ　シーダーパーク",
        "position": "総務部　総務課　係長",
        "name": "山田亮司",
        "sir": "様",
        "address": "r-yamada@cedarpark.jp"
    },
    {
        "company": "株式会社興産",
        "range": "芙蓉ゴルフガーデン",
        "position": "代表取締役",
        "name": "髙村康介",
        "sir": "様",
        "address": "fuyougolf-486@yahoo.co.jp"
    }
] """


customers = [
    # ソース より
    {
        "company": "中和羊毛工業株式会社",
        "range": "中和ゴルフクラブ　シーダーパーク",
        "position": "総務部　総務課　係長",
        "name": "山田亮司",
        "sir": "様",
        "mail": "r-yamada@cedarpark.jp"
    },
    {
        "company": "中和羊毛工業株式会社",
        "range": "中和ゴルフクラブ　シーダーパーク",
        "position": "代表取締役",
        "name": "奥村健",
        "sir": "様",
        "mail": "k-okumura@cedarpark.jp"
    },
    {
        "company": "株式会社興産",
        "range": "芙蓉ゴルフガーデン",
        "position": "代表取締役",
        "name": "髙村康介",
        "sir": "様",
        "mail": "fuyougolf-486@yahoo.co.jp"
    },
    {
        "company": "株式会社 観音山ゴルフ倶楽部",
        "range": "観音山ゴルフ倶楽部",
        "position": "代表取締役",
        "name": "染谷朋幸",
        "sir": "様",
        "mail": "tc22@kannonyama-golf.com"
    },
    {
        "company": "満別ゴルフコース(兼）上士幌ゴルフ場",
        "range": "",
        "position": "支配人",
        "name": "前田 昇",
        "sir": "様",
        "mail": "noboru.maeda@seibugroup.jp"
    },
    {
        "company": "青森ゴルフ観光株式会社",
        "range": "青森カントリー倶楽部",
        "position": "アドバイザー",
        "name": "岸田歩",
        "sir": "様",
        "mail": "hishikawa@kiwasangyo.co.jp"
    },
    {
        "company": "有限会社広島スポーツセンター",
        "range": "舟入ゴルフガーデン",
        "position": "取締役 支配人",
        "name": "中山一郎",
        "sir": "様",
        "mail": "funairi-gg@green.megaegg.ne.jp"
    },
    {
        "company": "有限会社ヒカリ",
        "range": "Green Forum Tobiuo",
        "position": "スタッフ",
        "name": "倉島修（くらしまおさむ）",
        "sir": "様",
        "mail": "info@tobiuo.shop"
    },
    # ソース より
    {
        "company": "ボールパーク",
        "range": "",
        "position": "支配人",
        "name": "澤智樹",
        "sir": "様",
        "mail": "ballpark-golf@drive.ocn.ne.jp"
    },
    {
        "company": "厚木ゴルフプラザ",
        "range": "厚木ゴルフプラザ",
        "position": "代表取締役 専務",
        "name": "森山浩二",
        "sir": "様",
        "mail": "k.moriyama@atsugi-golfplaza.com"
    },
    {
        "company": "株式会社サクラゴルフガーデン",
        "range": "サクラゴルフガーデン",
        "position": "代表取締役",
        "name": "相原金悦",
        "sir": "様",
        "mail": "aikin@sgg-akita.co.jp"
    },
    {
        "company": "株式会社田無ファミリーランド",
        "range": "タイムジップス24",
        "position": "業務部 部長代理",
        "name": "中田和光",
        "sir": "様",
        "mail": "nakada@tfl.co.jp"
    },
    {
        "company": "株式会社田無ファミリーランド",
        "range": "タイムジップス24",
        "position": "情報システム室 室長／システムエンジニア",
        "name": "斎賀重陽",
        "sir": "様",
        "mail": "saiga@tfl.co.jp"
    },
    {
        "company": "株式会社田無ファミリーランド",
        "range": "タイムジップス24",
        "position": "代表取締役",
        "name": "石津幸裕",
        "sir": "様",
        "mail": "ishizu@tfl.co.jp"
    },
    {
        "company": "ウッドヒルゴルフクラブ",
        "range": "",
        "position": "取締役",
        "name": "鈴木伸幸",
        "sir": "様",
        "mail": "ballondor@s5.dion.ne.jp"
    },
    {
        "company": "有限会社ヒカリ",
        "range": "Green Forum Tobiuo",
        "position": "常務",
        "name": "前島信広",
        "sir": "様",
        "mail": "hishikawa@kiwasangyo.co.jp"
    },
    {
        "company": "大扇株式会社",
        "range": "名古屋ウエストゴルフクラブ",
        "position": "専務取締役",
        "name": "伊藤宏真",
        "sir": "様",
        "mail": "hiro@west-golf.co.jp"
    },
    # ソース より
    {
        "company": "大扇株式会社",
        "range": "名古屋ウエストゴルフクラブ",
        "position": "代表取締役社長",
        "name": "伊藤嘉邦",
        "sir": "様",
        "mail": "yk@ito18.com"
    },
    {
        "company": "ヨネックスゴルフ練習場",
        "range": "",
        "position": "",
        "name": "杉本誠",
        "sir": "様",
        "mail": "hishikawa@kiwasangyo.co.jp"
    },
    {
        "company": "ARIAKEゴルフガーデン㈱",
        "range": "ARIAKEゴルフガーデン",
        "position": "代表取締役",
        "name": "沖田良三",
        "sir": "様",
        "mail": "hishikawa@kiwasangyo.co.jp"
    },
    {
        "company": "書写グリーン倶楽部",
        "range": "書写グリーン倶楽部",
        "position": "マネージャー",
        "name": "鳥居秀樹",
        "sir": "様",
        "mail": "torii@mitsuwa-g.co.jp"
    },
    {
        "company": "株式会社掛川ゴルフガーデン",
        "range": "掛川ゴルフガーデン",
        "position": "",
        "name": "深津一仁",
        "sir": "様",
        "mail": "kgg@taiho-group.com"
    },
    {
        "company": "有限会社青山商会",
        "range": "青山グリーンゴルフ",
        "position": "代表取締役",
        "name": "田村恭子",
        "sir": "様",
        "mail": "kyoko_tamura_golf@outlook.jp"
    },
    {
        "company": "株式会社ダイ二チ工機",
        "range": "",
        "position": "",
        "name": "新川哲則",
        "sir": "様",
        "mail": "dainichikouki@mocha.ocn.ne.jp"
    },
    {
        "company": "株式会社平川商事",
        "range": "",
        "position": "ゴルフ事業部マネージャー",
        "name": "向井清隆",
        "sir": "様",
        "mail": "k.mukai@hirakawa-corp.com"
    },
    {
        "company": "株式会社ナガノ",
        "range": "",
        "position": "代表取締役社長",
        "name": "長野利八",
        "sir": "様",
        "mail": "toshiya@nagano-golf.co.jp"
    },
    {
        "company": "株式会社ナガノ",
        "range": "",
        "position": "",
        "name": "植村龍太郎",
        "sir": "様",
        "mail": "uemura@nagano-golf.co.jp"
    },
    # ソース より
    {
        "company": "株式会社金久保",
        "range": "",
        "position": "営業部",
        "name": "東方一毅",
        "sir": "様",
        "mail": "kanekubo@mx1.ttcn.ne.jp"
    },
    {
        "company": "有限会社フタバ",
        "range": "ジャンボゴルフクラブ",
        "position": "専務取締役",
        "name": "申 崇寛",
        "sir": "様",
        "mail": "sin-jumbogolf@sinclover.com"
    },
    {
        "company": "株式会社岩崎電気",
        "range": "",
        "position": "首都圏営業部 首都圏第六営業課 課長",
        "name": "小菅昇",
        "sir": "様",
        "mail": "kosuge-noboru@eye.co.jp"
    },
    {
        "company": "有限会社鶴岡ゴルフガーデン",
        "range": "鶴岡ゴルフガーデン",
        "position": "代表取締役",
        "name": "朴文秀",
        "sir": "様",
        "mail": "moonsoo.park@kihoshoji.com"
    },
    {
        "company": "浜北ゴルフガーデン",
        "range": "",
        "position": "支配人",
        "name": "澤木賢也",
        "sir": "様",
        "mail": "hishikawa@kiwasangyo.co.jp"
    },
    {
        "company": "株式会社山田クラブ21",
        "range": "山田ゴルフ倶楽部",
        "position": "支配人",
        "name": "板倉千成",
        "sir": "様",
        "mail": "hishikawa@kiwasangyo.co.jp"
    },
    {
        "company": "ひかり産業株式会社",
        "range": "ひかりGOLF PARK",
        "position": "課長",
        "name": "石井慎一",
        "sir": "様",
        "mail": "s_ishii_s@hikarisangyo.co.jp"
    },
    {
        "company": "公益法人三菱養和会",
        "range": "",
        "position": "第一事業部 ゴルフ練習場",
        "name": "皆川瑳菜",
        "sir": "様",
        "mail": "s.minagawa@yowa.or.jp"
    },
    {
        "company": "東産業株式会社",
        "range": "東洋ゴルフクラブ",
        "position": "支配人",
        "name": "吉畑英樹",
        "sir": "様",
        "mail": "yoshihata@toyo-golf.co.jp"
    },
    # ソース より
    {
        "company": "東産業株式会社",
        "range": "東洋ゴルフクラブ",
        "position": "総務部長",
        "name": "荒沢公司",
        "sir": "様",
        "mail": "arasawa@toyo-golf.co.jp"
    },
    {
        "company": "株式会社エム・エス・ケイゴルフ",
        "range": "トピックゴルフ",
        "position": "マネージャー",
        "name": "松本俊介",
        "sir": "様",
        "mail": "s_matsumoto@topic-golf.yokohama"
    },
    {
        "company": "有限会社三井産業",
        "range": "",
        "position": "総務部長",
        "name": "俵 亘",
        "sir": "様",
        "mail": "tawataru47.tgc@gmail.com"
    },
    {
        "company": "株式会社Atlaz",
        "range": "",
        "position": "取締役",
        "name": "高橋正直",
        "sir": "様",
        "mail": "takahashi@atlaz.co.jp"
    },
    {
        "company": "株式会社CIS",
        "range": "Central Ise Shima ブルーグラス大山田 ブルーグラスクレア",
        "position": "総支配人",
        "name": "空正純",
        "sir": "様",
        "mail": "sora@cis-gr.com"
    },
    {
        "company": "ロッテ不動産株式会社",
        "range": "皆吉台カントリー倶楽部",
        "position": "運営課 キャディ係 主任",
        "name": "中村智津子",
        "sir": "様",
        "mail": "hishikawa@kiwasangyo.co.jp"
    },
    {
        "company": "長津田ゴルフガーデン",
        "range": "",
        "position": "支配人 日本プロゴルフ協会ティーチングプロB級会員",
        "name": "梅村孝之",
        "sir": "様",
        "mail": "takayuki.umemura@tfn-style.jp"
    },
    {
        "company": "株式会社アクト",
        "range": "",
        "position": "営業部",
        "name": "山崎 宏一",
        "sir": "様",
        "mail": "k-yamazaki.act06@bc.wakwak.com"
    },
    {
        "company": "株式会社アクト",
        "range": "",
        "position": "営業部",
        "name": "大窪淳",
        "sir": "様",
        "mail": "act@au.wakwak.com"
    },
    # ソース より
    {
        "company": "株式会社ティータイム",
        "range": "",
        "position": "ゴルフ事業部リーダー",
        "name": "山田大輔",
        "sir": "様",
        "mail": "daisuke.yamada@teetime.co.jp"
    },
    {
        "company": "オリエントオリンピア産業株式会社",
        "range": "山の手ゴルフセンター",
        "position": "取締役 支配人",
        "name": "中村淳司",
        "sir": "様",
        "mail": "nakamura@yamanotegolf-drivingrange.club"
    },
    {
        "company": "株式会社六ツ川台ゴルフ練習場",
        "range": "六ツ川台ゴルフガーデン",
        "position": "主任",
        "name": "坂本淳也",
        "sir": "様",
        "mail": "golf_range@mutsukawadai.jp"
    },
    {
        "company": "株式会社スズコー",
        "range": "",
        "position": "",
        "name": "鈴木晴澄",
        "sir": "様",
        "mail": "hishikawa@kiwasangyo.co.jp"
    },
    {
        "company": "株式会社スズコー",
        "range": "スズコーゴルフ",
        "position": "支配人",
        "name": "笹崎彰利",
        "sir": "様",
        "mail": "a.sasazaki@suzukoh-golf.com"
    }
]
# ソース [2] に基づくメール本文（body5以降）
main_text = """いつもお世話になっております
この度は「ゴルフフェア 2026」弊社ブースにお立ち寄りいただきありがとうございます
今年も無事に出展を終えることができました
これもひとえに弊社をお引き立ていただいているお客様のお力添えと感謝いたしております \n
出展品の中に気になった製品はございましたでしょうか
是非改めてこれら商品のご紹介にあがりたく、ご多忙とは存じますがお時間を頂戴
できますと幸甚にそんじます
改めて担当の者から連絡させていただきますので、何卒よろしくお願いいたします \n
最後になりましたがお客様のご繁栄とご健康を祈念いたしまして
ご来場御礼の挨拶とさせていただきます
今後とも相変わらずのご高配何卒お願い申し上げます \n
                                                                                                      喜和産業株式会社
                                                                                                      代表取締役
                                                                                                      安岡 進一郎"""

def send_outlook_emails():
    # Outlookアプリケーションの起動
    outlook = win32com.client.Dispatch("Outlook.Application")

    for customer in customers:
        # 新しいメールアイテムの作成
        mail = outlook.CreateItem(0)
        
        # メールの設定
        mail.To = customer["mail"] # 送信先 [1]
        mail.Subject = "「ゴルフフェア2026」ご来場御礼のご挨拶" # 指定の件名
        mail.bcc = "shinichiro@kiwasangyo.co.jp;yuuki@kiwasangyo.co.jp"
        
        # 送信元の設定 (権限がある場合のみ有効)
        mail.SentOnBehalfOfName = "hishikawa@kiwasangyo.co.jp"

        # 指定されたフォーマットで本文を構築
        # body1: company, body2: range, body3: position, body4: name + sir
        # その後、2行の空白行を空けて本文を結合
        header = (
            f"{customer['company']}\n"
            f"{customer['range']}\n"
            f"{customer['position']}\n"
            f"{customer['name']} {customer['sir']}\n\n\n"
        )
        
        mail.Body = header + main_text # ヘッダーとソース [2] の本文を結合

        # メールの表示（自動送信する場合は mail.Send() に変更してください）
        print(f"{customer['company'] + customer['name'] + customer['mail']} 様宛のメールを作成しました。")
        input_update = input('送信していいですか(y or n):') 
        if input_update == 'y':
            print('送信する場合は送信ボタンをクリックしてください')
            mail.Display(True)


if __name__ == "__main__":
    send_outlook_emails()