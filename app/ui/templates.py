HTML_MAIN = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Phoenix Laws</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --primary: #90CAF9;
      --primary-dark: #42A5F5;
      --bg: #121212;
      --surface: #1E1E1E;
      --surface-2: #2C2C2C;
      --text: #E0E0E0;
      --text-secondary: #B0B0B0;
      --border: #333;
      --success: #66BB6A;
    }
    body {
      font-family: 'Roboto', sans-serif;
      background-color: var(--bg);
      color: var(--text);
      margin: 0;
      padding: 0;
      line-height: 1.6;
    }
    .app-bar {
      background-color: var(--surface);
      padding: 0 24px;
      height: 64px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      box-shadow: 0 2px 4px rgba(0,0,0,0.3);
      position: sticky;
      top: 0;
      z-index: 100;
    }
    .app-bar-title {
      font-size: 1.25rem;
      font-weight: 500;
      color: var(--primary);
    }
    .nav-links a {
      color: var(--text-secondary);
      text-decoration: none;
      margin-left: 20px;
      font-size: 0.9rem;
      transition: color 0.2s;
    }
    .nav-links a:hover, .nav-links a.active {
      color: var(--primary);
    }
    .container {
      max-width: 900px;
      margin: 24px auto;
      padding: 0 16px;
    }
    .card {
      background: var(--surface);
      border-radius: 8px;
      padding: 24px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.2), 0 2px 8px rgba(0,0,0,0.1);
      margin-bottom: 24px;
      transition: box-shadow 0.3s ease;
    }
    .card:hover {
       box-shadow: 0 4px 6px rgba(0,0,0,0.3), 0 8px 16px rgba(0,0,0,0.1);
    }
    h2 { font-weight: 400; font-size: 1.5rem; margin-top: 0; margin-bottom: 8px; }
    p.subtitle { color: var(--text-secondary); font-size: 0.9rem; margin-bottom: 24px; margin-top: 0; }
    .input-group { position: relative; margin-bottom: 20px; }
    textarea {
      width: 100%;
      background: rgba(255,255,255,0.05);
      border: 1px solid var(--border);
      border-radius: 4px;
      color: var(--text);
      padding: 16px;
      font-family: inherit;
      font-size: 1rem;
      min-height: 120px;
      resize: vertical;
      box-sizing: border-box;
      transition: border-color 0.2s;
    }
    textarea:focus { outline: none; border-color: var(--primary); background: rgba(255,255,255,0.08); }
    label { display: block; margin-bottom: 8px; color: var(--text-secondary); font-size: 0.85rem; font-weight: 500; }
    .controls { display: flex; align-items: center; gap: 24px; flex-wrap: wrap; margin-bottom: 24px; }
    .chip-group { display: flex; gap: 12px; }
    .chip-input { display: none; }
    .chip-label {
      background: var(--surface-2);
      padding: 8px 16px;
      border-radius: 16px;
      font-size: 0.9rem;
      cursor: pointer;
      border: 1px solid transparent;
      transition: all 0.2s;
      user-select: none;
    }
    .chip-input:checked + .chip-label {
      background: rgba(144, 202, 249, 0.15);
      color: var(--primary);
      border-color: var(--primary);
    }
    .switch-label { display: flex; align-items: center; gap: 12px; cursor: pointer; font-size: 0.9rem; }
    .switch {
      position: relative; width: 36px; height: 20px; background: #555; border-radius: 20px; transition: 0.3s;
    }
    .switch::after {
      content: ''; position: absolute; top: 2px; left: 2px; width: 16px; height: 16px; 
      background: #fff; border-radius: 50%; transition: 0.3s;
    }
    input:checked + .switch-label .switch { background: var(--primary-dark); }
    input:checked + .switch-label .switch::after { transform: translateX(16px); }
    .btn {
      background: var(--primary);
      color: #000;
      border: none;
      padding: 10px 24px;
      border-radius: 4px;
      font-size: 0.95rem;
      font-weight: 500;
      text-transform: uppercase;
      letter-spacing: 0.5px;
      cursor: pointer;
      box-shadow: 0 2px 4px rgba(0,0,0,0.2);
      transition: filter 0.2s, box-shadow 0.2s;
    }
    .btn:hover { filter: brightness(1.1); box-shadow: 0 4px 8px rgba(0,0,0,0.3); }
    .btn:disabled { opacity: 0.6; cursor: default; }
    .answer-card {
      background: var(--surface);
      border-radius: 8px;
      padding: 0;
      overflow: hidden;
      margin-top: 24px;
      border: 1px solid var(--border);
    }
    .answer-header {
      background: rgba(255,255,255,0.03);
      padding: 12px 20px;
      border-bottom: 1px solid var(--border);
      display: flex; justify-content: space-between; align-items: center;
    }
    .badge {
      font-size: 0.75rem; padding: 2px 8px; border-radius: 12px; 
      background: rgba(102, 187, 106, 0.2); color: var(--success); border: 1px solid rgba(102, 187, 106, 0.4);
    }
    .answer-body {
      padding: 20px;
      white-space: pre-wrap;
      font-family: 'Roboto', sans-serif; 
      font-size: 0.95rem;
      color: #dcdcdc;
    }
    .sources-box {
      margin-top: 16px;
      padding: 16px;
      background: #151515;
      border-top: 1px solid var(--border);
      font-size: 0.85rem;
    }
    .source-link { color: var(--primary); text-decoration: none; }
    .source-link:hover { text-decoration: underline; }
    .status-text { color: var(--text-secondary); font-size: 0.9rem; margin-top: 8px; font-style: italic; }
  </style>
</head>
<body>
  <div class="app-bar">
    <div class="app-bar-title">Phoenix Laws</div>
    <div class="nav-links">
      <a href="/ui" class="active">Laws</a>
      <a href="/ui/intake">Intake</a>
      <a href="/ui/contracts">Contracts</a>
      <a href="/ui/mapper">Mapper</a>
    </div>
  </div>

  <div class="container">
    <div class="card">
      <h2>Legal Research (Laws)</h2>
      <p class="subtitle">Select jurisdictions to retrieve relevant statutory text and explanations.</p>
      
      <div class="input-group">
        <label for="question">YOUR QUESTION</label>
        <textarea id="question" placeholder="e.g., What are the requirements for data breach notification in Michigan?"></textarea>
      </div>

      <div class="controls">
        <div>
            <label>JURISDICTIONS</label>
            <div class="chip-group">
                <label>
                    <input type="checkbox" id="p_mi" class="chip-input" checked>
                    <span class="chip-label">Michigan</span>
                </label>
                <label>
                    <input type="checkbox" id="p_ca" class="chip-input">
                    <span class="chip-label">California</span>
                </label>
            </div>
        </div>
        
        <div style="margin-top:24px;"> <input type="checkbox" id="use_rag" style="display:none;">
           <label for="use_rag" class="switch-label">
             <div class="switch"></div>
             <span>Use Knowledge Base (RAG)</span>
           </label>
        </div>
      </div>

      <button id="ask_btn" class="btn">Pull Statutes</button>
      <div id="status" class="status-text"></div>
    </div>

    <div id="answers"></div>
    
    <div style="text-align:center; color: #555; font-size: 0.75rem; margin-top: 40px;">
        CONFIDENTIAL &bull; INTERNAL DEMO ONLY &bull; NOT LEGAL ADVICE
    </div>
    <div style="text-align:center; color: #666; font-size: 0.75rem; margin: 5px 0 20px 0;">
        AI generated, can make mistakes. Check important info.
    </div>
  </div>

  <script>
    async function askAgents() {
      const btn = document.getElementById("ask_btn");
      const status = document.getElementById("status");
      const answersDiv = document.getElementById("answers");
      const q = document.getElementById("question").value.trim();
      const useRag = document.getElementById("use_rag").checked;

      const personas = [];
      if (document.getElementById("p_mi").checked) personas.push("mi");
      if (document.getElementById("p_ca").checked) personas.push("ca");

      if (!q) {
        status.textContent = "Please enter a question.";
        return;
      }
      if (personas.length === 0) {
        status.textContent = "Select at least one jurisdiction.";
        return;
      }

      btn.disabled = true;
      status.textContent = "Searching statutes and generating response...";
      answersDiv.innerHTML = "";

      try {
        const resp = await fetch("/api/legal/query", {
          method: "POST",
          headers: {"Content-Type": "application/json"},
          body: JSON.stringify({
            question: q,
            personas: personas,
            use_rag: useRag
          })
        });
        if (!resp.ok) {
          const t = await resp.text();
          status.textContent = "Error: " + t;
          btn.disabled = false;
          return;
        }
        const data = await resp.json();
        status.textContent = "";

        data.answers.forEach(ans => {
          const card = document.createElement("div");
          card.className = "answer-card";

          const header = document.createElement("div");
          header.className = "answer-header";
          
          header.innerHTML = `
            <span style="font-weight:500; color:white;">${ans.label}</span>
            <span class="badge">${data.used_rag ? "RAG ACTIVE" : "NO RAG"}</span>
          `;

          const body = document.createElement("div");
          body.className = "answer-body";
          body.textContent = ans.answer;

          card.appendChild(header);
          card.appendChild(body);
          answersDiv.appendChild(card);
        });

        if (data.used_rag && data.sources && data.sources.length) {
          const srcDiv = document.createElement("div");
          srcDiv.className = "sources-box";
          let html = "<div style='color:var(--text-secondary); margin-bottom:12px; font-weight:500;'>CITATIONS & SOURCES</div>";
          
          data.sources.forEach(s => {
             let displayTitle = s.title;
             if (!displayTitle) {
                  displayTitle = s.source.split('/').pop().replace('.md', '').replace(/_/g, ' ').toUpperCase();
             }
             const label = s.jurisdiction === "MI" ? "Michigan" : s.jurisdiction === "CA" ? "California" : "Ref";
             
             let action = "";
             if (s.url && s.url.startsWith("http")) {
                 action = `<a href="${s.url}" class="source-link" target="_blank">[Official Source]</a>`;
             } else {
                 action = `<span style="font-size:0.8rem; color:#666;">(No online link available)</span>`;
             }
             
             html += `<div style="margin-bottom:12px; font-family:'Roboto', sans-serif; font-size:0.9rem; border-left:3px solid #444; padding-left:12px;">
                <div style="font-weight:500; color:#e0e0e0;">${displayTitle} <span style="font-size:0.75em; color:#888; margin-left:8px; text-transform:uppercase;">${label}</span></div>
                <div style="margin-top:2px;">${action}</div>
             </div>`;
          });
          srcDiv.innerHTML = html;
          answersDiv.appendChild(srcDiv);
        }

      } catch (err) {
        console.error(err);
        status.textContent = "Network error: " + err;
      } finally {
        btn.disabled = false;
      }
    }

    document.getElementById("ask_btn").addEventListener("click", askAgents);
    document.getElementById("use_rag").checked = true;
  </script>
</body>
</html>
"""

HTML_INTAKE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Phoenix Intake Engine</title>
  <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=Roboto+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root {
      --primary: #90CAF9;
      --bg: #121212;
      --surface: #1E1E1E;
      --surface-2: #2C2C2C;
      --text: #E0E0E0;
      --text-sec: #A0A0A0;
      --border: #333;
      --accent: #BB86FC;
    }
    * { box-sizing: border-box; }
    body {
      font-family: 'Roboto', sans-serif;
      background-color: var(--bg);
      color: var(--text);
      margin: 0; padding: 0;
    }
    .app-bar {
      background-color: var(--surface);
      padding: 0 24px;
      height: 64px;
      display: flex; align-items: center; justify-content: space-between;
      box-shadow: 0 2px 4px rgba(0,0,0,0.3);
      position: sticky; top: 0; z-index: 100;
    }
    .app-bar-title { font-size: 1.25rem; font-weight: 500; color: var(--accent); }
    .nav-links a { color: var(--text-sec); text-decoration: none; margin-left: 20px; font-size: 0.9rem; transition: 0.2s; }
    .nav-links a:hover, .nav-links a.active { color: var(--accent); }
    .main { max-width: 1200px; margin: 24px auto; padding: 0 16px; display: grid; grid-template-columns: 1fr 380px; gap: 24px; }
    @media (max-width: 900px) { .main { grid-template-columns: 1fr; } }
    .card {
      background: var(--surface); border-radius: 8px; padding: 24px;
      box-shadow: 0 1px 3px rgba(0,0,0,0.2); margin-bottom: 24px;
    }
    h3 { font-size: 1.1rem; font-weight: 500; margin: 0 0 16px 0; color: var(--text); border-bottom: 1px solid var(--border); padding-bottom: 8px; }
    .field { margin-bottom: 16px; }
    label { display: block; font-size: 0.75rem; font-weight: 500; color: var(--text-sec); margin-bottom: 6px; letter-spacing: 0.5px; text-transform: uppercase; }
    input[type="text"], textarea {
      width: 100%; background: #121212; border: 1px solid var(--border);
      color: var(--text); padding: 12px; border-radius: 4px; font-family: 'Roboto', sans-serif; font-size: 0.9rem;
      transition: border-color 0.2s;
    }
    input[type="text"]:focus, textarea:focus { outline: none; border-color: var(--accent); }
    textarea { min-height: 150px; resize: vertical; }
    .btn {
      background: linear-gradient(135deg, #7C4DFF, #448AFF);
      color: white; border: none; padding: 12px 24px; border-radius: 4px;
      font-size: 0.95rem; font-weight: 500; letter-spacing: 0.5px; cursor: pointer;
      width: 100%; text-transform: uppercase; box-shadow: 0 4px 6px rgba(0,0,0,0.3);
      transition: transform 0.1s, box-shadow 0.2s;
    }
    .btn:hover { box-shadow: 0 6px 12px rgba(0,0,0,0.4); }
    .btn:active { transform: translateY(1px); }
    .btn.small { width: auto; padding: 6px 12px; font-size: 0.75rem; background: var(--surface-2); border: 1px solid var(--border); box-shadow: none; margin-top: 8px; }
    .btn.small:hover { background: #333; }
    .team-card {
      background: var(--surface-2); border-radius: 6px; padding: 12px; margin-bottom: 12px; border: 1px solid var(--border);
    }
    .team-name { font-weight: 700; color: #fff; margin-bottom: 8px; display: flex; justify-content: space-between; font-size: 0.95rem; }
    .skill-row { display: flex; align-items: center; margin-bottom: 8px; font-size: 0.8rem; }
    .skill-lbl { width: 80px; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; color: var(--text-sec); }
    .skill-val { width: 30px; text-align: right; margin-right: 8px; font-family: 'Roboto Mono', monospace; }
    input[type=range] { flex: 1; margin: 0 8px; accent-color: var(--accent); cursor: pointer; }
    #results { margin-top: 24px; }
    .res-section { margin-bottom: 20px; }
    .res-label { color: var(--text-sec); font-size: 0.8rem; margin-bottom: 4px; }
    .res-val { font-size: 1rem; color: #fff; }
    .priority-badge {
        display: inline-block; padding: 4px 12px; border-radius: 4px; font-weight: bold; text-transform: uppercase; font-size: 0.8rem;
    }
    .p-Critical { background: rgba(244, 67, 54, 0.2); color: #ef5350; border: 1px solid #ef5350; }
    .p-High { background: rgba(255, 167, 38, 0.2); color: #ffa726; border: 1px solid #ffa726; }
    .p-Medium { background: rgba(102, 187, 106, 0.2); color: #66bb6a; border: 1px solid #66bb6a; }
    .p-Low { background: rgba(41, 182, 246, 0.2); color: #29b6f6; border: 1px solid #29b6f6; }
    .cat-chip {
        display: inline-block; background: #333; padding: 4px 10px; border-radius: 12px; font-size: 0.8rem; margin-right: 6px; border: 1px solid #444;
    }
    .csuite-box { background: rgba(187, 134, 252, 0.08); border-left: 3px solid var(--accent); padding: 8px 12px; font-size: 0.9rem; margin-top: 4px; }
    pre { background: #000; padding: 12px; border-radius: 4px; font-family: 'Roboto Mono', monospace; font-size: 0.8rem; color: #ccc; overflow-x: auto; border: 1px solid #333; }
    .json-area { font-family: 'Roboto Mono'; font-size: 0.75rem; min-height: 80px; }
    input[type="file"] { display: none; }
  </style>
</head>
<body>
  <div class="app-bar">
    <div class="app-bar-title">Intake</div>
    <div class="nav-links">
      <a href="/ui">Laws</a>
      <a href="/ui/intake" class="active">Intake</a>
      <a href="/ui/contracts">Contracts</a>
      <a href="/ui/mapper">Mapper</a>
    </div>
  </div>

  <div class="main">
    <div>
       <div class="card">
         <h3>Inbound Analysis</h3>
         <div class="field">
           <label>Organization (Optional)</label>
           <input type="text" id="org" placeholder="e.g. Acme Corp">
         </div>
         <div class="field">
           <label>Inbound Message / Email Body</label>
           <textarea id="email_text" placeholder="Paste the full email or request here..."></textarea>
         </div>
         <div class="field">
            <label>Notify Email (Optional)</label>
            <input type="text" id="notify_email" placeholder="result@example.com">
         </div>
         <button id="analyze_btn" class="btn">Analyze & Route</button>
         <div id="status" style="margin-top:12px; font-size:0.9rem; color: var(--text-sec); font-style: italic;"></div>
       </div>

       <div id="results"></div>
       
       <div class="card" style="margin-top:24px;">
         <h3>Configuration Context</h3>
         <div class="field">
            <label>Playbook / Reference Notes (Overrides Team Routing if specific)</label>
            <textarea id="ref_notes" style="min-height:80px; font-size:0.85rem;"></textarea>
         </div>
         <div class="field">
            <label>Watchlist (C-Suite)</label>
            <input type="text" id="csuite" placeholder="e.g. CEO, Jane Doe">
         </div>
       </div>
    </div>

    <div>
      <div class="card">
        <h3>Team Routing Profile</h3>
        <p style="font-size:0.8rem; color:var(--text-sec); margin-bottom:16px;">
           Configure team skills to simulate routing logic. Adjust mastery (0-100).
        </p>
        <div id="team_profile_container"></div>
        <button class="btn small" id="btn_add_member">+ Add Member</button>
        <div style="margin-top:24px; border-top:1px solid var(--border); padding-top:16px;">
            <label>JSON Profile Import/Export</label>
            <textarea id="team_json" class="json-area"></textarea>
            <div style="display:flex; gap:8px; flex-wrap:wrap;">
                <button class="btn small" id="btn_team_apply">Apply Text</button>
                <button class="btn small" id="btn_team_reset">Reset</button>
                <label for="import_file" class="btn small" style="cursor:pointer; display:inline-block; text-align:center;">
                   Import JSON File
                </label>
                <input type="file" id="import_file" accept=".json">
            </div>
        </div>
      </div>
    </div>
  </div>
  
    <div style="text-align:center; color: #555; font-size: 0.75rem; margin-top: 40px;">
        CONFIDENTIAL &bull; INTERNAL DEMO ONLY &bull; NOT LEGAL ADVICE
    </div>
    <div style="text-align:center; color: #666; font-size: 0.75rem; margin: 5px 0 20px 0;">
        AI generated, can make mistakes. Check important info.
    </div>
  </div>

  <script>
    const defaultNotes = "# Playbook & Routing Rules\\n\\n## 1. Commercial & Contracts\\n- Keywords: contract, agreement, sow, msa, nda, negotiation, renewal\\n- Primary Owner: Ron\\n- Priority: Medium (unless 'urgent' or 'today' mentioned)\\n\\n## 2. Privacy & Cybersecurity\\n- Keywords: breach, incident, gdpr, ccpa, dpa, security, privacy\\n- Primary Owner: Shawn\\n- Priority: High (Critical if 'breach' or 'incident')\\n\\n## 3. Data & Compliance\\n- Keywords: analytics, ai, data usage, compliance, audit, tax\\n- Primary Owner: Doug\\n- Priority: Medium\\n\\n## 4. Litigation & Disputes\\n- Keywords: lawsuit, subpoena, court, dispute, cease and desist\\n- Primary Owner: Ron\\n- Priority: High";
    
    const defaultTeamProfile = {
      members: [
        {
          name: "Shawn",
          skills: [
            { label: "saas", mastery: 95 },
            { label: "cybersecurity", mastery: 95 },
            { label: "privacy", mastery: 95 },
            { label: "contracts", mastery: 100 },
            { label: "ai", mastery: 100 },
            { label: "real estate", mastery: 55 }           
          ]
        },
        {
          name: "Ron",
          skills: [
            { label: "negotiating", mastery: 95 },
            { label: "contracts", mastery: 95 },
            { label: "litigation", mastery: 95 },
            { label: "real estate", mastery: 95 }
          ]
        },
        {
          name: "Russell",
          skills: [
            { label: "open source", mastery: 95 },
            { label: "compliance", mastery: 95 },
            { label: "litigation", mastery: 85 }
            ]
        }
      ]
    };

    let teamProfile = JSON.parse(JSON.stringify(defaultTeamProfile));

    document.addEventListener("DOMContentLoaded", () => {
      const ref = document.getElementById("ref_notes");
      if (ref && !ref.value.trim()) ref.value = defaultNotes;
      renderTeamProfile();
      document.getElementById("btn_team_reset").addEventListener("click", () => {
         teamProfile = JSON.parse(JSON.stringify(defaultTeamProfile));
         renderTeamProfile();
      });
      document.getElementById("btn_team_apply").addEventListener("click", applyTeamFromJson);
      document.getElementById("btn_add_member").addEventListener("click", addMember);
      document.getElementById("analyze_btn").addEventListener("click", analyzeIntake);
      document.getElementById("import_file").addEventListener("change", handleFileImport);
    });

    function renderTeamProfile() {
      const container = document.getElementById("team_profile_container");
      container.innerHTML = "";
      teamProfile.members.forEach((member, mi) => {
        const card = document.createElement("div");
        card.className = "team-card";
        const header = document.createElement("div");
        header.className = "team-name";
        header.innerHTML = `<span>${member.name}</span> <span style='cursor:pointer; opacity:0.5;' onclick='removeMember(${mi})'>&times;</span>`;
        card.appendChild(header);
        
        member.skills.forEach((skill, si) => {
           const row = document.createElement("div");
           row.className = "skill-row";
           const lbl = document.createElement("div");
           lbl.className = "skill-lbl";
           lbl.textContent = skill.label;
           lbl.title = skill.label;
           const slider = document.createElement("input");
           slider.type = "range"; slider.min=0; slider.max=100;
           slider.value = skill.mastery;
           slider.oninput = (e) => {
              teamProfile.members[mi].skills[si].mastery = parseInt(e.target.value);
              valDisp.textContent = e.target.value;
              syncJson();
           };
           const valDisp = document.createElement("div");
           valDisp.className = "skill-val";
           valDisp.textContent = skill.mastery;
           row.appendChild(lbl);
           row.appendChild(slider);
           row.appendChild(valDisp);
           card.appendChild(row);
        });
        
        const addSkillBtn = document.createElement("div");
        addSkillBtn.style.textAlign = "center";
        addSkillBtn.innerHTML = "<span style='font-size:0.7rem; color:#666; cursor:pointer;'>+ Add Skill</span>";
        addSkillBtn.onclick = () => addSkill(mi);
        card.appendChild(addSkillBtn);
        container.appendChild(card);
      });
      syncJson();
    }
    
    function addSkill(mi) {
        const lbl = prompt("Skill Name (e.g. litigation)");
        if(lbl) {
            teamProfile.members[mi].skills.push({ label: lbl, mastery: 50 });
            renderTeamProfile();
        }
    }
    
    function addMember() {
        const name = prompt("Member Name:");
        if(name) {
            teamProfile.members.push({ name: name, skills: [] });
            renderTeamProfile();
        }
    }
    
    window.removeMember = function(mi) {
        if(confirm("Remove this member?")) {
            teamProfile.members.splice(mi, 1);
            renderTeamProfile();
        }
    };
    
    function syncJson() {
        document.getElementById("team_json").value = JSON.stringify(teamProfile, null, 2);
    }
    
    function applyTeamFromJson() {
        try {
            const parsed = JSON.parse(document.getElementById("team_json").value);
            if(parsed && parsed.members) {
                teamProfile = parsed;
                renderTeamProfile();
            }
        } catch(e) { alert("Invalid JSON"); }
    }
    
    function handleFileImport(e) {
        const file = e.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = function(evt) {
            try {
                const parsed = JSON.parse(evt.target.result);
                if (parsed && parsed.members) {
                    teamProfile = parsed;
                    renderTeamProfile();
                    alert("Team profile imported successfully.");
                } else {
                    alert("Invalid JSON format. Must contain 'members' array.");
                }
            } catch(err) {
                alert("Error parsing JSON file: " + err);
            }
        };
        reader.readAsText(file);
        e.target.value = '';
    }

    async function analyzeIntake() {
       const btn = document.getElementById("analyze_btn");
       const status = document.getElementById("status");
       const resultsDiv = document.getElementById("results");
       const email = document.getElementById("email_text").value;
       if(!email.trim()) { alert("Please enter message text."); return; }
       
       btn.disabled = true;
       status.textContent = " Analyzing content & routing...";
       resultsDiv.innerHTML = "";
       
       const payload = {
           email_text: email,
           reference_notes: document.getElementById("ref_notes").value,
           organization_name: document.getElementById("org").value,
           csuite_names: document.getElementById("csuite").value.split(",").map(s=>s.trim()).filter(s=>s),
           max_categories: 5,
           notify_email: document.getElementById("notify_email").value,
           team_profile: teamProfile
       };
       
       try {
           const res = await fetch("/api/intake/analyze", {
               method: "POST",
               headers: {"Content-Type": "application/json"},
               body: JSON.stringify(payload)
           });
           const data = await res.json();
           
           status.textContent = " Analysis complete.";
           const card = document.createElement("div");
           card.className = "card";
           card.style.borderTop = "4px solid var(--accent)";
           
           const pLabel = data.priority_label || "Normal";
           const pClass = "p-" + pLabel;
           
           let html = `
             <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
                <h3>Analysis Result</h3>
                <span class="priority-badge ${pClass}">${pLabel} (${data.priority_score}/10)</span>
             </div>
           `;
           
           html += `<div class="res-section"><div class="res-label">CATEGORIES</div>`;
           if(data.categories && data.categories.length) {
               data.categories.forEach(c => { html += `<span class="cat-chip">${c}</span>`; });
           } else { html += `<span style="color:#666">None</span>`; }
           html += `</div>`;
           
           html += `<div class="res-section"><div class="res-label">SUMMARY</div><div class="res-val" style="line-height:1.4">${data.summary}</div></div>`;
           
           if(data.csuite_mentions && data.csuite_mentions.length > 0) {
              html += `<div class="res-section"><div class="res-label">EXECUTIVE MENTIONS</div>`;
              data.csuite_mentions.forEach(m => {
                  html += `<div class="csuite-box"><strong>${m.name}</strong> detected.</div>`;
              });
              html += `</div>`;
           }
           
           html += `<div class="res-section" style="background:#222; padding:12px; border-radius:6px; border:1px solid #333;">
              <div class="res-label" style="color:var(--primary);">SUGGESTED OWNER</div>
              <div style="font-size:1.1rem; font-weight:bold; color:#fff;">${data.suggested_owner || 'Unassigned'}</div>`;
              
           if(data.suggested_backup) {
              html += `<div style="font-size:0.85rem; color:#aaa; margin-top:4px;">Backup: ${data.suggested_backup}</div>`;
           }
           if(data.learning_opportunities && data.learning_opportunities.length) {
              html += `<div style="font-size:0.85rem; color:var(--accent); margin-top:8px;">Suggested Training: ${data.learning_opportunities.join(", ")}</div>`;
           }
           html += `</div>`;
           
           if(data.suggested_next_steps) {
               html += `<div class="res-section"><div class="res-label">NEXT STEPS</div><pre style="white-space:pre-wrap; background:#1a1a1a;">${data.suggested_next_steps}</pre></div>`;
           }
           
           if(data.email_status) {
              html += `<div style="font-size:0.75rem; color:#666; text-align:right;">Email Notification: ${data.email_status}</div>`;
           }
           
           if (data.original_text) {
               html += `<div class="res-section" style="margin-top:20px; padding-top:16px; border-top:1px solid #333;">
                  <div class="res-label" style="margin-bottom:8px;">ORIGINAL REQUEST</div>
                  <div style="font-size:0.85rem; color:#bbb; white-space:pre-wrap; background:#111; padding:12px; border-radius:4px; font-family:'Roboto Mono', monospace;">${data.original_text}</div>
               </div>`;
           }

           card.innerHTML = html;
           resultsDiv.appendChild(card);
           
       } catch(e) {
           console.error(e);
           status.textContent = "Error: " + e;
       } finally {
           btn.disabled = false;
       }
    }
  </script>
</body>
</html>
"""

HTML_CONTRACTS = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Phoenix Contracts</title>
  <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=Roboto+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root { --primary: #90CAF9; --bg: #121212; --surface: #1E1E1E; --surface-2: #2C2C2C; --text: #E0E0E0; --text-sec: #A0A0A0; --border: #333; --accent: #FFA500; }
    * { box-sizing: border-box; }
    body { font-family: 'Roboto', sans-serif; background-color: var(--bg); color: var(--text); margin: 0; padding: 0; }
    
    .app-bar { background-color: var(--surface); padding: 0 24px; height: 64px; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 2px 4px rgba(0,0,0,0.3); position: sticky; top: 0; z-index: 100; }
    .app-bar-title { font-size: 1.25rem; font-weight: 500; color: var(--accent); }
    .nav-links a { color: var(--text-sec); text-decoration: none; margin-left: 20px; font-size: 0.9rem; transition: 0.2s; }
    .nav-links a.active { color: var(--accent); }

    .main { max-width: 1100px; margin: 24px auto; padding: 0 16px; display: grid; grid-template-columns: 2fr 1fr; gap: 24px; }
    @media (max-width: 900px) { .main { grid-template-columns: 1fr; } }

    .card { background: var(--surface); border-radius: 8px; padding: 24px; box-shadow: 0 1px 3px rgba(0,0,0,0.2); margin-bottom: 24px; }
    h2 { font-weight: 400; font-size: 1.3rem; margin: 0 0 16px 0; color: var(--text); border-bottom: 1px solid var(--border); padding-bottom: 8px; }
    
    .field { margin-bottom: 16px; }
    label { display: block; font-size: 0.8rem; font-weight: 500; color: var(--text-sec); margin-bottom: 8px; text-transform: uppercase; }
    select, input[type=file], input[type=text] { width: 100%; padding: 10px; background: var(--surface-2); border: 1px solid var(--border); color: var(--text); border-radius: 4px; font-size: 0.9rem; }
    textarea { width: 100%; padding: 10px; background: var(--surface-2); border: 1px solid var(--border); color: var(--text); border-radius: 4px; font-size: 0.9rem; min-height: 150px; font-family: 'Roboto Mono', monospace; }
    
    .btn { background: var(--accent); color: #000; border: none; padding: 12px 24px; border-radius: 4px; font-size: 0.95rem; font-weight: 500; cursor: pointer; width: 100%; text-transform: uppercase; box-shadow: 0 2px 4px rgba(0,0,0,0.2); }
    .btn:hover { filter: brightness(1.1); }
    .btn:disabled { opacity: 0.6; cursor: not-allowed; }
    .btn-small { padding: 6px 12px; font-size: 0.8rem; width: auto; }
    .btn-danger { background: #ef5350; color: white; }

    /* Analysis Results */
    .analysis-item { background: #252525; border-left: 4px solid #555; margin-bottom: 15px; padding: 15px; border-radius: 4px; }
    .analysis-item.has-changes { border-left-color: #ef5350; }
    .clause-label { font-size: 0.75rem; color: #888; text-transform: uppercase; font-weight: bold; margin-bottom: 6px; }
    .clause-box { font-family: 'Roboto Mono', monospace; font-size: 0.8rem; background: #111; padding: 10px; border-radius: 4px; color: #ccc; white-space: pre-wrap; max-height: 200px; overflow-y: auto; border: 1px solid #333; }
    .change-row { margin-bottom: 8px; font-family: 'Roboto Mono', monospace; font-size: 0.85rem; display: flex; align-items: flex-start; margin-top: 8px; }
    .badge { display: inline-block; padding: 2px 6px; border-radius: 3px; font-size: 0.7em; font-weight: bold; margin-right: 10px; min-width: 70px; text-align: center; flex-shrink: 0; }
    .badge.ins { background: rgba(102, 187, 106, 0.15); color: #66bb6a; border: 1px solid #66bb6a; }
    .badge.del { background: rgba(239, 83, 80, 0.15); color: #ef5350; border: 1px solid #ef5350; }
    .badge.rep { background: rgba(255, 167, 38, 0.15); color: #ffa726; border: 1px solid #ffa726; }
    .badge.cmt { background: rgba(66, 165, 245, 0.15); color: #42a5f5; border: 1px solid #42a5f5; }
    
    /* Persona List in Sidebar */
    .persona-list-item { padding: 10px; background: var(--surface-2); margin-bottom: 8px; border-radius: 4px; cursor: pointer; border: 1px solid transparent; display: flex; justify-content: space-between; align-items: center; }
    .persona-list-item:hover { border-color: var(--primary); }
    .persona-list-item.active { background: rgba(144, 202, 249, 0.15); border-color: var(--primary); color: var(--primary); }
  </style>
</head>
<body>
  <div class="app-bar">
    <div class="app-bar-title">Contract Redline</div>
    <div class="nav-links">
      <a href="/ui">Laws</a>
      <a href="/ui/intake">Intake</a>
      <a href="/ui/contracts" class="active">Contracts</a>
      <a href="/ui/mapper">Mapper</a>
    </div>
  </div>

  <div class="main">
    
    <div>
      <div class="card">
        <h2>1. Upload & Configure</h2>
        
        <div class="field">
          <label>Counterparty DOCX (Required)</label>
          <input id="counterparty" type="file" accept=".docx">
        </div>
        <div class="field">
          <label>Template DOCX (Optional)</label>
          <input id="template" type="file" accept=".docx">
        </div>

        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
            <div class="field">
              <label>Our Role</label>
              <select id="role_select">
                  <option value="Buyer">Buyer / Client</option>
                  <option value="Seller">Seller / Provider</option>
              </select>
            </div>
            <div class="field">
              <label>Persona</label>
              <select id="persona_select">
                  <option value="General Counsel">General Counsel</option>
                  </select>
            </div>
        </div>

        <button class="btn" id="analyze_btn" onclick="runRedline()">Analyze Contract</button>
      </div>

      <div class="card" style="border-top: 4px solid var(--accent); min-height:100px;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 20px;">
            <h2 style="margin:0; border:none;">2. Analysis Result</h2>
            <div id="export_area" style="display:none; display:flex; gap:12px;">
                <button class="btn btn-small" style="background:#66BB6A;" onclick="downloadRedline()">Download Redline</button>
                <button class="btn btn-small" style="background:#42A5F5;" onclick="downloadReport()">Download Report</button>
            </div>
        </div>
        <div id="status_text" style="color:#777; font-style:italic;">Analysis will take a few minutes to complete. Ready to analyze...</div>
        <div id="output"></div>
      </div>
    </div>

    <div>
      <div class="card">
        <h2>Persona Library</h2>
        <div id="persona_list"></div>
        <button class="btn btn-small" style="margin-top:12px; width:100%; background:#444;" onclick="createNewPersona()">+ New Persona</button>
      </div>

      <div class="card" id="editor_card" style="display:none;">
        <h2 style="font-size:1rem;">Edit Persona</h2>
        <div class="field">
            <label>Name</label>
            <input type="text" id="edit_name">
        </div>
        <div class="field">
            <label>Instructions / Strategy</label>
            <textarea id="edit_instructions"></textarea>
        </div>
        <div style="display:flex; gap:8px;">
            <button class="btn btn-small" onclick="savePersona()">Save</button>
            <button class="btn btn-small btn-danger" onclick="deletePersona()">Delete</button>
        </div>
      </div>
    </div>

  </div>
  
    <div style="text-align:center; color: #555; font-size: 0.75rem; margin-top: 40px;">
        CONFIDENTIAL &bull; INTERNAL DEMO ONLY &bull; NOT LEGAL ADVICE
    </div>
    <div style="text-align:center; color: #666; font-size: 0.75rem; margin: 5px 0 20px 0;">
        AI generated, can make mistakes. Check important info.
    </div>
  </div>

  <script>
    let lastAnalysisData = null;
    let lastUploadedFile = null;
    let availablePersonas = [];

    // --- Init ---
    document.addEventListener("DOMContentLoaded", () => {
        loadPersonas();
    });

    async function loadPersonas() {
        try {
            const res = await fetch("/api/contracts/personas");
            const data = await res.json();
            availablePersonas = data;
            renderPersonaList();
            renderPersonaSelect();
        } catch(e) { console.error("Failed to load personas", e); }
    }

    function renderPersonaList() {
        const list = document.getElementById("persona_list");
        list.innerHTML = "";
        availablePersonas.forEach(p => {
            const div = document.createElement("div");
            div.className = "persona-list-item";
            div.innerText = p.name;
            div.onclick = () => openEditor(p);
            list.appendChild(div);
        });
    }

    function renderPersonaSelect() {
        const sel = document.getElementById("persona_select");
        const currentVal = sel.value; 
        sel.innerHTML = "";
        availablePersonas.forEach(p => {
            const opt = document.createElement("option");
            opt.value = p.name;
            opt.innerText = p.name;
            sel.appendChild(opt);
        });
        if (availablePersonas.find(p => p.name === currentVal)) {
            sel.value = currentVal;
        }
    }

    // --- Editor Logic ---
    function openEditor(persona) {
        document.getElementById("editor_card").style.display = "block";
        document.getElementById("edit_name").value = persona.name;
        document.getElementById("edit_name").disabled = true; // Edit existing by name lock
        document.getElementById("edit_instructions").value = persona.instructions;
    }

    function createNewPersona() {
        document.getElementById("editor_card").style.display = "block";
        document.getElementById("edit_name").value = "";
        document.getElementById("edit_name").disabled = false;
        document.getElementById("edit_instructions").value = "Tone: ...\\nStrategy: ...";
    }

    async function savePersona() {
        const name = document.getElementById("edit_name").value;
        const instr = document.getElementById("edit_instructions").value;
        if(!name) return alert("Name required");

        await fetch("/api/contracts/personas", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ name: name, instructions: instr })
        });
        loadPersonas();
        alert("Saved");
    }

    async function deletePersona() {
        const name = document.getElementById("edit_name").value;
        if(!confirm("Delete " + name + "?")) return;
        
        await fetch("/api/contracts/personas/" + encodeURIComponent(name), { method: "DELETE" });
        document.getElementById("editor_card").style.display = "none";
        loadPersonas();
    }

    // --- Redline Logic ---
    
    async function runRedline() {
        const output = document.getElementById("output");
        const status = document.getElementById("status_text");
        const btn = document.getElementById("analyze_btn");
        const cpFile = document.getElementById("counterparty").files[0];
        
        if (!cpFile) return alert("Upload a counterparty DOCX!");

        output.innerHTML = "";
        document.getElementById("export_area").style.display = "none";
        status.innerText = "Uploading & Analyzing...";
        btn.disabled = true;
        lastUploadedFile = cpFile;

        const formData = new FormData();
        formData.append("counterparty", cpFile);
        const tpFile = document.getElementById("template").files[0];
        if (tpFile) formData.append("template", tpFile);

        try {
            // 1. Upload
            const upRes = await fetch("/api/contracts/redline/upload", { method: "POST", body: formData });
            if (!upRes.ok) throw new Error(await upRes.text());
            const upData = await upRes.json();

            // 2. Analyze
            const payload = {
                counterparty_text: upData.counterparty_text,
                template_text: upData.template_text,
                mode: "template_only", 
                persona: document.getElementById("persona_select").value,
                role: document.getElementById("role_select").value // NEW
            };

            const anRes = await fetch("/api/contracts/redline/analyze", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });
            
            if (!anRes.ok) throw new Error(await anRes.text());
            const data = await anRes.json();
            
            lastAnalysisData = data.diff;
            status.innerText = `Analysis Complete. ${data.diff.length} issues found.`;
            status.style.color = "#66BB6A";
            
            // Show Export Area with Flex for buttons
            const exp = document.getElementById("export_area");
            exp.style.display = "flex";
            exp.style.gap = "12px";
            
            renderResults(data.diff);

        } catch(e) {
            status.innerText = "Error: " + e.message;
            status.style.color = "#ef5350";
        } finally {
            btn.disabled = false;
        }
    }

    function renderResults(diffs) {
        const container = document.getElementById("output");
        if (!diffs || diffs.length === 0) return container.innerHTML = "<div style='padding:20px; text-align:center;'>No redlines or issues found (Contract looks clean).</div>";

        diffs.forEach(item => {
            const d = item.delta || {};
            const ins = d.insertions || [];
            const del = d.deletions || [];
            const rep = d.replacements || [];
            const cmt = d.comments || [];
            const hasChanges = (ins.length + del.length + rep.length + cmt.length) > 0;

            const card = document.createElement("div");
            card.className = "analysis-item" + (hasChanges ? " has-changes" : "");
            
            let html = `<div><div class="clause-label">Clause</div><div class="clause-box">${item.cp_text || "(New Clause)"}</div></div>`;
            
            if (hasChanges) {
                ins.forEach(x => html += `<div class="change-row"><span class="badge ins">INSERT</span><span>${x}</span></div>`);
                del.forEach(x => html += `<div class="change-row"><span class="badge del">DELETE</span><span>${x}</span></div>`);
                rep.forEach(x => html += `<div class="change-row"><span class="badge rep">REPLACE</span><span>"${x.from}" &rarr; "${x.to}"</span></div>`);
                cmt.forEach(x => html += `<div class="change-row"><span class="badge cmt">NOTE</span><span>${x}</span></div>`);
            } else {
                html += `<div style="margin-top:8px; font-size:0.8rem; color:#666;">No issues found.</div>`;
            }
            card.innerHTML = html;
            container.appendChild(card);
        });
    }

    async function downloadRedline() {
        if (!lastAnalysisData) return;
        const toBase64 = file => new Promise((resolve, reject) => {
            const r = new FileReader(); r.readAsDataURL(file);
            r.onload = () => resolve(r.result.split(',')[1]); r.onerror = reject;
        });
        
        try {
            const b64 = await toBase64(lastUploadedFile);
            const res = await fetch("/api/contracts/redline/export", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ original_docx_base64: b64, diff: lastAnalysisData })
            });
            if(!res.ok) throw new Error(await res.text());
            
            const blob = await res.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a"); a.href = url; a.download = "redlined.docx";
            document.body.appendChild(a); a.click(); document.body.removeChild(a);
        } catch(e) { alert(e); }
    }
    
    async function downloadReport() {
        if (!lastAnalysisData) return;
        try {
            const res = await fetch("/api/contracts/redline/export-report", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ diff: lastAnalysisData })
            });
            if(!res.ok) throw new Error(await res.text());
            
            const blob = await res.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a"); a.href = url; a.download = "Analysis_Report.docx";
            document.body.appendChild(a); a.click(); document.body.removeChild(a);
        } catch(e) { alert(e); }
    }
  </script>
</body>
</html>
"""

HTML_MAPPER = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<title>Phoenix Data Mapper</title>

<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=Roboto+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">

<style>
  :root {
    --primary: #03DAC6;
    --bg: #121212;
    --surface: #1E1E1E;
    --border: #333;
    --accent: #BB86FC;
    --warn: #FF5252;
    --text: #E0E0E0;
  }

  body { background: var(--bg); color: var(--text); font-family: 'Roboto', sans-serif; margin: 0; }

  /* Navigation */
  .app-bar {
    background-color: var(--surface); padding: 0 24px; height: 64px;
    display: flex; align-items: center; justify-content: space-between;
    box-shadow: 0 2px 4px rgba(0,0,0,0.3); position: sticky; top: 0; z-index: 100;
  }
  .app-bar-title { font-size: 1.25rem; font-weight: 500; color: var(--primary); }
  .nav-links a { color: #aaa; text-decoration: none; margin-left: 20px; transition: 0.2s; }
  .nav-links a.active { color: var(--primary); }

  /* Layout */
  .container { max-width: 1200px; margin: 30px auto; padding: 0 20px; }
  .card { background: var(--surface); padding: 24px; border-radius: 12px; border: 1px solid var(--border); margin-bottom: 24px; }

  .btn {
    background: var(--primary); color: #000; border: none; padding: 10px 24px; border-radius: 4px;
    font-weight: bold; cursor: pointer; text-transform: uppercase; letter-spacing: 0.5px; transition: 0.2s; width: 100%;
  }
  .btn:hover { box-shadow: 0 0 10px rgba(3, 218, 198, 0.4); }
  .btn:disabled { background: #444; color: #888; cursor: not-allowed; box-shadow: none; }

  /* Segmented Control (Tabs) */
  .tabs { display: flex; background: #252525; padding: 4px; border-radius: 6px; margin-bottom: 20px; width: fit-content; border: 1px solid var(--border); }
  .tab-btn {
    background: transparent; border: none; color: #aaa;
    padding: 8px 24px; cursor: pointer; border-radius: 4px; font-size: 0.9rem; font-weight: 500; transition: 0.2s;
  }
  .tab-btn.active { background: #444; color: var(--primary); }
  .tab-btn:hover:not(.active) { color: #fff; }

  /* Inputs */
  .input-section { display: none; }
  .input-section.active { display: block; }

  textarea {
    width: 100%; background: #252525; border: 1px solid #444; color: #fff; padding: 12px;
    border-radius: 4px; min-height: 120px; font-family: monospace;
  }
  textarea:focus { outline: none; border-color: var(--primary); }

  .file-drop-area {
    display: block;
    border: 2px dashed #444; border-radius: 8px; padding: 32px;
    text-align: center; color: #aaa; transition: 0.2s; cursor: pointer; background: #252525;
  }
  .file-drop-area:hover { border-color: var(--primary); background: rgba(3, 218, 198, 0.05); }

  /* Diagram Workspace - Full Height & No Clipping */
  #diagram_wrapper {
    border: 1px solid var(--border);
    border-radius: 8px;
    background: #151515;
    height: 75vh;
    min-height: 600px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    position: relative;
  }

  #toolbar {
    background: #252525; padding: 8px 16px; display: flex; align-items: center; gap: 16px;
    border-bottom: 1px solid var(--border);
  }

  #diagram_scroll_area {
    flex: 1;
    overflow: auto;
    padding: 40px;
    display: block;
    text-align: center;
  }

  #diagram_scroll_area svg { height: auto; }

  /* Custom Range Slider */
  input[type=range] { -webkit-appearance: none; width: 100px; height: 4px; background: #555; border-radius: 2px; outline: none; }
  input[type=range]::-webkit-slider-thumb { -webkit-appearance: none; width: 16px; height: 16px; background: var(--primary); border-radius: 50%; cursor: pointer; }

  .zoom-btn {
    background: #444; color: #fff; border: 1px solid #555; width: 28px; height: 28px; border-radius: 4px;
    cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 1.2rem;
  }
  .zoom-btn:hover { background: #555; }

  /* Legend Grid */
  .legend-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 16px; margin-top: 20px; }

  .flow-card {
    background: #252525; border-radius: 8px; border: 1px solid #444; padding: 0;
    transition: transform 0.2s; position: relative; overflow: hidden;
  }
  .flow-card:hover { transform: translateY(-2px); border-color: var(--primary); }

  .flow-header {
    padding: 12px 16px; border-bottom: 1px solid #333; background: rgba(255,255,255,0.03);
    display: flex; align-items: center; justify-content: space-between;
  }
  .flow-title { font-size: 0.8rem; font-weight: 900; letter-spacing: 1px; text-transform: uppercase; }
  .flow-index { color: #555; font-weight: bold; font-size: 1.5rem; opacity: 0.3; }

  .flow-body { padding: 16px; }
  .flow-meta { font-size: 0.85rem; color: #aaa; margin-bottom: 12px; border-bottom: 1px solid #333; padding-bottom: 8px; }

  .tags-container { display: flex; flex-wrap: wrap; gap: 6px; }
  .data-tag {
    background: #252525; border: 1px solid #444; border-radius: 4px;
    padding: 4px 8px; font-size: 0.75rem; color: #ccc;
    font-family: 'Roboto Mono', monospace;
  }

  /* JSON Output */
  details { margin-top: 24px; color: #888; font-size: 0.9rem; cursor: pointer; }
  pre { background: #000; padding: 16px; border-radius: 6px; overflow-x: auto; border: 1px solid var(--border); color: #ccc; font-family: 'Roboto Mono'; }

  /* Footer disclaimer (reusable across pages) */
  .footer { text-align:center; color: #555; font-size: 0.75rem; margin-top: 40px; }
  .footer-sub { text-align:center; color: #666; font-size: 0.75rem; margin: 5px 0 20px 0; }
</style>
</head>

<body>
  <div class="app-bar">
    <div class="app-bar-title">Phoenix Mapper</div>
    <div class="nav-links">
      <a href="/ui">Laws</a>
      <a href="/ui/intake">Intake</a>
      <a href="/ui/contracts">Contracts</a>
      <a href="/ui/mapper" class="active">Mapper</a>
    </div>
  </div>

  <!-- IMPORTANT: result area + footer are INSIDE container now -->
  <div class="container">
    <div class="card">
      <h2 style="margin-top:0;">Data Flow Analysis</h2>
      <p style="color:#aaa; font-size:0.9rem;">Paste a privacy policy to automatically map data collection and third-party sharing.</p>

      <div class="tabs">
        <button class="tab-btn active" onclick="setMode('upload')">Upload File</button>
        <button class="tab-btn" onclick="setMode('text')">Paste Text</button>
      </div>

      <div id="input_upload" class="input-section active">
        <label for="file" class="file-drop-area">
          <div style="font-size:2rem; margin-bottom:8px;">📂</div>
          <div>Click to Select File</div>
          <div style="font-size:0.8rem; color:#666; margin-top:4px;">PDF, DOCX, or HTML supported</div>
          <input type="file" id="file" style="display:none;" onchange="handleFileSelect(this)">
        </label>
        <div id="file_name" style="margin-top:8px; color:var(--primary); font-size:0.9rem; text-align:center;"></div>
      </div>

      <div id="input_text" class="input-section">
        <textarea id="text_input" placeholder="Paste Privacy Policy text here..."></textarea>
      </div>

      <div style="margin-top:16px; display:flex; justify-content:space-between; align-items:center;">
        <button class="btn" id="run_btn" onclick="runMapper()">Generate Map</button>
      </div>
      <div id="status" style="margin-top:12px; text-align:center; color:#888; font-size:0.9rem; font-style:italic;"></div>
    </div>

    <div id="result_area" style="display:none;">
      <div class="card" style="border-top: 4px solid var(--primary); padding:0; overflow:hidden;">
        <div style="padding:16px 24px; background:#222; border-bottom:1px solid #333; display:flex; justify-content:space-between; align-items:center; gap:12px; flex-wrap:wrap;">
          <h3 style="margin:0;">Visual Map</h3>
          <div style="font-size:0.8rem; color:#888;">
            <span id="node_count">0</span> Entities &bull; <span id="flow_count">0</span> Flows
          </div>
          <button class="btn" style="width:auto; padding:6px 16px; font-size:0.8rem; background:#66BB6A;" onclick="downloadMapperReport()">Download Report</button>
        </div>

        <div id="diagram_wrapper">
          <div id="toolbar">
            <span style="font-size:0.8rem; color:#888; text-transform:uppercase; font-weight:bold;">Workspace</span>
            <div style="flex:1"></div>
            <button class="zoom-btn" onclick="adjustZoom(-0.1)">-</button>
            <input type="range" id="zoomRange" min="0.5" max="3.0" step="0.1" value="1.0" oninput="applyZoom(this.value)">
            <button class="zoom-btn" onclick="adjustZoom(0.1)">+</button>
            <span id="zoomLabel" style="font-size:0.8rem; color:#888; width:40px; text-align:right;">100%</span>
            <button class="zoom-btn" onclick="resetZoom()" style="width:auto; padding:0 12px; margin-left:12px; font-size:0.8rem;">Reset</button>
          </div>
          <div id="diagram_scroll_area"></div>
        </div>
      </div>

      <h3 style="margin:20px 0 10px 0; color:#888; font-size:0.9rem; text-transform:uppercase;">Detailed Data Flows</h3>
      <div id="legend_container" class="legend-grid"></div>

      <details>
        <summary>View Raw Analysis JSON</summary>
        <pre id="output"></pre>
      </details>
    </div>

    <!-- Disclaimer now always bottom of page, consistently -->
    <div class="footer">
      CONFIDENTIAL &bull; INTERNAL DEMO ONLY &bull; NOT LEGAL ADVICE
    </div>
    <div class="footer-sub">
      AI generated, can make mistakes. Check important info.
    </div>
  </div>

  <script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';

    // Single, canonical mermaid init (removed the duplicate init from <head>)
    mermaid.initialize({
      startOnLoad: false,
      theme: 'base',
      themeVariables: {
        darkMode: true,
        background: '#181818',
        mainBkg: '#1E1E1E',
        primaryColor: '#03DAC6',
        primaryTextColor: '#E0E0E0',
        lineColor: '#555',
        fontFamily: 'Roboto'
      },
      securityLevel: 'loose',
      flowchart: {
        useMaxWidth: false,
        htmlLabels: true,
        curve: 'basis',
        padding: 20
      }
    });

    window.currentMode = 'upload';
    window.currentZoom = 1.0;
    window.lastAnalysisData = null;

    // UI Logic
    window.setMode = function(mode) {
      window.currentMode = mode;
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelector(`button[onclick="setMode('${mode}')"]`).classList.add('active');
      document.querySelectorAll('.input-section').forEach(d => d.classList.remove('active'));
      document.getElementById(`input_${mode}`).classList.add('active');
    }

    window.handleFileSelect = function(input) {
      const fn = input.files[0] ? input.files[0].name : "";
      document.getElementById("file_name").textContent = fn;
    }

    // Zoom Logic
    window.applyZoom = function(val) {
      window.currentZoom = parseFloat(val);
      const svg = document.querySelector('#diagram_scroll_area svg');
      const label = document.getElementById('zoomLabel');
      if (svg) {
        svg.style.width = (window.currentZoom * 100) + "%";
        label.innerText = Math.round(window.currentZoom * 100) + "%";
      }
    }

    window.adjustZoom = function(delta) {
      const range = document.getElementById('zoomRange');
      let newVal = parseFloat(range.value) + delta;
      if (newVal < 0.5) newVal = 0.5;
      if (newVal > 3.0) newVal = 3.0;
      range.value = newVal;
      applyZoom(newVal);
    }

    window.resetZoom = function() {
      document.getElementById('zoomRange').value = 1.0;
      applyZoom(1.0);
    }

    function sanitizeId(text) {
      if (!text) return "unknown";
      return text.replace(/[^a-zA-Z0-9]/g, "");
    }

    function sanitizeLabel(text) {
      if (!text) return "";
      let clean = text.substring(0, 30);
      if (text.length > 30) clean += "...";
      clean = clean.replace(/["'(){}\\[\\]]/g, "");
      return clean;
    }

    // Prevent node id collisions (mermaid merges nodes with same id)
    function makeIdFactory() {
      const used = new Set();
      return function uniqueId(raw) {
        let base = sanitizeId(raw) || "node";
        let id = base;
        let i = 2;
        while (used.has(id)) id = `${base}_${i++}`;
        used.add(id);
        return id;
      };
    }

    window.runMapper = async function() {
      const status = document.getElementById("status");
      const out = document.getElementById("output");
      const resultArea = document.getElementById("result_area");
      const diagArea = document.getElementById("diagram_scroll_area");
      const legendContainer = document.getElementById("legend_container");
      const btn = document.getElementById("run_btn");

      const form = new FormData();
      if (window.currentMode === 'upload') {
        const fileInput = document.getElementById("file");
        if (!fileInput.files.length) { alert("Please select a file."); return; }
        form.append("file", fileInput.files[0]);
      } else {
        const textVal = document.getElementById("text_input").value;
        if (!textVal) { alert("Please paste text."); return; }
        form.append("payload_text", textVal);
      }

      btn.disabled = true;
      btn.innerText = "Processing...";
      status.innerText = "Analyzing text with LLM...";
      resultArea.style.display = "none";
      diagArea.innerHTML = "";

      try {
        const res = await fetch("/api/mapper", { method: "POST", body: form });
        const data = await res.json();

        if (data.error) throw new Error(data.error);

        window.lastAnalysisData = data;
        status.innerText = "";
        resultArea.style.display = "block";
        out.textContent = JSON.stringify(data, null, 2);
        document.getElementById("node_count").innerText = (data.diagram.nodes || []).length;
        document.getElementById("flow_count").innerText = (data.diagram.edges || []).length;

        // --- 1. RENDER DIAGRAM ---
        let graphDef = "graph LR\\n";
        graphDef += "classDef company fill:#37474F,stroke:#90A4AE,color:#ECEFF1,stroke-width:2px,rx:5,ry:5;\\n";
        graphDef += "classDef user fill:#00695C,stroke:#4DB6AC,color:#E0F2F1,stroke-width:2px,rx:5,ry:5;\\n";
        graphDef += "classDef thirdparty fill:#4527A0,stroke:#9575CD,color:#EDE7F6,stroke-width:2px,rx:5,ry:5;\\n";

        const laneColors = {
          "user": "user",
          "company": "company",
          "controller": "company",
          "thirdparty": "thirdparty",
          "vendors": "thirdparty",
          "partners": "thirdparty",
          "government": "thirdparty"
        };

        const uniqueId = makeIdFactory();
        const idMap = new Map(); // raw id -> unique mermaid id

        function getNodeId(raw) {
          if (!idMap.has(raw)) idMap.set(raw, uniqueId(raw));
          return idMap.get(raw);
        }

        // Nodes (stable subgraph ids; avoids styling issues)
        if (data.diagram.lanes) {
          data.diagram.lanes.forEach(lane => {
            const laneId = `lane_${sanitizeId(lane) || "lane"}`;
            const laneLabel = (lane || "").toUpperCase();

            graphDef += `subgraph ${laneId}["${laneLabel}"]\\n`;
            graphDef += `direction TB\\n`;

            (data.diagram.nodes || []).filter(n => n.lane === lane).forEach(n => {
              const mid = getNodeId(n.id);
              const cleanLbl = sanitizeLabel(n.label);
              const styleClass = laneColors[lane] || 'company';
              graphDef += `${mid}("${cleanLbl}"):::${styleClass}\\n`;
            });

            graphDef += "end\\n";
            graphDef += `style ${laneId} fill:#1E1E1E,stroke:#444,stroke-width:1px,color:#888\\n`;
          });
        } else {
          // fallback: render nodes without lanes
          (data.diagram.nodes || []).forEach(n => {
            const mid = getNodeId(n.id);
            const cleanLbl = sanitizeLabel(n.label);
            const styleClass = laneColors[n.lane] || 'company';
            graphDef += `${mid}("${cleanLbl}"):::${styleClass}\\n`;
          });
        }

        // Edges
        if (data.diagram.edges) {
          data.diagram.edges.forEach((e, i) => {
            const src = getNodeId(e.from);
            const tgt = getNodeId(e.to);
            const idx = i + 1;
            graphDef += `${src} -- ${idx} --> ${tgt}\\n`;
          });
        }

        const diagDiv = document.getElementById("diagram_scroll_area");
        diagDiv.innerHTML = `<pre class="mermaid" id="mermaid-graph">${graphDef}</pre>`;
        await mermaid.run({ nodes: [document.getElementById("mermaid-graph")] });
        resetZoom();

        // --- 2. RENDER LEGEND (Simple Chips) ---
        legendContainer.innerHTML = "";

        (data.flows || []).forEach((f, i) => {
          const card = document.createElement("div");
          card.className = "flow-card";

          const color = f.category === "Sharing" ? "var(--accent)" : "var(--primary)";
          const recipient = f.category === "Sharing"
            ? `To: <span>${(f.to || "")}</span>`
            : `From: <span>User</span>`;

          let tagsHtml = "";
          if (f.data_types && f.data_types.length) {
            tagsHtml = f.data_types.map(dt => `<span class="data-tag">${dt}</span>`).join("");
          } else {
            tagsHtml = `<span style="color:#666; font-size:0.8rem;">No specific data types listed.</span>`;
          }

          card.innerHTML = `
            <div class="flow-header">
              <div class="flow-title" style="color:${color}">${f.category || "Flow"}</div>
              <div class="flow-index">${i+1}</div>
            </div>
            <div class="flow-body">
              <div class="flow-meta">${recipient}</div>
              <div class="tags-container">${tagsHtml}</div>
            </div>
          `;
          legendContainer.appendChild(card);
        });

      } catch (e) {
        console.error(e);
        alert("Error: " + e.message);
        status.innerText = "Error occurred.";
      } finally {
        btn.disabled = false;
        btn.innerText = "Generate Map";
      }
    };

    // Function to generate the report
    window.downloadMapperReport = async function() {
      if (!window.lastAnalysisData) return;
      const svg = document.querySelector('#diagram_scroll_area svg');
      if (!svg) return alert("Diagram not ready");

      const serializer = new XMLSerializer();
      const source = serializer.serializeToString(svg);
      const encodedData = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(source)));

      const canvas = document.createElement('canvas');
      const ctx = canvas.getContext('2d');
      const img = new Image();

      const bbox = svg.getBoundingClientRect();
      canvas.width = bbox.width * 2;
      canvas.height = bbox.height * 2;

      img.onload = async function() {
        ctx.fillStyle = "#1E1E1E";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        const pngData = canvas.toDataURL("image/png");

        try {
          const resp = await fetch("/api/mapper/export-report", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
              image_base64: pngData,
              flows: window.lastAnalysisData.flows,
              controller: window.lastAnalysisData.controller_detected || "Unknown"
            })
          });
          if (!resp.ok) throw new Error(await resp.text());
          const blob = await resp.blob();
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement("a");
          a.href = url;
          a.download = "Privacy_Map_Report.docx";
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
        } catch (e) {
          console.error(e);
          alert("Export failed: " + e.message);
        }
      };
      img.src = encodedData;
    }
  </script>
</body>
</html>
"""
