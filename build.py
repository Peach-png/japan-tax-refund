#!/usr/bin/env python3
"""Builds the static site into ./site from data/*.json and the translations below.
Run: python3 build.py
"""
import json, os, html, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "site")
SITE_URL = "https://peach-png.github.io/japan-tax-refund"

stores = json.load(open(os.path.join(ROOT, "data/stores.json"), encoding="utf-8"))
links = json.load(open(os.path.join(ROOT, "data/links.json"), encoding="utf-8"))

LANGS = {
"en": {
  "path": "", "html_lang": "en", "name": "English",
  "title": "Japan Tax Refund Calculator 2026 – New Refund System Explained",
  "desc": "Since 1 Nov 2026 you pay Japan's 10% tax up front and claim it back at the airport. Calculate your refund after store fees, check the 90-day deadline, and follow the airport steps.",
  "h1": "Japan tax refund calculator",
  "lead": "Since <b>1 November 2026</b>, tourists in Japan pay the full price including tax, then get the tax back at the airport. Work out how much you'll actually receive.",
  "calc_h": "Your purchases",
  "store": "Store", "paid": "Amount paid (¥, incl. tax)", "type": "Item type", "fee": "Refund fee %", "date": "Purchase date",
  "std": "General goods (10%)", "food": "Food & drinks (8%)",
  "add": "+ Add another store", "remove": "Remove",
  "res_tax": "Tax paid", "res_fee": "Fees", "res_refund": "You get back", "res_deadline": "Last day to leave Japan for a refund",
  "not_eligible": "Below ¥5,000 before tax at this store on this day — not eligible",
  "custom": "Other store",
  "steps_h": "How the new refund works",
  "steps": [
    "<b>At the store:</b> pay the full price, show your passport, and register for the refund with the store's refund company. Spend at least ¥5,000 before tax, in one store, on one day.",
    "<b>Don't use it:</b> keep everything unused until you leave. Food, drinks and cosmetics used in Japan can't be refunded.",
    "<b>At the airport, BEFORE check-in:</b> scan your passport at a tax-free kiosk in the departure lobby. Green = done. Red = show your items at customs.",
    "<b>Get paid:</b> the refund goes to the card or method you registered. Leave Japan within 90 days of buying."
  ],
  "warn": "Biggest mistake: checking in your suitcase before the kiosk. If customs asks to see items that are already in the hold, you lose the refund.",
  "fees_h": "Store refund fees (known so far)",
  "fees_note": "Each store chooses its own refund company and fee. Fees below are reported, not guaranteed — always ask at the tax-free counter before paying.",
  "th_store": "Store", "th_op": "Refund company", "th_fee": "Fee",
  "faq_h": "Common questions",
  "faq": [
    ["What is the minimum spend?", "¥5,000 or more before tax, at the same store on the same day."],
    ["Can I get the refund on a debit card?", "Some refund companies won't refund to prepaid or multi-currency debit cards. Registering a standard credit card is safest."],
    ["What if I bought before 1 November 2026?", "Purchases up to 31 October 2026 follow the old instant tax-free rules, even if you fly home later."],
    ["Is there still a spending cap on cosmetics and food?", "No. The ¥500,000 cap and sealed bags are gone under the new system."]
  ],
  "travel_h": "Before you fly",
  "esim": "Get a Japan eSIM so you have data at the airport kiosk", "activities": "Book tours, rail passes & tickets", "insurance": "Travel insurance",
  "updated": "Facts last checked", "sources": "Sources", "disclaimer": "Independent guide, not affiliated with the Japanese government. Some links are affiliate links; we may earn a commission at no extra cost to you.",
},
"ko": {
  "path": "ko/", "html_lang": "ko", "name": "한국어",
  "title": "일본 택스리펀드 계산기 2026 – 새 환급 제도 총정리",
  "desc": "2026년 11월 1일부터 일본 면세가 '선결제 후환급'으로 바뀌었습니다. 매장 수수료를 뺀 실제 환급액 계산, 90일 기한, 공항 절차까지 한 번에.",
  "h1": "일본 택스리펀드 계산기",
  "lead": "<b>2026년 11월 1일</b>부터 일본에서는 세금 포함 가격을 먼저 내고, 공항에서 세금을 돌려받습니다. 실제로 얼마를 돌려받는지 계산해 보세요.",
  "calc_h": "구매 내역",
  "store": "매장", "paid": "결제 금액 (엔, 세금 포함)", "type": "품목", "fee": "환급 수수료 %", "date": "구매일",
  "std": "일반 물품 (10%)", "food": "식품·음료 (8%)",
  "add": "+ 매장 추가", "remove": "삭제",
  "res_tax": "낸 세금", "res_fee": "수수료", "res_refund": "환급액", "res_deadline": "환급을 위한 출국 마감일",
  "not_eligible": "이 매장에서 하루 세전 5,000엔 미만 — 환급 대상 아님",
  "custom": "기타 매장",
  "steps_h": "새 환급 절차",
  "steps": [
    "<b>매장에서:</b> 세금 포함 가격을 결제하고 여권을 보여준 뒤, 매장의 환급 회사에 환급 정보를 등록하세요. 한 매장에서 하루 세전 5,000엔 이상이어야 합니다.",
    "<b>사용 금지:</b> 출국할 때까지 사용하지 마세요. 일본에서 먹거나 사용한 식품·화장품은 환급되지 않습니다.",
    "<b>공항에서 수하물 위탁 전에:</b> 출국 로비의 면세 키오스크에서 여권을 스캔하세요. 초록색 = 완료, 빨간색 = 세관에서 물건 확인.",
    "<b>환급 받기:</b> 등록한 카드나 방법으로 환급됩니다. 구매 후 90일 이내에 출국해야 합니다."
  ],
  "warn": "가장 흔한 실수: 키오스크 전에 캐리어를 먼저 부치는 것. 세관이 이미 부친 물건을 확인하려 하면 환급을 못 받습니다.",
  "fees_h": "매장별 환급 수수료 (현재까지 알려진 정보)",
  "fees_note": "매장마다 환급 회사와 수수료가 다릅니다. 아래 수수료는 보도된 내용이며 보장되지 않습니다. 결제 전 면세 카운터에서 꼭 확인하세요.",
  "th_store": "매장", "th_op": "환급 회사", "th_fee": "수수료",
  "faq_h": "자주 묻는 질문",
  "faq": [
    ["최소 구매 금액은?", "같은 매장, 같은 날 세전 5,000엔 이상입니다."],
    ["체크카드로 환급받을 수 있나요?", "일부 환급 회사는 선불·다통화 체크카드로 환급하지 않습니다. 일반 신용카드를 등록하는 것이 가장 안전합니다."],
    ["11월 1일 전에 산 물건은?", "2026년 10월 31일까지 구매한 물건은 출국이 그 이후여도 기존 즉시 면세 규칙이 적용됩니다."],
    ["화장품·식품 구매 한도가 아직 있나요?", "없습니다. 50만 엔 한도와 밀봉 포장은 새 제도에서 폐지되었습니다."]
  ],
  "travel_h": "출국 전 준비",
  "esim": "공항 키오스크에서도 데이터가 되는 일본 eSIM", "activities": "투어·패스·티켓 예약", "insurance": "여행자 보험",
  "updated": "정보 확인일", "sources": "출처", "disclaimer": "일본 정부와 무관한 독립 가이드입니다. 일부 링크는 제휴 링크이며, 추가 비용 없이 수수료를 받을 수 있습니다.",
},
"zh-tw": {
  "path": "zh-tw/", "html_lang": "zh-Hant-TW", "name": "繁體中文",
  "title": "日本退稅計算機 2026 – 新退稅制度完整說明",
  "desc": "2026年11月1日起，日本免稅改為「先付稅、後退稅」。計算扣除手續費後的實際退稅金額、90天期限與機場流程。",
  "h1": "日本退稅計算機",
  "lead": "自<b>2026年11月1日</b>起，在日本購物要先付含稅價格，離境時在機場退稅。算算看你實際能拿回多少。",
  "calc_h": "購物明細",
  "store": "店家", "paid": "支付金額（日圓，含稅）", "type": "商品類別", "fee": "退稅手續費 %", "date": "購買日期",
  "std": "一般商品（10%）", "food": "食品飲料（8%）",
  "add": "+ 新增店家", "remove": "刪除",
  "res_tax": "已付稅金", "res_fee": "手續費", "res_refund": "可退金額", "res_deadline": "退稅最晚離境日",
  "not_eligible": "此店當日未稅金額未滿5,000日圓——不符合退稅",
  "custom": "其他店家",
  "steps_h": "新退稅流程",
  "steps": [
    "<b>在店裡：</b>支付含稅價格、出示護照，並向店家的退稅公司登記退稅資料。同一店家、同一天未稅金額需滿5,000日圓。",
    "<b>不要使用：</b>離境前請勿使用。在日本食用或使用過的食品、化妝品無法退稅。",
    "<b>在機場，託運行李之前：</b>在出境大廳的免稅機台掃描護照。綠色＝完成；紅色＝需到海關檢查商品。",
    "<b>收到退款：</b>退稅會退到你登記的卡片或方式。購買後90天內必須離境。"
  ],
  "warn": "最常見的錯誤：先託運行李再去機台。若海關要檢查已託運的商品，就拿不到退稅。",
  "fees_h": "各店退稅手續費（目前已知）",
  "fees_note": "每家店自行選擇退稅公司與手續費。以下為報導資訊，並非保證——付款前請務必在免稅櫃台確認。",
  "th_store": "店家", "th_op": "退稅公司", "th_fee": "手續費",
  "faq_h": "常見問題",
  "faq": [
    ["最低消費金額是多少？", "同一店家、同一天未稅滿5,000日圓。"],
    ["可以退到簽帳金融卡嗎？", "部分退稅公司不接受預付卡或多幣別簽帳卡。登記一般信用卡最保險。"],
    ["11月1日前買的東西呢？", "2026年10月31日前購買的商品，即使之後才離境，仍適用舊的即時免稅規則。"],
    ["化妝品、食品還有購買上限嗎？", "沒有。新制已取消50萬日圓上限與密封包裝。"]
  ],
  "travel_h": "出發前準備",
  "esim": "日本eSIM，機場機台也能上網", "activities": "預訂行程、交通周遊券與門票", "insurance": "旅遊保險",
  "updated": "資料確認日期", "sources": "資料來源", "disclaimer": "本站為獨立指南，與日本政府無關。部分連結為聯盟連結，我們可能獲得佣金，您無需額外付費。",
},
}

FEE_TR = {  # translate fee strings for the table
  "ko": {"Not published": "미공개", "0% (store says no processing fee)": "0% (매장 공지: 수수료 없음)",
         "0% on card refunds (reported, not on Bic's site)": "카드 환급 0% (보도, 공식 미공개)",
         "About 10% of the refund": "환급액의 약 10%", "J&J Tax Free (reported)": "J&J Tax Free (보도)",
         "Hankyu / Hanshin dept. stores": "한큐·한신 백화점", "Don Quijote (Donki)": "돈키호테", "Bic Camera": "빅카메라",
         "Uniqlo": "유니클로", "Yodobashi Camera": "요도바시 카메라"},
  "zh-tw": {"Not published": "未公開", "0% (store says no processing fee)": "0%（店家表示不收手續費）",
         "0% on card refunds (reported, not on Bic's site)": "退至信用卡0%（報導，官網未公布）",
         "About 10% of the refund": "約退稅額的10%", "J&J Tax Free (reported)": "J&J Tax Free（報導）",
         "Hankyu / Hanshin dept. stores": "阪急・阪神百貨", "Don Quijote (Donki)": "唐吉訶德", "Bic Camera": "Bic Camera",
         "Uniqlo": "Uniqlo", "Yodobashi Camera": "友都八喜 Yodobashi"},
}

def tr(lang, s):
    return FEE_TR.get(lang, {}).get(s, s)

CSS = """
:root{--bg:#fffdf8;--ink:#1d1d1f;--muted:#5f6368;--accent:#c8102e;--card:#fff;--line:#e7e2d8;--ok:#1e7a46}
*{box-sizing:border-box}body{margin:0;font:16px/1.6 system-ui,-apple-system,"Segoe UI","Noto Sans KR","Noto Sans TC",sans-serif;background:var(--bg);color:var(--ink)}
.wrap{max-width:820px;margin:0 auto;padding:20px}
header{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap}
.logo{font-weight:800;color:var(--accent);text-decoration:none}.langs a{margin-left:10px;color:var(--muted);font-size:14px}
h1{font-size:clamp(26px,5vw,38px);line-height:1.2;margin:18px 0 8px}h2{margin-top:36px}
.lead{font-size:18px;color:#333}
.card{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px;margin:12px 0}
.row{display:grid;grid-template-columns:1.4fr 1fr 1fr .7fr 1fr auto;gap:8px;align-items:end;border-bottom:1px dashed var(--line);padding:10px 0}
.row label{font-size:12px;color:var(--muted);display:block}
input,select{width:100%;padding:9px;border:1px solid #ccc;border-radius:8px;font:inherit;background:#fff}
button{font:inherit;border:0;border-radius:8px;padding:10px 14px;cursor:pointer}
.add{background:#f3efe6}.rm{background:none;color:var(--muted);text-decoration:underline;padding:6px}
.note{font-size:13px;color:var(--accent);grid-column:1/-1}
.totals{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:14px}
.totals div{background:#faf6ee;border-radius:10px;padding:12px;text-align:center}.totals b{display:block;font-size:22px}
.totals .big b{color:var(--ok);font-size:28px}
.deadline{margin-top:10px;font-size:15px}
ol li{margin:10px 0}.warn{background:#fff1f1;border-left:4px solid var(--accent);padding:12px;border-radius:8px}
table{width:100%;border-collapse:collapse;font-size:15px}th,td{text-align:left;padding:8px;border-bottom:1px solid var(--line)}
.aff a{display:block;padding:12px;margin:8px 0;border:1px solid var(--line);border-radius:10px;text-decoration:none;color:var(--ink);background:#fff}
.aff a:hover{border-color:var(--accent)}
footer{font-size:13px;color:var(--muted);margin:40px 0 20px}
details{border-bottom:1px solid var(--line);padding:10px 0}summary{font-weight:600;cursor:pointer}
@media(max-width:640px){.row{grid-template-columns:1fr 1fr}.totals{grid-template-columns:1fr}}
"""

JS = r"""
(function(){
const T = window.T, STORES = window.STORES;
const rows = document.getElementById('rows');
function storeOptions(){
  let o = STORES.map((s,i)=>`<option value="${i}">${s.label}</option>`).join('');
  return o + `<option value="custom">${T.custom}</option>`;
}
function addRow(){
  const d = document.createElement('div'); d.className='row';
  const today = new Date().toISOString().slice(0,10);
  d.innerHTML = `
   <div><label>${T.store}</label><select class="st">${storeOptions()}</select></div>
   <div><label>${T.paid}</label><input class="amt" type="number" min="0" step="1" placeholder="11000"></div>
   <div><label>${T.type}</label><select class="ty"><option value="0.10">${T.std}</option><option value="0.08">${T.food}</option></select></div>
   <div><label>${T.fee}</label><input class="fee" type="number" min="0" max="100" step="0.5"></div>
   <div><label>${T.date}</label><input class="dt" type="date" value="${today}"></div>
   <div><button class="rm" type="button">${T.remove}</button></div>
   <div class="note" hidden>${T.not_eligible}</div>`;
  rows.appendChild(d);
  const st=d.querySelector('.st'), fee=d.querySelector('.fee');
  const setFee=()=>{ if(st.value!=='custom'){ const f=STORES[st.value].fee_pct; fee.value = f==null? 10 : f; } };
  st.addEventListener('change',()=>{setFee();calc();});
  setFee();
  d.querySelectorAll('input,select').forEach(e=>e.addEventListener('input',calc));
  d.querySelector('.rm').addEventListener('click',()=>{d.remove();calc();});
}
const yen = n => '¥' + Math.round(n).toLocaleString();
function calc(){
  let tax=0, fees=0, earliest=null;
  rows.querySelectorAll('.row').forEach(r=>{
    const amt = parseFloat(r.querySelector('.amt').value)||0;
    const rate = parseFloat(r.querySelector('.ty').value);
    const feePct = (parseFloat(r.querySelector('.fee').value)||0)/100;
    const t = amt*rate/(1+rate), pre = amt - t;
    const note = r.querySelector('.note');
    const ok = pre >= 5000;
    note.hidden = !(amt>0 && !ok);
    if(ok){ tax += t; fees += t*feePct;
      const dv = r.querySelector('.dt').value;
      if(dv){ const d=new Date(dv); if(!earliest||d<earliest) earliest=d; } }
  });
  document.getElementById('o-tax').textContent = yen(tax);
  document.getElementById('o-fee').textContent = yen(fees);
  document.getElementById('o-ref').textContent = yen(tax-fees);
  const dl = document.getElementById('o-dl');
  if(earliest){ const d=new Date(earliest); d.setDate(d.getDate()+90);
    dl.textContent = T.res_deadline + ': ' + d.toLocaleDateString(document.documentElement.lang,{year:'numeric',month:'long',day:'numeric'}); }
  else dl.textContent='';
}
document.getElementById('add').addEventListener('click',addRow);
addRow();
})();
"""

def page(code, L):
    up = "../" if L["path"] else ""
    other = "".join(f'<a href="{up}{LANGS[c]["path"] or "./"}index.html" hreflang="{LANGS[c]["html_lang"]}">{LANGS[c]["name"]}</a>' for c in LANGS if c != code)
    alternates = "".join(f'<link rel="alternate" hreflang="{LANGS[c]["html_lang"]}" href="{SITE_URL}/{LANGS[c]["path"]}">' for c in LANGS)
    alternates += f'<link rel="alternate" hreflang="x-default" href="{SITE_URL}/">'
    store_js = [{"label": tr(code, s["name"]), "fee_pct": s["fee_pct"]} for s in stores["stores"]]
    t_js = {k: L[k] for k in ["store","paid","type","fee","date","std","food","remove","not_eligible","custom","res_deadline"]}
    steps = "".join(f"<li>{s}</li>" for s in L["steps"])
    fee_rows = "".join(f"<tr><td>{html.escape(tr(code,s['name']))}</td><td>{html.escape(tr(code,s['operator']))}</td><td>{html.escape(tr(code,s['fee']))}</td></tr>" for s in stores["stores"])
    faq = "".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q,a in L["faq"])
    faq_ld = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in L["faq"]]}
    srcs = "".join(f'<li><a href="{s["url"]}" rel="nofollow">{html.escape(s["title"])}</a></li>' for s in stores["sources"])
    aff = "".join(f'<a href="{links[k]["url"]}" rel="sponsored nofollow" target="_blank">{L[k]} →</a>' for k in ["esim","activities","insurance"])
    return f"""<!doctype html>
<html lang="{L['html_lang']}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(L['title'])}</title>
<meta name="description" content="{html.escape(L['desc'])}">
<link rel="canonical" href="{SITE_URL}/{L['path']}">{alternates}
<meta property="og:title" content="{html.escape(L['title'])}"><meta property="og:description" content="{html.escape(L['desc'])}">
<meta property="og:type" content="website"><meta property="og:url" content="{SITE_URL}/{L['path']}">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><circle cx='50' cy='50' r='30' fill='%23c8102e'/></svg>">
<style>{CSS}</style>
<script type="application/ld+json">{json.dumps(faq_ld, ensure_ascii=False)}</script>
</head><body><div class="wrap">
<header><a class="logo" href="index.html">¥ Japan Tax Refund</a><nav class="langs">{other}</nav></header>
<h1>{L['h1']}</h1><p class="lead">{L['lead']}</p>
<section class="card"><h2 style="margin-top:0">{L['calc_h']}</h2>
<div id="rows"></div><button id="add" class="add" type="button">{L['add']}</button>
<div class="totals"><div>{L['res_tax']}<b id="o-tax">¥0</b></div><div>{L['res_fee']}<b id="o-fee">¥0</b></div><div class="big">{L['res_refund']}<b id="o-ref">¥0</b></div></div>
<p class="deadline" id="o-dl"></p></section>
<h2>{L['steps_h']}</h2><ol>{steps}</ol><p class="warn">⚠️ {L['warn']}</p>
<h2>{L['fees_h']}</h2><p>{L['fees_note']}</p>
<table><thead><tr><th>{L['th_store']}</th><th>{L['th_op']}</th><th>{L['th_fee']}</th></tr></thead><tbody>{fee_rows}</tbody></table>
<h2>{L['travel_h']}</h2><div class="aff">{aff}</div>
<h2>{L['faq_h']}</h2>{faq}
<footer><p>{L['updated']}: {stores['updated']}</p><p>{L['sources']}:</p><ul>{srcs}</ul><p>{L['disclaimer']}</p></footer>
</div>
<script>window.T={json.dumps(t_js, ensure_ascii=False)};window.STORES={json.dumps(store_js, ensure_ascii=False)};</script>
<script>{JS}</script>
</body></html>"""

def main():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    for code, L in LANGS.items():
        d = os.path.join(OUT, L["path"]); os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(page(code, L))
    urls = "".join(f"<url><loc>{SITE_URL}/{L['path']}</loc><lastmod>{stores['updated']}</lastmod></url>" for L in LANGS.values())
    open(os.path.join(OUT, "sitemap.xml"), "w").write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}/sitemap.xml\n")
    print("built", [L["path"] or "/" for L in LANGS.values()])

if __name__ == "__main__":
    main()
