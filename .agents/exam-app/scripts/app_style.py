"""The exam app's shared chrome — ONE stylesheet for all three screens.

Screen 1 (the test list) is built by `serve_sheet.py`; screens 2 and 3 (the exam
and its result) are built into 解答.html by `build_interactive.py`. They are
different files produced by different scripts, which is exactly how two "the
same" designs drift apart, so both import `APP_CSS` from here: the sticky `#bar`,
the buttons, the tables, the badges, the verdict colours are defined once.

Keep this module dependency-free (no markdown, no booklet import) — `make serve`
must start even if the authoring dependencies are not installed.

Keep it free of bare element selectors (`body`, `table`, …) too: 解答.html loads
it ON TOP of the booklet stylesheet, and the exam text must keep the booklet's
typography and its A4 print geometry. Scope every rule to an id or a class.
"""

APP_CSS = """
:root{--ink:#0f172a;--line:#cbd5e1;--muted:#475569;--accent:#1d4ed8;
  --ui:"Hiragino Sans","Yu Gothic",sans-serif}
/* The bar spans the full window on every screen, so the scrollbar sits ON its
   right edge — the horizontal padding has to clear it or it covers 採点する. */
#bar{position:sticky;top:0;z-index:99;background:#111;color:#fff;
  box-sizing:border-box;min-height:3.25em;padding:0 1.8em;display:flex;
  flex-wrap:nowrap;gap:.45em 1em;align-items:center;font-family:var(--ui);
  font-size:11pt}
#bar b{font-size:12pt;font-weight:700;white-space:nowrap;overflow:hidden;
  text-overflow:ellipsis;min-width:0;max-width:18em}
#bar .sub{font-size:10pt;color:#cbd5e1;font-variant-numeric:tabular-nums;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;min-width:0}
#bar .grow{flex:1 1 auto;min-width:.5em}
#bar-controls{display:flex;flex-wrap:nowrap;align-items:center;gap:.45em;flex:0 0 auto}
#bar button{font-size:10pt;padding:.25em .75em;cursor:pointer;border-radius:6px;
  border:1px solid #555;background:#fff;color:var(--ink);font-family:var(--ui);
  white-space:nowrap;line-line:1.35;min-height:32px;display:inline-flex;align-items:center}
#bar button.primary{background:var(--accent);color:#fff;border-color:var(--accent);
  font-weight:700}
#bar a.back{color:#cbd5e1;text-decoration:none;font-size:10.5pt;white-space:nowrap;
  flex:0 0 auto;padding:.2em 0}
#bar a.back:hover{color:#fff;text-decoration:underline}
.ui-btn{display:inline-flex;align-items:center;justify-content:center;
  font-size:11pt;padding:.45em 1.1em;border-radius:6px;text-decoration:none;
  border:1px solid var(--line);background:#fff;color:var(--ink);cursor:pointer;
  font-family:var(--ui);box-sizing:border-box;min-height:38px}
.ui-btn.primary{background:var(--accent);border-color:var(--accent);color:#fff;font-weight:700}
.ui-btn.danger{background:#fff;border-color:#fca5a5;color:#991b1b}
.ui-btn.danger:hover{background:#fef2f2}
.ui-btn:hover{filter:brightness(.96)}
.ui-table-wrap{width:100%;overflow-x:auto;-webkit-overflow-scrolling:touch;margin:.4em 0}
.ui-table{border-collapse:collapse;width:100%;font-size:10.5pt;margin:.4em 0;
  font-family:var(--ui)}
.ui-table th,.ui-table td{border:1px solid var(--line);padding:.35em .6em;
  text-align:left;vertical-align:middle}
.ui-table th{background:#f1f5f9;font-weight:700}
.ui-table td.n{text-align:right;font-variant-numeric:tabular-nums}
.ui-table tr.weak td{background:#fff7ed}
.badge{font-size:10pt;padding:.25em .7em;border-radius:99px;border:1px solid;
  white-space:nowrap;font-variant-numeric:tabular-nums;font-family:var(--ui);
  display:inline-flex;align-items:center}
.badge.pass{background:#f0fdf4;border-color:#16a34a;color:#166534}
.badge.fail{background:#fef2f2;border-color:#dc2626;color:#991b1b}
.badge.none{background:#f8fafc;border-color:var(--line);color:#64748b}
.badge.warn{background:#fffbeb;border-color:#f59e0b;color:#92400e}
.chip{display:inline-flex;align-items:center;gap:.35em;font-size:10pt;
  padding:.22em .55em;border-radius:6px;border:1px solid;font-family:var(--ui);
  font-variant-numeric:tabular-nums;min-height:30px}
.chip i{font-style:normal;font-size:9pt;opacity:.75}
.chip.ok{background:#f0fdf4;border-color:#86efac;color:#166534}
.chip.ng{background:#fef2f2;border-color:#fca5a5;color:#991b1b}
.chip.na{background:#f8fafc;border-color:var(--line);color:#64748b}
.meter .track{height:9px;border-radius:99px;background:#e2e8f0;overflow:hidden;
  text-align:left}
.meter .fill{height:100%;background:var(--accent)}
.meter .fill.done{background:#16a34a}
.meter .lbl{font-size:10pt;color:var(--muted);margin-top:.3em;text-align:left;
  font-variant-numeric:tabular-nums;font-family:var(--ui)}
@media screen and (max-width: 48em){
  #bar{padding:.45em .9em;gap:.35em .7em;flex-wrap:wrap;font-size:10pt}
  #bar b{max-width:11em;font-size:11pt}
  #bar .sub{font-size:9pt}
  #bar-controls{gap:.35em}
  #bar button{font-size:9.5pt;padding:.3em .65em;min-height:34px}
  .ui-btn{font-size:10pt;padding:.4em .85em;min-height:36px}
}
@media screen and (max-width: 32em){
  #bar b{max-width:7.5em;font-size:10.5pt}
  #where{display:none}
}
"""

