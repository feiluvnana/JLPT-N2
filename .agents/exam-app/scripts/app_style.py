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
:root{
  --ink:#0f172a;
  --line:#cbd5e1;
  --muted:#64748b;
  --accent:#2563eb;
  --accent-hover:#1d4ed8;
  --ui:"Noto Sans JP",-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Hiragino Sans","Yu Gothic",sans-serif;
  --serif:"Noto Serif JP","Yu Mincho",serif;
}
/* The bar spans the full window on every screen, so the scrollbar sits ON its
   right edge — the horizontal padding has to clear it or it covers 採点する. */
#bar{
  position:sticky;
  top:0;
  z-index:99;
  background:linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
  color:#ffffff;
  box-sizing:border-box;
  min-height:3.4em;
  padding:0 1.8em;
  display:flex;
  flex-wrap:nowrap;
  gap:.6em 1.2em;
  align-items:center;
  font-family:var(--ui);
  font-size:11pt;
  box-shadow:0 4px 14px rgba(0,0,0,0.08);
  border-bottom:1px solid rgba(255,255,255,0.08);
}
#bar b{
  font-size:12.5pt;
  font-weight:800;
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
  min-width:0;
  max-width:20em;
  color:#ffffff;
}
#bar .sub{
  font-size:9.5pt;
  color:#94a3b8;
  font-variant-numeric:tabular-nums;
  white-space:nowrap;
  overflow:hidden;
  text-overflow:ellipsis;
  min-width:0;
}
#bar .grow{
  flex:1 1 auto;
  min-width:.5em;
}
#bar-controls{
  display:flex;
  flex-wrap:nowrap;
  align-items:center;
  gap:.55em;
  flex:0 0 auto;
}
#bar button{
  font-size:10pt;
  font-weight:700;
  padding:.3em .85em;
  cursor:pointer;
  border-radius:6px;
  border:1px solid rgba(255,255,255,0.2);
  background:rgba(255,255,255,0.1);
  color:#ffffff;
  font-family:var(--ui);
  white-space:nowrap;
  line-height:1.35;
  min-height:34px;
  display:inline-flex;
  align-items:center;
  justify-content:center;
  transition:all .15s ease;
}
#bar button:hover{
  background:rgba(255,255,255,0.2);
  border-color:rgba(255,255,255,0.35);
}
#bar button.primary{
  background:var(--accent);
  color:#ffffff;
  border-color:var(--accent);
  box-shadow:0 2px 6px rgba(37,99,235,0.3);
}
#bar button.primary:hover{
  background:var(--accent-hover);
  border-color:var(--accent-hover);
}
#bar a.back{
  display:inline-flex;
  align-items:center;
  gap:.35em;
  color:#cbd5e1;
  text-decoration:none;
  font-size:10pt;
  font-weight:700;
  white-space:nowrap;
  flex:0 0 auto;
  padding:.3em .75em;
  border-radius:6px;
  background:rgba(255,255,255,0.08);
  border:1px solid rgba(255,255,255,0.15);
  transition:all .15s ease;
}
#bar a.back:hover{
  background:rgba(255,255,255,0.18);
  color:#ffffff;
  border-color:rgba(255,255,255,0.3);
}
.ui-btn{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  font-size:10pt;
  font-weight:600;
  padding:0 1.1em;
  height:38px;
  min-height:38px;
  max-height:38px;
  line-height:36px;
  border-radius:6px;
  text-decoration:none;
  border:1px solid var(--line);
  background:#ffffff;
  color:var(--ink);
  cursor:pointer;
  font-family:var(--ui);
  box-sizing:border-box;
  vertical-align:middle;
  -webkit-appearance:none;
  appearance:none;
  transition:all .15s ease;
}
.ui-btn:hover{
  background:#f8fafc;
  border-color:#94a3b8;
  color:var(--ink);
}
.ui-btn.primary{
  background:var(--accent);
  border-color:var(--accent);
  color:#ffffff;
  font-weight:700;
  box-shadow:0 2px 6px rgba(37,99,235,0.2);
}
.ui-btn.primary:hover{
  background:var(--accent-hover);
  border-color:var(--accent-hover);
  color:#ffffff;
}
.ui-btn.danger{
  background:#ffffff;
  border-color:#fca5a5;
  color:#991b1b;
}
.ui-btn.danger:hover{
  background:#fef2f2;
  border-color:#f87171;
}
.ui-table-wrap{
  width:100%;
  overflow-x:auto;
  -webkit-overflow-scrolling:touch;
  margin:.6em 0;
  border-radius:8px;
  border:1px solid var(--line);
}
.ui-table{
  border-collapse:collapse;
  width:100%;
  font-size:10pt;
  margin:0;
  font-family:var(--ui);
}
.ui-table th,.ui-table td{
  border:1px solid #e2e8f0;
  padding:.55em .8em;
  text-align:left;
  vertical-align:middle;
}
.ui-table th{
  background:#f1f5f9;
  font-weight:700;
  color:#1e293b;
  border-bottom:2px solid #cbd5e1;
}
.ui-table tr{
  transition:background .1s ease;
}
.ui-table tbody tr:hover{
  background:#f8fafc;
}
.ui-table td.n{
  text-align:right;
  font-variant-numeric:tabular-nums;
}
.ui-table tr.weak td{
  background:#fffbeb;
  color:#92400e;
}
.badge{
  font-size:9.5pt;
  font-weight:700;
  padding:.22em .75em;
  border-radius:9999px;
  border:1px solid;
  white-space:nowrap;
  font-variant-numeric:tabular-nums;
  font-family:var(--ui);
  display:inline-flex;
  align-items:center;
  letter-spacing:.02em;
}
.badge.pass{
  background:#ecfdf5;
  border-color:#a7f3d0;
  color:#065f46;
}
.badge.fail{
  background:#fef2f2;
  border-color:#fecaca;
  color:#991b1b;
}
.badge.none{
  background:#f8fafc;
  border-color:var(--line);
  color:#64748b;
}
.badge.warn{
  background:#fffbeb;
  border-color:#fde68a;
  color:#92400e;
}
.chip{
  display:inline-flex;
  align-items:center;
  justify-content:center;
  gap:.35em;
  font-size:9.5pt;
  font-weight:700;
  padding:.22em .6em;
  border-radius:6px;
  border:1px solid;
  font-family:var(--ui);
  font-variant-numeric:tabular-nums;
  min-height:30px;
  transition:all .15s ease;
}
.chip i{
  font-style:normal;
  font-size:8.5pt;
  opacity:.8;
}
.chip.ok{
  background:#ecfdf5;
  border-color:#a7f3d0;
  color:#065f46;
}
.chip.ng{
  background:#fef2f2;
  border-color:#fecaca;
  color:#991b1b;
}
.chip.na{
  background:#f8fafc;
  border-color:var(--line);
  color:#64748b;
}
.meter .track{
  height:8px;
  border-radius:9999px;
  background:#e2e8f0;
  overflow:hidden;
  text-align:left;
}
.meter .fill{
  height:100%;
  border-radius:9999px;
  background:var(--accent);
  transition:width .3s ease;
}
.meter .fill.done{
  background:#059669;
}
.meter .lbl{
  font-size:9.5pt;
  color:var(--muted);
  margin-top:.35em;
  text-align:left;
  font-variant-numeric:tabular-nums;
  font-family:var(--ui);
}
@media screen and (max-width: 48em){
  #bar{
    padding:.5em .9em;
    gap:.4em .8em;
    flex-wrap:wrap;
    font-size:10pt;
  }
  #bar b{
    max-width:12em;
    font-size:11.5pt;
  }
  #bar .sub{
    font-size:9pt;
  }
  #bar-controls{
    gap:.4em;
  }
  #bar button{
    font-size:9.5pt;
    padding:.3em .7em;
    min-height:34px;
  }
  .ui-btn{
    font-size:10pt;
    padding:.4em .9em;
    min-height:36px;
  }
}
@media screen and (max-width: 32em){
  #bar b{
    max-width:8.5em;
    font-size:10.5pt;
  }
  #where{
    display:none;
  }
}
"""
