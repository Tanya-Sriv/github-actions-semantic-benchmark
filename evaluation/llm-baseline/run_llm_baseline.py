#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, os, random, time
from datetime import datetime, timezone
from pathlib import Path
import requests, yaml

PKG=Path(__file__).resolve().parent

def utcnow(): return datetime.now(timezone.utc).isoformat()
def digest(s:str): return hashlib.sha256(s.encode()).hexdigest()

def load_cfg(path):
    with open(path,encoding="utf-8") as f:return yaml.safe_load(f)

def call_openai(p, prompt, max_tokens, timeout):
    key=os.environ[p["api_key_env"]]
    payload={"model":p["model"],"input":prompt,"max_output_tokens":max_tokens}
    if p.get("temperature") is not None: payload["temperature"]=p["temperature"]
    payload.update(p.get("extra_request_fields",{}))
    r=requests.post(p["endpoint"],headers={"Authorization":f"Bearer {key}","Content-Type":"application/json"},json=payload,timeout=timeout)
    r.raise_for_status(); data=r.json()
    text=data.get("output_text")
    if not text:
        parts=[]
        for item in data.get("output",[]):
            for c in item.get("content",[]):
                if c.get("type") in {"output_text","text"}: parts.append(c.get("text",""))
        text="\n".join(parts)
    return data,text or ""

def call_anthropic(p,prompt,max_tokens,timeout):
    key=os.environ[p["api_key_env"]]
    payload={"model":p["model"],"max_tokens":max_tokens,"messages":[{"role":"user","content":prompt}]}
    if p.get("temperature") is not None:payload["temperature"]=p["temperature"]
    payload.update(p.get("extra_request_fields",{}))
    h={"x-api-key":key,"anthropic-version":p.get("anthropic_version","2023-06-01"),"Content-Type":"application/json"}
    r=requests.post(p["endpoint"],headers=h,json=payload,timeout=timeout);r.raise_for_status();data=r.json()
    text="\n".join(x.get("text","") for x in data.get("content",[]) if x.get("type")=="text")
    return data,text

def call_google(p,prompt,max_tokens,timeout):
    key=os.environ[p["api_key_env"]]
    endpoint=p["endpoint_template"].format(model=p["model"])
    payload={"contents":[{"role":"user","parts":[{"text":prompt}]}],"generationConfig":{"maxOutputTokens":max_tokens}}
    if p.get("temperature") is not None:payload["generationConfig"]["temperature"]=p["temperature"]
    payload.update(p.get("extra_request_fields",{}))
    r=requests.post(endpoint,headers={"x-goog-api-key":key,"Content-Type":"application/json"},json=payload,timeout=timeout);r.raise_for_status();data=r.json()
    text="\n".join(part.get("text","") for cand in data.get("candidates",[]) for part in cand.get("content",{}).get("parts",[]) if "text" in part)
    return data,text

CALLERS={"openai":call_openai,"anthropic":call_anthropic,"google":call_google}

def main():
    ap=argparse.ArgumentParser();ap.add_argument("--config",default="providers.yaml");ap.add_argument("--cases",default="private/prepared_cases_private.json");ap.add_argument("--dry-run",action="store_true");ap.add_argument("--case-id");ap.add_argument("--provider");args=ap.parse_args()
    cfg=load_cfg(PKG/args.config); cases=json.loads((PKG/args.cases).read_text()); template=(PKG/"prompt_template.txt").read_text()
    exp=cfg["experiment"]; trials=int(exp["trials_per_case"]); timeout=int(exp["timeout_seconds"]); max_tokens=int(exp["max_output_tokens"])
    providers=[p for p in cfg["providers"] if p.get("enabled")]
    if args.provider: providers=[p for p in providers if p["provider"]==args.provider]
    if not providers: raise SystemExit("No enabled providers.")
    if args.case_id: cases=[c for c in cases if c["source_case_id"]==args.case_id]
    for p in providers:
        if p["provider"] not in CALLERS: raise ValueError(p["provider"])
        if "FILL_" in p["model"]: raise ValueError("Exact model ID not filled")
        if not args.dry_run and not os.getenv(p["api_key_env"]): raise EnvironmentError(f"Missing {p['api_key_env']}")
        for case in cases:
            prompt=template.format(intended_behavior=case["intended_behavior"],workflow_bundle=case["workflow_bundle"])
            for trial in range(1,trials+1):
                run_id=f"{p['provider']}__{p['model'].replace('/','_')}__{case['source_case_id']}__t{trial}"
                req={"run_id":run_id,"timestamp_utc":utcnow(),"provider":p["provider"],"model":p["model"],"case_id":case["source_case_id"],"case_status":case["case_status"],"set":case["set"],"trial":trial,"prompt_sha256":digest(prompt),"prompt":prompt,"settings":{"temperature":p.get("temperature"),"max_output_tokens":max_tokens}}
                (PKG/"raw_requests"/f"{run_id}.json").write_text(json.dumps(req,indent=2)+"\n")
                if args.dry_run:
                    print("DRY",run_id);continue
                attempts=[]; raw=None;text="";error=None
                for attempt in range(1,int(exp.get("retry_transport_errors",3))+1):
                    try:
                        raw,text=CALLERS[p["provider"]](p,prompt,max_tokens,timeout);error=None;break
                    except (requests.Timeout,requests.ConnectionError,requests.HTTPError) as e:
                        error=repr(e);attempts.append({"attempt":attempt,"error":error,"time":utcnow()})
                        if isinstance(e,requests.HTTPError) and e.response is not None and e.response.status_code < 500 and e.response.status_code != 429: break
                        time.sleep(min(2**attempt,30))
                out={"run_id":run_id,"completed_utc":utcnow(),"provider":p["provider"],"model":p["model"],"case_id":case["source_case_id"],"case_status":case["case_status"],"set":case["set"],"trial":trial,"response_text":text,"response_sha256":digest(text),"raw_response":raw,"attempt_log":attempts,"terminal_error":error}
                (PKG/"raw_responses"/f"{run_id}.json").write_text(json.dumps(out,indent=2)+"\n")
                print("DONE",run_id,"chars",len(text),"error",bool(error))

if __name__=="__main__": main()
