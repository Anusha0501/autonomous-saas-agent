import React, { useState } from 'react';
import { createRoot } from 'react-dom/client';
import { Bot, CheckCircle2, ShieldCheck } from 'lucide-react';
import './styles.css';

type AgentRun = {
  id: string;
  goal: string;
  status: string;
  current_node: string;
  tasks: { id: string; title: string; description: string; risk_level: string; requires_approval: boolean; status: string }[];
  research_notes: string[];
  approvals: { id: string; proposed_action: string; risk_level: string; status: string }[];
  final_output?: string;
  cost_summary: { estimated_cost_usd: number; total_tokens: number; model_calls: number; tool_calls: number };
};

const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api';

function App() {
  const [goal, setGoal] = useState('Research competitors and draft a launch plan for my AI note-taking SaaS.');
  const [run, setRun] = useState<AgentRun | null>(null);
  const [loading, setLoading] = useState(false);

  async function submitGoal() {
    setLoading(true);
    const response = await fetch(`${API_URL}/runs`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ goal, constraints: { budget_usd: 5, requires_approval_for_external_actions: true } }),
    });
    setRun(await response.json());
    setLoading(false);
  }

  async function approveRun() {
    if (!run) return;
    const response = await fetch(`${API_URL}/approvals/${run.id}/approve`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ reason: 'Approved from dashboard.' }),
    });
    setRun(await response.json());
  }

  return (
    <main className="shell">
      <section className="hero">
        <div>
          <p className="eyebrow"><Bot size={18} /> Autonomous SaaS Agent</p>
          <h1>Build, inspect, approve, and deliver production agent workflows.</h1>
          <p className="subtle">Planner → Research → Execution → Memory → Human Approval → Final Delivery.</p>
        </div>
        <div className="card goal-card">
          <label htmlFor="goal">User goal</label>
          <textarea id="goal" value={goal} onChange={(event) => setGoal(event.target.value)} />
          <button onClick={submitGoal} disabled={loading}>{loading ? 'Starting...' : 'Start Agent Run'}</button>
        </div>
      </section>

      {run && (
        <section className="grid">
          <article className="card">
            <h2>Status</h2>
            <p className="status">{run.status}</p>
            <p>Current node: <strong>{run.current_node}</strong></p>
            <p>Estimated cost: ${run.cost_summary.estimated_cost_usd.toFixed(2)}</p>
            <p>Total tokens: {run.cost_summary.total_tokens}</p>
          </article>

          <article className="card">
            <h2>Plan</h2>
            {run.tasks.map((task) => <div className="task" key={task.id}><strong>{task.title}</strong><span>{task.risk_level}</span><p>{task.description}</p></div>)}
          </article>

          <article className="card">
            <h2>Research Notes</h2>
            <ul>{run.research_notes.map((note) => <li key={note}>{note}</li>)}</ul>
          </article>

          <article className="card approval">
            <h2><ShieldCheck size={20} /> Human Approval</h2>
            {run.approvals.length ? run.approvals.map((approval) => <div key={approval.id}><p>{approval.proposed_action}</p><p>Risk: {approval.risk_level}</p><p>Status: {approval.status}</p></div>) : <p>No pending approvals.</p>}
            {run.status === 'waiting_for_approval' && <button onClick={approveRun}>Approve and Resume</button>}
          </article>

          {run.final_output && <article className="card delivery"><h2><CheckCircle2 size={20} /> Final Delivery</h2><p>{run.final_output}</p></article>}
        </section>
      )}
    </main>
  );
}

createRoot(document.getElementById('root')!).render(<App />);
