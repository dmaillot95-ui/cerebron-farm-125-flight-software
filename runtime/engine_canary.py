import json,hashlib,pathlib,platform
# Deterministic flight-software executive canary: periodic tasks, command validation, watchdog and safe-mode transition.
periods={"GNC":10,"TELEMETRY":20,"FDIR":5}; ticks=100; counts={k:0 for k in periods}; rejected=0; watchdog=0; safe=False
commands=[(12,"SET_MODE","NOMINAL"),(37,"BAD_OPCODE","X"),(63,"SET_MODE","SAFE")]
for t in range(ticks):
 for k,p in periods.items():
  if t%p==0: counts[k]+=1
 for ct,op,arg in commands:
  if t==ct:
   if op!="SET_MODE" or arg not in {"NOMINAL","SAFE"}: rejected+=1
   elif arg=="SAFE": safe=True
 if t==75:
  watchdog+=1; safe=True
expected={"GNC":10,"TELEMETRY":5,"FDIR":20}
ok=counts==expected and rejected==1 and watchdog==1 and safe
out={"farm":125,"engine":"python-deterministic-flight-software-executive","engine_version":platform.python_version(),"test":"SCHEDULER_COMMAND_FDIR","ticks":ticks,"task_counts":counts,"expected_counts":expected,"rejected_commands":rejected,"watchdog_events":watchdog,"final_safe_mode":safe,"status":"REAL_ENGINE_CANARY_OK" if ok else "FAIL","epistemic_status":"SOFTWARE_EXECUTIVE_CANARY_NOT_FLIGHT_QUALIFICATION"}
raw=json.dumps(out,sort_keys=True).encode();out["result_sha256"]=hashlib.sha256(raw).hexdigest();pathlib.Path("artifacts").mkdir(exist_ok=True);pathlib.Path("artifacts/f125_engine_canary.json").write_text(json.dumps(out,indent=2)+"\n");print(json.dumps(out));raise SystemExit(0 if ok else 1)
