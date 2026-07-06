#!/usr/bin/env python3
import urllib.request, urllib.error, re, time, os, sys

OUT = "/workspace/BALAB_Prof/Lecture_STML_2026/papers"
os.makedirs(OUT, exist_ok=True)

# (week, required?, slug, arxiv_id, expected keyword substring in real title [lowercase])
PAPERS = [
 (1,True ,"ReAct","2210.03629","react"),
 (1,True ,"Chain-of-Thought","2201.11903","chain-of-thought prompting elicits"),
 (2,True ,"Toolformer","2302.04761","toolformer"),
 (2,True ,"ToolLLM","2307.16789","toolllm"),
 (3,True ,"Reflexion","2303.11366","reflexion"),
 (3,True ,"Self-Refine","2303.17651","self-refine"),
 (4,True ,"Tree-of-Thoughts","2305.10601","tree of thoughts"),
 (4,True ,"ReWOO","2305.18323","decoupling reasoning from observations"),
 (5,True ,"STaR","2203.14465","bootstrapping reasoning"),
 (5,True ,"DeepSeek-R1","2501.12948","incentivizing reasoning"),
 (6,True ,"RAG-Lewis","2005.11401","retrieval-augmented generation for knowledge-intensive"),
 (6,True ,"HyDE","2212.10496","precise zero-shot dense retrieval"),
 (7,True ,"Self-RAG","2310.11511","self-rag"),
 (7,True ,"Adaptive-RAG","2403.14403","adaptive-rag"),
 (8,True ,"MemGPT","2310.08560","memgpt"),
 (8,True ,"MemoryBank","2305.10250","memorybank"),
 (9,True ,"Voyager","2305.16291","voyager"),
 (9,True ,"Generative-Agents","2304.03442","generative agents"),
 (10,True ,"AutoGen","2308.08155","autogen"),
 (10,True ,"MetaGPT","2308.00352","metagpt"),
 (10,False,"opt-Multiagent-Debate","2305.14325","factuality and reasoning"),
 (10,False,"opt-CAMEL","2303.17760","camel"),
 (11,True ,"ReTool","2504.11536","retool"),
 (11,False,"opt-Agentic-Context-Engineering","2510.04618","agentic context engineering"),
 (11,False,"opt-ReasoningBank","2509.25140","reasoningbank"),
 (12,True ,"WebArena","2307.13854","webarena"),
 (12,True ,"Mind2Web","2306.06070","mind2web"),
 (13,True ,"Indirect-Prompt-Injection","2302.12173","signed up for"),
 (13,True ,"InjecAgent","2403.02691","injecagent"),
 (14,True ,"AI-Agents-That-Matter","2407.01502","ai agents that matter"),
 (14,True ,"tau-bench","2406.12045","-bench"),
 (15,True ,"Agentless","2407.01489","agentless"),
 (15,True ,"SWE-agent","2405.15793","swe-agent"),
 (16,True ,"LLM-Agents-Survey-Xi","2309.07864","rise and potential of large language model"),
]

UA = {"User-Agent":"Mozilla/5.0 (course-syllabus-checker; mailto:ralbu85@gmail.com)"}

def get_title(arxiv_id):
    url = f"https://arxiv.org/abs/{arxiv_id}"
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        html = r.read().decode("utf-8","ignore")
    m = re.search(r"<title>(.*?)</title>", html, re.S)
    t = re.sub(r"\s+"," ", m.group(1)).strip() if m else ""
    t = re.sub(r"^\[[^\]]*\]\s*","",t)  # strip leading [id]
    return t

def download_pdf(arxiv_id, path):
    url = f"https://arxiv.org/pdf/{arxiv_id}"
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=90) as r:
        data = r.read()
    if data[:4] != b"%PDF":
        return 0
    with open(path,"wb") as f:
        f.write(data)
    return len(data)

rows=[]
for wk,req,slug,aid,kw in PAPERS:
    tag=f"W{wk:02d}"
    fname=f"{tag}_{slug}_{aid}.pdf"
    path=os.path.join(OUT,fname)
    status={"wk":wk,"req":req,"slug":slug,"aid":aid,"kw":kw}
    try:
        title=get_title(aid)
        status["title"]=title
        status["match"]= kw.lower() in title.lower()
    except Exception as e:
        status["title"]=f"ERR abs: {e}"
        status["match"]=False
    # download
    try:
        n=download_pdf(aid,path)
        status["bytes"]=n
    except Exception as e:
        status["bytes"]=0
        status["dlerr"]=str(e)
    rows.append(status)
    mk="OK " if status["match"] else "?? "
    print(f"{mk}{tag} {slug:32s} {aid:12s} {status.get('bytes',0)//1024:6d}KB  {status['title'][:70]}")
    time.sleep(0.7)

# summary
bad=[r for r in rows if not r["match"]]
nopdf=[r for r in rows if r.get("bytes",0)==0]
print("\n===== SUMMARY =====")
print(f"total={len(rows)}  title_mismatch={len(bad)}  pdf_missing={len(nopdf)}")
if bad:
    print("\n-- TITLE MISMATCH (verify ID!) --")
    for r in bad:
        print(f"  W{r['wk']:02d} {r['slug']} [{r['aid']}] expected~'{r['kw']}' got: {r['title'][:80]}")
if nopdf:
    print("\n-- PDF MISSING --")
    for r in nopdf:
        print(f"  W{r['wk']:02d} {r['slug']} [{r['aid']}] {r.get('dlerr','no pdf bytes')}")
