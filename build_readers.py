#!/usr/bin/env python3
"""Build self-contained chapter readers (images embedded as base64) + series index."""
import base64, os, glob, re

BASE = "/home/user/project"
OUT  = os.path.join(BASE, "readers")

CHAPTERS = {
 1: ("Low Battery",                "SEPTEMBER · TOKYO",  "10 PAGES", "Sept · humid indigo + neon"),
 2: ("New Member",                 "SEPTEMBER · TOKYO",  "9 PAGES",  "Sept · warm amber"),
 3: ("Direct Message",             "OCTOBER · TOKYO",    "10 PAGES", "Oct · maple orange"),
 4: ("Two Months of Midnight",     "NOVEMBER · TOKYO",   "10 PAGES", "Nov · rust & gold"),
 5: ("Winter, Held Together",      "DECEMBER – JANUARY", "10 PAGES", "Dec–Jan · ice blue + screen glow"),
 6: ("Counting Down to Spring",    "FEBRUARY – MARCH",   "10 PAGES", "Feb–Mar · plum → bud pink"),
 7: ("See You Offline",            "APRIL · TOKYO",      "10 PAGES", "April · sakura pink + sky blue"),
}

CSS = """
  * { margin:0; padding:0; box-sizing:border-box; }
  body { background:#14121a; color:#efe9e2; font-family:Georgia,'Times New Roman',serif; }
  header { text-align:center; padding:56px 20px 30px; background:linear-gradient(180deg,#1d1a26 0%,#14121a 100%); }
  .kicker { letter-spacing:.35em; font-size:11px; color:#ff8a7a; text-transform:uppercase; font-family:Verdana,sans-serif; }
  h1 { font-size:34px; margin:10px 0 4px; letter-spacing:.06em; }
  .jp { color:#8f8798; font-size:14px; margin-bottom:18px; }
  h2 { font-size:19px; font-weight:normal; color:#d9cfc2; }
  .meta { font-size:12px; color:#7d7688; margin-top:10px; font-family:Verdana,sans-serif; }
  .bar { width:64px; height:3px; background:linear-gradient(90deg,#ff6b6b,#ffb25e); margin:22px auto 0; border-radius:2px; }
  main { max-width:860px; margin:0 auto; padding:26px 14px 60px; }
  .pg { margin:0 0 34px; }
  .pg img { width:100%; display:block; border-radius:10px; box-shadow:0 10px 40px rgba(0,0,0,.55); }
  figcaption { text-align:center; font-size:10px; letter-spacing:.3em; color:#6f6880; padding:12px 0 0; font-family:Verdana,sans-serif; }
  footer { text-align:center; padding:10px 20px 70px; color:#9a92a8; font-size:14px; }
  footer .next { color:#ffb25e; }
  .nav { text-align:center; font-family:Verdana,sans-serif; font-size:11px; letter-spacing:.18em; padding:0 0 24px; }
  .nav a { color:#8f8798; text-decoration:none; border-bottom:1px dotted #4a4458; padding-bottom:2px; }
  .nav a:hover { color:#ffb25e; }
  .mini { text-align:center; font-size:11px; color:#6f6880; font-family:Verdana,sans-serif; letter-spacing:.2em; padding:6px 0 0; }
"""

def img_tag(path):
    ext = "jpeg" if path.endswith((".jpeg",".jpg")) else "png"
    b = base64.b64encode(open(path,"rb").read()).decode()
    return f'<img src="data:image/{ext};base64,{b}" alt="{os.path.basename(path)}">'

def build(ch):
    d = os.path.join(BASE, "pages", f"ch{ch}")
    files = sorted(glob.glob(os.path.join(d, "p*.jp*g")))
    title, meta, pages, palette = CHAPTERS[ch]
    prev_l = f'<a href="Chapter_{ch-1}_Reader.html">← Chapter {ch-1}: {CHAPTERS[ch-1][0]}</a>' if ch > 1 else '<a href="../index.html">← Series library</a>'
    next_l = f'<span class="next">Next: Chapter {ch+1} — “{CHAPTERS[ch+1][0]}” 🐾</span>' if ch < 7 and os.path.exists(os.path.join(OUT, f"Chapter_{ch+1}_Reader.html")) else (
             '<span class="next">Season 1 complete 🐾</span>' if ch == 7 else "")
    figs = "\n".join(f'<figure class="pg">{img_tag(f)}<figcaption>PAGE {i:02d} / {len(files)}</figcaption></figure>'
                     for i, f in enumerate(files, 1))
    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>SEE YOU OFFLINE — Chapter {ch}: {title}</title></head><body><style>{CSS}</style>
<header>
  <div class="kicker">A PawGram Story</div>
  <h1>SEE YOU OFFLINE</h1>
  <div class="jp">オフラインで会おう</div>
  <h2>Chapter {ch} — “{title}”</h2>
  <div class="meta">{meta} · {len(files)} PAGES · {palette.upper()}</div>
  <div class="bar"></div>
</header>
<div class="nav">{prev_l}</div>
<main>
{figs}
</main>
<footer>Chapter {ch} — End &nbsp;·&nbsp; {next_l}</footer>
</body></html>"""
    out = os.path.join(OUT, f"Chapter_{ch}_Reader.html")
    open(out, "w", encoding="utf-8").write(html)
    print(f"Ch{ch}: {len(files)} pages -> {out} ({os.path.getsize(out)//1024} KB)")
    return len(files)

if __name__ == "__main__":
    for ch in CHAPTERS:
        if os.path.isdir(os.path.join(BASE, "pages", f"ch{ch}")):
            build(ch)
