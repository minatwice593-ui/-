import pandas as pd
from pathlib import Path
from flask import Flask, request, render_template_string

app = Flask(__name__)
CSV_PATH = Path(__file__).with_name("korean_dictionary_template.csv")
COLUMNS = ["單字編號", "韓文單字", "漢字詞", "發音(羅馬拼音)", "詞性", "TOPIK等級", "中文釋義", "韓文例句", "例句中文翻譯", "常用搭配/備註"]

HTML_TEMPLATE = """<!doctype html>
<html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>韓文字典查詢系統</title><style>
body{font-family:system-ui,'Noto Sans TC',sans-serif;background:#f7f9fc;color:#1e293b;margin:0;padding:24px}.container{max-width:960px;margin:auto}h1{text-align:center;color:#0f172a}.search,.card,.empty{background:white;border:1px solid #e2e8f0;border-radius:12px;padding:18px;margin-bottom:16px}.search form{display:grid;grid-template-columns:2fr 1fr 1fr auto;gap:10px}input,select,button{padding:10px;border:1px solid #cbd5e1;border-radius:8px;font-size:14px}button{background:#3b82f6;color:white;border:0;cursor:pointer}.meta,.sub{color:#64748b}.head{display:flex;align-items:center;gap:12px;flex-wrap:wrap}.term{font-size:1.5rem;font-weight:700}.badge{background:#eff6ff;color:#1d4ed8;padding:3px 8px;border-radius:6px;font-size:12px}.meaning{font-size:1.1rem;font-weight:600;margin:12px 0}.example{background:#f8fafc;border-left:3px solid #3b82f6;padding:10px 14px}.notes{margin-top:10px;color:#64748b;font-size:13px}.empty{text-align:center;color:#64748b;padding:40px}@media(max-width:700px){.search form{grid-template-columns:1fr}}
</style></head><body><main class="container"><h1>韓文字典查詢系統</h1>
<section class="search"><form method="get"><input name="q" placeholder="韓文、中文、羅馬拼音或漢字詞" value="{{ query }}">
<select name="level"><option value="">全部 TOPIK 等級</option>{% for x in all_levels %}<option value="{{ x }}" {% if selected_level == x %}selected{% endif %}>{{ x }}</option>{% endfor %}</select>
<select name="pos"><option value="">全部詞性</option>{% for x in all_pos %}<option value="{{ x }}" {% if selected_pos == x %}selected{% endif %}>{{ x }}</option>{% endfor %}</select><button>搜尋</button></form></section>
<p class="meta">共找到 <strong>{{ records|length }}</strong> 個詞條</p>
{% for item in records %}<article class="card"><div class="head"><span class="term">{{ item['韓文單字'] }}</span>{% if item['漢字詞'] %}<span class="sub">({{ item['漢字詞'] }})</span>{% endif %}<span class="sub">[{{ item['發音(羅馬拼音)'] }}]</span><span class="badge">{{ item['詞性'] }}</span>{% if item['TOPIK等級'] %}<span class="badge">{{ item['TOPIK等級'] }}</span>{% endif %}</div>
<div class="meaning">{{ item['中文釋義'] }}</div>{% if item['韓文例句'] %}<div class="example"><div>{{ item['韓文例句'] }}</div><div class="sub">{{ item['例句中文翻譯'] }}</div></div>{% endif %}{% if item['常用搭配/備註'] %}<div class="notes"><strong>補充：</strong>{{ item['常用搭配/備註'] }}</div>{% endif %}</article>
{% else %}<div class="empty">未找到符合條件的單字，請嘗試更換搜尋條件。</div>{% endfor %}</main></body></html>"""

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



