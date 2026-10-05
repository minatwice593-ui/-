import pandas as pd
from pathlib import Path
from flask import Flask, request, render_template_string

app = Flask(__name__)
CSV_PATH = Path(__file__).with_name("korean_dictionary_template.csv")
COLUMNS = ["單字編號", "韓文單字", "漢字詞", "發音(羅馬拼音)", "詞性", "TOPIK等級", "中文釋義", "韓文例句", "例句中文翻譯", "常用搭配/備註"]

HTML_TEMPLATE = """<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#0047A0">
<title>韓文字典｜Korean Vocabulary</title>
<style>
:root{color-scheme:light;--red:#CD2E3A;--red-soft:#FFF0F1;--blue:#0047A0;--blue-soft:#EDF4FF;--ink:#17191D;--muted:#68717D;--line:#E5E8ED;--paper:#FFFFFF;--bg:#F5F7FA}
*{box-sizing:border-box}
body{margin:0;background:radial-gradient(ellipse at 12% 0%,rgba(205,46,58,.08),transparent 28rem),radial-gradient(ellipse at 90% 6%,rgba(0,71,160,.09),transparent 30rem),var(--bg);color:var(--ink);font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans TC",sans-serif;min-height:100vh}
.container{width:min(960px,100% - 36px);margin:0 auto;padding:48px 0 64px}
.hero{text-align:center;margin-bottom:30px}
.brand{display:flex;align-items:center;justify-content:center;gap:13px}
.taegeuk{width:42px;height:42px;display:inline-block;border-radius:50%;position:relative;overflow:hidden;background:conic-gradient(from 90deg,var(--red) 0deg 180deg,var(--blue) 180deg 360deg);box-shadow:0 3px 10px rgba(20,35,60,.14)}
.taegeuk:before,.taegeuk:after{content:"";position:absolute;left:25%;width:50%;height:50%;border-radius:50%}
.taegeuk:before{top:0;background:var(--blue)}
.taegeuk:after{bottom:0;background:var(--red)}
.brand-copy{text-align:left}
.eyebrow{margin:0 0 3px;font-size:11px;font-weight:800;letter-spacing:.16em;color:var(--blue);text-transform:uppercase}
h1{font-size:clamp(30px,5vw,43px);letter-spacing:-.04em;margin:0;line-height:1.15}
.hero-copy{color:var(--muted);font-size:15px;margin:14px 0 0}
.color-rule{width:70px;height:5px;border-radius:5px;margin:20px auto 0;background:linear-gradient(90deg,var(--red) 0 50%,var(--blue) 50%)}
.search-card{background:var(--paper);border:1px solid var(--line);border-top:3px solid transparent;border-image:linear-gradient(90deg,var(--red) 0 50%,var(--blue) 50%) 1;border-radius:15px;padding:21px;box-shadow:0 12px 32px rgba(20,35,60,.055);margin-bottom:23px}
.search-title{font-weight:750;font-size:15px;margin:0 0 13px}
.search-form{display:grid;grid-template-columns:minmax(200px,2fr) minmax(145px,1fr) minmax(130px,.9fr) auto;gap:10px}
input,select,button{font:inherit;min-width:0;border-radius:9px}
input,select{width:100%;padding:12px 13px;border:1px solid var(--line);background:#fff;color:var(--ink);outline:none}
input::placeholder{color:#9299A3}
input:focus,select:focus{border-color:var(--blue);box-shadow:0 0 0 3px rgba(0,71,160,.12)}
button{border:0;padding:0 21px;background:var(--blue);color:#fff;font-weight:700;cursor:pointer;transition:background .18s,transform .18s}
button:hover{background:var(--red);transform:translateY(-1px)}
.results-head{display:flex;justify-content:space-between;align-items:center;margin:0 2px 13px;color:var(--muted);font-size:14px}
.count{font-size:16px;color:var(--ink)}
.word-card{background:var(--paper);border:1px solid var(--line);border-radius:13px;padding:19px 21px;margin-bottom:12px;box-shadow:0 4px 16px rgba(20,35,60,.035);transition:border-color .18s,transform .18s}
.word-card:hover{border-color:#B7C9E3;transform:translateY(-1px)}
.word-head{display:flex;align-items:center;gap:9px;flex-wrap:wrap}
.term{font-size:25px;line-height:1.2;font-weight:800;letter-spacing:-.025em}
.hanja,.roman{color:var(--muted);font-size:14px}
.roman{font-style:italic}
.badge{border-radius:99px;padding:4px 9px;font-size:11px;font-weight:750;white-space:nowrap}
.badge-pos{background:var(--red-soft);color:#9D1F2B}
.badge-level{background:var(--blue-soft);color:#003B84}
.meaning{font-weight:700;font-size:17px;margin:12px 0 11px}
.example{background:#F8FAFC;border-left:3px solid var(--blue);border-radius:0 9px 9px 0;padding:11px 13px}
.example-kr{font-size:15px;font-weight:600}
.example-zh{font-size:13px;color:var(--muted);margin-top:4px}
.notes{font-size:12px;color:var(--muted);margin-top:10px}
.notes strong{color:var(--red);margin-right:5px}
.empty{text-align:center;color:var(--muted);background:#fff;border:1px dashed #C9D0DA;border-radius:13px;padding:42px 20px}
.footer{text-align:center;color:#89919C;font-size:12px;margin-top:28px}
@media(max-width:700px){.container{width:min(100% - 24px,600px);padding-top:30px}.search-form{grid-template-columns:1fr 1fr}.search-form input{grid-column:1/-1}.search-form button{min-height:44px}.word-card{padding:16px}.term{font-size:23px}}
@media(max-width:420px){.search-form{grid-template-columns:1fr}.search-form input{grid-column:auto}.brand{gap:10px}.taegeuk{width:36px;height:36px}.eyebrow{font-size:9px}}
</style>
</head>
<body>
<main class="container">
<header class="hero">
<div class="brand"><span class="taegeuk" aria-hidden="true"></span><div class="brand-copy"><p class="eyebrow">Korean Vocabulary</p><h1>韓文字典</h1></div></div>
<p class="hero-copy">從日常用語開始，慢慢累積你的韓語詞彙。</p><div class="color-rule" aria-hidden="true"></div>
</header>
<section class="search-card">
<p class="search-title">搜尋詞彙</p>
<form method="get" class="search-form">
<input name="q" aria-label="關鍵字" placeholder="韓文、中文、羅馬拼音或漢字詞" value="{{ query }}">
<select name="level" aria-label="TOPIK 等級"><option value="">全部 TOPIK 等級</option>{% for x in all_levels %}<option value="{{ x }}" {% if selected_level == x %}selected{% endif %}>{{ x }}</option>{% endfor %}</select>
<select name="pos" aria-label="詞性"><option value="">全部詞性</option>{% for x in all_pos %}<option value="{{ x }}" {% if selected_pos == x %}selected{% endif %}>{{ x }}</option>{% endfor %}</select>
<button type="submit">搜尋</button>
</form>
</section>
<div class="results-head"><span>搜尋結果</span><span class="count">共 <strong>{{ records|length }}</strong> 個詞條</span></div>
{% for item in records %}
<article class="word-card">
<div class="word-head"><span class="term">{{ item['韓文單字'] }}</span>{% if item['漢字詞'] %}<span class="hanja">({{ item['漢字詞'] }})</span>{% endif %}<span class="roman">[{{ item['發音(羅馬拼音)'] }}]</span><span class="badge badge-pos">{{ item['詞性'] }}</span>{% if item['TOPIK等級'] %}<span class="badge badge-level">{{ item['TOPIK等級'] }}</span>{% endif %}</div>
<div class="meaning">{{ item['中文釋義'] }}</div>
{% if item['韓文例句'] %}<div class="example"><div class="example-kr">{{ item['韓文例句'] }}</div><div class="example-zh">{{ item['例句中文翻譯'] }}</div></div>{% endif %}
{% if item['常用搭配/備註'] %}<div class="notes"><strong>補充</strong>{{ item['常用搭配/備註'] }}</div>{% endif %}
</article>
{% else %}<div class="empty">沒有找到符合條件的詞彙，請試試其他搜尋字詞或篩選條件。</div>{% endfor %}
<footer class="footer">韓國國旗靈感配色 · 韓語入門詞彙</footer>
</main>
</body></html>"""

def load_data():
    if not CSV_PATH.exists():
        return pd.DataFrame(columns=COLUMNS)
    return pd.read_csv(CSV_PATH, encoding="utf-8-sig").reindex(columns=COLUMNS).fillna("")

@app.route("/")
def index():
    df = load_data()
    query = request.args.get("q", "").strip()
    selected_level = request.args.get("level", "").strip()
    selected_pos = request.args.get("pos", "").strip()
    all_levels = sorted(v for v in df["TOPIK等級"].unique() if str(v).strip())
    all_pos = sorted(v for v in df["詞性"].unique() if str(v).strip())
    filtered = df
    if query:
        fields = ["韓文單字", "中文釋義", "發音(羅馬拼音)", "漢字詞"]
        mask = pd.Series(False, index=filtered.index)
        for field in fields:
            mask |= filtered[field].astype(str).str.contains(query, case=False, regex=False, na=False)
        filtered = filtered[mask]
    if selected_level:
        filtered = filtered[filtered["TOPIK等級"].astype(str) == selected_level]
    if selected_pos:
        filtered = filtered[filtered["詞性"].astype(str) == selected_pos]
    return render_template_string(HTML_TEMPLATE, records=filtered.to_dict(orient="records"), query=query,
        selected_level=selected_level, selected_pos=selected_pos, all_levels=all_levels, all_pos=all_pos)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
