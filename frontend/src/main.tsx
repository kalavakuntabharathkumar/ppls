import React, {useEffect, useState} from "react";
import {createRoot} from "react-dom/client";
import "./styles.css";

type Rule = {id:string; name:string; condition:string; action:string; enabled:boolean};
const API = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

function App() {
  const [rules,setRules]=useState<Rule[]>([]);
  const [name,setName]=useState("");
  const [condition,setCondition]=useState("");
  const [action,setAction]=useState("bank-a");
  const [status,setStatus]=useState("");

  const load=()=>fetch(`${API}/rules`).then(r=>r.json()).then(setRules).catch(()=>setStatus("Start the FastAPI backend first."));
  useEffect(()=>{load()},[]);

  async function addRule(e:React.FormEvent) {
    e.preventDefault();
    const r=await fetch(`${API}/rules`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({name,condition,action,enabled:true})});
    if(!r.ok){setStatus("Rule could not be created.");return}
    setName("");setCondition("");setStatus("Rule published.");load();
  }

  return <main>
    <header><span className="eyebrow">PAYPULSE</span><h1>Rules Studio</h1><p>Self-service payment routing controls and anomaly operations.</p></header>
    <section className="grid">
      <form className="card" onSubmit={addRule}>
        <h2>Create routing rule</h2>
        <label>Name<input value={name} onChange={e=>setName(e.target.value)} required/></label>
        <label>Condition<input value={condition} onChange={e=>setCondition(e.target.value)} placeholder="merchant_tier == 'gold'" required/></label>
        <label>Action<select value={action} onChange={e=>setAction(e.target.value)}><option>bank-a</option><option>bank-b</option><option>bank-c</option></select></label>
        <button>Publish rule</button><small>{status}</small>
      </form>
      <section className="card"><h2>Active rules</h2>{rules.map(r=><article className="rule" key={r.id}><b>{r.name}</b><span>{r.condition}</span><em>{r.action}</em></article>)}</section>
    </section>
  </main>
}
createRoot(document.getElementById("root")!).render(<App />);
