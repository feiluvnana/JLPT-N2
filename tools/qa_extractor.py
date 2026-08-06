import json
import re
import os

def check_test(test_id="2"):
    findings = []
    
    gengo_md_path = f"tests/{test_id}/言語知識・読解.md"
    choukai_md_path = f"tests/{test_id}/聴解.md"
    
    with open(gengo_md_path, "r", encoding="utf-8") as f:
        gengo = f.read()
        
    with open(choukai_md_path, "r", encoding="utf-8") as f:
        choukai = f.read()
        
    # Check 1: Stem length in 問題7
    mon7_match = re.search(r'## 問題7.*?(?=## 問題8)', gengo, re.DOTALL)
    if mon7_match:
        mon7 = mon7_match.group(0)
        stems = re.findall(r'\*\*(\d+)\*\*(.*?)\n', mon7)
        total_len = 0
        stem_count = 0
        for num, stem in stems:
            # strip options
            stem_text = re.sub(r'^\s*\d\.\s.*$', '', stem, flags=re.MULTILINE).strip()
            total_len += len(stem_text)
            stem_count += 1
            if len(stem_text) < 30:
                findings.append({"item": f"問題7-{num}", "class": "automatic", "evidence": f"Stem length is {len(stem_text)} chars (< 30)", "fix": "Rewrite stem to be longer"})
        if stem_count > 0:
            avg = total_len / stem_count
            if avg < 35:
                findings.append({"item": "問題7", "class": "automatic", "evidence": f"Average stem length {avg:.1f} < 35", "fix": "Rewrite stems"})
                
    # Check 2: (注N) counts
    chu_count = len(re.findall(r'（注\d+）', gengo))
    if chu_count < 15:
        findings.append({"item": "読解全体", "class": "automatic", "evidence": f"Total （注N） count is {chu_count} < 15", "fix": "Add more 注 to passages"})
        
    # Check 3: (中略) presence
    if '（中略）' not in gengo:
        findings.append({"item": "読解全体", "class": "automatic", "evidence": "No （中略） in passages", "fix": "Add 中略 to long passages"})
        
    # Check 4: furigana
    if '<ruby>' in gengo:
        findings.append({"item": "読解全体", "class": "automatic", "evidence": "Furigana found in Gengo.md", "fix": "Remove ruby tags, use 注"})

    # Extract all answers
    all_items = []
    
    with open("qa_report.json", "w") as f:
        json.dump(findings, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    check_test()
