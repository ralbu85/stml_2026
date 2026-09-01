#!/usr/bin/env python3
import urllib.request, urllib.error, re, time, os, sys

OUT = "/workspace/BALAB_Prof/Lecture_STML_2026/papers"
os.makedirs(OUT, exist_ok=True)

# (week, required?, slug, arxiv_id, expected keyword substring in real title [lowercase])
# 순서: 개념 의존성 기준 v4 재조정 (docs/syllabus.md 참고)
PAPERS = [
 (2,True ,"Chain-of-Thought","2201.11903","chain-of-thought prompting elicits"),
 (2,True ,"Self-Consistency","2203.11171","self-consistency improves chain of thought"),
 (3,True ,"STaR","2203.14465","bootstrapping reasoning"),
 (3,True ,"DeepSeek-R1","2501.12948","incentivizing reasoning"),
 (4,True ,"Toolformer","2302.04761","toolformer"),
 (4,True ,"ToolLLM","2307.16789","toolllm"),
 (4,False,"opt-ReTool","2504.11536","retool"),
 (5,True ,"ReAct","2210.03629","react"),
 (6,True ,"RAG-Lewis","2005.11401","retrieval-augmented generation for knowledge-intensive"),
 (6,True ,"Self-RAG","2310.11511","self-rag"),
 (6,False,"opt-HyDE","2212.10496","precise zero-shot dense retrieval"),
 (6,False,"opt-Adaptive-RAG","2403.14403","adaptive-rag"),
 (7,True ,"Tree-of-Thoughts","2305.10601","tree of thoughts"),
 (7,True ,"ReWOO","2305.18323","decoupling reasoning from observations"),
 (8,True ,"Reflexion","2303.11366","reflexion"),
 (8,True ,"Self-Refine","2303.17651","self-refine"),
 (9,True ,"Lost-in-the-Middle","2307.03172","lost in the middle"),
 (9,True ,"LLMLingua","2310.05736","llmlingua"),
 (9,False,"opt-Agentic-Context-Engineering","2510.04618","agentic context engineering"),
 (9,False,"opt-ReasoningBank","2509.25140","reasoningbank"),
 (10,True ,"MemGPT","2310.08560","memgpt"),
 (10,True ,"Mem0","2504.19413","building production-ready ai agents"),
 (10,False,"opt-MemoryBank","2305.10250","memorybank"),
 (10,False,"opt-Generative-Agents","2304.03442","generative agents"),
 (11,True ,"AutoGen","2308.08155","autogen"),
 (11,True ,"MetaGPT","2308.00352","metagpt"),
 (11,False,"opt-Multiagent-Debate","2305.14325","factuality and reasoning"),
 (11,False,"opt-CAMEL","2303.17760","camel"),
 (12,True ,"WebArena","2307.13854","webarena"),
 (12,True ,"OSWorld","2404.07972","benchmarking multimodal agents"),
 (12,False,"opt-Mind2Web","2306.06070","mind2web"),
 (12,False,"opt-Voyager","2305.16291","voyager"),
 (13,True ,"AI-Agents-That-Matter","2407.01502","ai agents that matter"),
 (13,True ,"tau-bench","2406.12045","-bench"),
 (14,True ,"Indirect-Prompt-Injection","2302.12173","signed up for"),
 (14,True ,"InjecAgent","2403.02691","injecagent"),
 (15,True ,"Agentless","2407.01489","agentless"),
 (15,True ,"SWE-agent","2405.15793","swe-agent"),
 (16,True ,"LLM-Agents-Survey-Xi","2309.07864","rise and potential of large language model"),
]

UA = {"User-Agent":"Mozilla/5.0 (course-syllabus-checker; mailto:ralbu85@gmail.com)"}

def get_title(arxiv_id):
    req = urllib.request.Request(f"https://arxiv.org/abs/{arxiv_id}", headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        html = r.read().decode("utf-8","ignore")
    m = re.search(r"<title>(.*?)</title>", html, re.S)
    t = re.sub(r"\s+"," ", m.group(1)).strip() if m else ""
    return re.sub(r"^\[[^\]]*\]\s*","",t)

def download_pdf(arxiv_id, path):
    req = urllib.request.Request(f"https://arxiv.org/pdf/{arxiv_id}", headers=UA)
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
    path=os.path.join(OUT,f"{tag}_{slug}_{aid}.pdf")
    st={"wk":wk,"slug":slug,"aid":aid,"kw":kw}
    try:
        title=get_title(aid); st["title"]=title; st["match"]= kw.lower() in title.lower()
    except Exception as e:
        st["title"]=f"ERR {e}"; st["match"]=False
    try:
        st["bytes"]=download_pdf(aid,path)
    except Exception as e:
        st["bytes"]=0; st["dlerr"]=str(e)
    rows.append(st)
    print(f"{'OK ' if st['match'] else '?? '}{tag} {slug:34s} {aid:12s} {st.get('bytes',0)//1024:6d}KB  {st['title'][:60]}")
    time.sleep(0.6)

bad=[r for r in rows if not r["match"]]; nopdf=[r for r in rows if r.get("bytes",0)==0]
print(f"\n===== total={len(rows)} title_mismatch={len(bad)} pdf_missing={len(nopdf)} =====")
for r in bad:   print(f"  MISMATCH W{r['wk']:02d} {r['slug']} [{r['aid']}] expected~'{r['kw']}' got: {r['title'][:70]}")
for r in nopdf: print(f"  NOPDF    W{r['wk']:02d} {r['slug']} [{r['aid']}] {r.get('dlerr','no pdf')}")
