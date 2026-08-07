"""The browser-side store — ONE implementation of "the disk, in localStorage".

`make serve` writes answers and results to `tests/<id>/ユーザー解答.json` and
`tests/<id>/採点結果.json`. A GitHub Pages deployment is static: there is no
server to POST to and no disk to write. This module holds the localStorage
backend that stands in for that disk, and it is the SINGLE copy of it — both
the exam sheet (screens 2–3, `build_interactive.py`) and the test list
(screen 1, `build_pages.py` via `index_view.py`) include this same snippet.

**One store per build, never two.** `exam-app/SKILL.md` forbids
a second copy of the answers, because the list and the sheet would then disagree
about what you answered. That rule is unchanged: the storage backend is chosen
at BUILD time (`build_interactive.py --storage server|local`), so a server build
touches only the JSON files on disk and a Pages build touches only localStorage.
Nothing sniffs at runtime and nothing writes to both.

The localStorage keys deliberately spell out the on-disk paths they replace —
`jlpt-mock/v1/<test_id>/ユーザー解答.json` — so what a key holds, and which file
it corresponds to when you export it, is readable in devtools.

Keep this module dependency-free: `make serve` must start without the authoring
dependencies installed.
"""

# Bump the version segment only if the stored SHAPE changes; the values are the
# same documents grade_answers.py reads, so a shape change means a grader change.
STORAGE_PREFIX = "jlpt-mock/v1"
ANSWERS_JSON = "ユーザー解答.json"
RESULT_JSON = "採点結果.json"

# `window.JLPTStore` — the localStorage half of the two storage backends.
# Pure data access: no DOM, no fetch, no rendering. Safe to include on any page.
LOCAL_STORE_JS = """
window.JLPTStore = (function(){
  var PREFIX = "%(prefix)s", ANSWERS = "%(answers)s", RESULT = "%(result)s";
  function key(id, name){ return PREFIX + '/' + id + '/' + name; }
  function read(id, name){
    try {
      var raw = localStorage.getItem(key(id, name));
      return raw ? JSON.parse(raw) : null;
    } catch (e){ return null; }          // private mode, quota, corrupt JSON
  }
  function write(id, name, obj){
    try { localStorage.setItem(key(id, name), JSON.stringify(obj)); return true; }
    catch (e){ return false; }           // quota exceeded → caller falls back
  }
  function remove(id, name){
    try { localStorage.removeItem(key(id, name)); } catch (e){}
  }
  return {
    PREFIX: PREFIX, ANSWERS: ANSWERS, RESULT: RESULT,
    key: key, read: read, write: write, remove: remove,
    answers: function(id){ return read(id, ANSWERS); },
    setAnswers: function(id, o){ return write(id, ANSWERS, o); },
    result: function(id){ return read(id, RESULT); },
    setResult: function(id, o){ return write(id, RESULT, o); },
    clear: function(id){ remove(id, ANSWERS); remove(id, RESULT); },
    // Which test ids this browser actually holds data for — the Pages test
    // list uses it so a test whose folder was renamed still shows its progress.
    ids: function(){
      var out = [];
      try {
        for (var i = 0; i < localStorage.length; i++){
          var k = localStorage.key(i);
          if (k && k.indexOf(PREFIX + '/') === 0){
            var id = k.slice(PREFIX.length + 1).split('/')[0];
            if (id && out.indexOf(id) < 0) out.push(id);
          }
        }
      } catch (e){}
      return out;
    }
  };
})();
""" % {"prefix": STORAGE_PREFIX, "answers": ANSWERS_JSON, "result": RESULT_JSON}
