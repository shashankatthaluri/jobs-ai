# Jobs - AI-Powered Job Application Assistant

## EXECUTION STRATEGY (HIGH LEVEL)

### Goal (V1 end of day):
A live web app where a user can:
- Upload Master CV (PDF)
- Paste Job Description OR Job Link
- Click actions:
  - Analyze company
  - Tailor ATS-safe resume
  - Generate cover letter
  - Generate cold email

**Not perfect. Working + believable + demo-ready.**

---

## SYSTEM ARCHITECTURE (LOCKED)

### Frontend
- Next.js (App Router)
- Tailwind CSS
- Simple dashboard UX
- PDF upload + preview
- Results panels (tabs)

### Backend
- FastAPI (Python)
- Async endpoints
- One LLM provider (no abstraction yet)
- Perplexity Search (for company intel)

### Core Philosophy
- Rule-first, AI-second
- Structure before writing
- No hallucinated experience

---

## FASTEST POSSIBLE ROADMAP (24-HOUR VERSION)

### PHASE 0 — Lock Scope (30 min)

**We are NOT building:**
- User accounts
- Payments
- Multiple resume templates
- Recruiter analytics

**We ARE building:**
- One clean ATS-safe resume format
- One cover letter
- One cold email
- One company intelligence panel

---

### PHASE 1 — Master CV Intelligence (3 hours)

#### What it must do
- Accept PDF
- Extract:
  - Name
  - Experience (company, role, dates)
  - Skills
  - Education
- Convert to structured JSON

#### Output (example)
```json
{
  "name": "",
  "experience": [],
  "skills": [],
  "education": []
}
```

#### Agent Prompt — CV Parsing Agent
```
You are a senior resume parsing engineer.

Input: raw text extracted from a PDF resume.

Task:
- Extract all information into structured JSON.
- Preserve exact dates and company names.
- Do NOT infer or invent skills.
- Group experience chronologically.

Output JSON with keys:
- name
- experience (company, role, start_date, end_date, bullets)
- skills
- education

Output ONLY valid JSON.
```

---

### PHASE 2 — Job + Company Intelligence (3 hours)

#### Job Description Handling
Accept:
- Pasted JD
- OR Job URL

If URL:
- Fetch page
- Extract job text
- Clean boilerplate

#### Company Intelligence (via Perplexity)
- Website
- Employee count (range)
- Hiring manager (if visible)
- Public email (if available)
- Recent funding/news (last 12 months)

#### Agent Prompt — Job Analyzer Agent
```
You are a technical recruiter with ATS expertise.

Input: Job description text.

Extract:
- Required skills
- Preferred skills
- Seniority level
- Industry
- Keywords ATS will scan

Output JSON only.
```

#### Agent Prompt — Company Intelligence Agent
```
You are a company research analyst.

Using web search if needed:
- Company website
- Approx employee size
- Any public hiring contact
- Recent funding/news

If info is unavailable, return null.

Output structured JSON only.
```

---

### PHASE 3 — Matching + Tailoring Engine (4 hours)

This is the core brain.

#### Logic (non-negotiable)
- Match JD skills ↔ CV skills
- Score relevance per experience
- Select ONLY relevant bullets
- Rewrite bullets for clarity + keywords
- Keep chronology intact

#### Resume Rules
- One column
- No tables
- Standard headings
- Bullet length ≤ 2 lines
- No graphics

#### Agent Prompt — Resume Tailoring Agent
```
You are an ATS optimization expert.

Inputs:
- Structured Master CV (JSON)
- Job description analysis (JSON)

Rules:
- Do NOT invent experience.
- Do NOT change dates.
- Emphasize matching skills.
- Rewrite bullets using job keywords where truthful.

Output:
- ATS-safe resume in clean markdown format.
```

---

### PHASE 4 — Writing Layer (2 hours)

#### Cover Letter
- Personalized
- 3 paragraphs
- No fluff
- Job + company specific

#### Cold Email
- 4–6 lines
- Human tone
- Clear CTA
- No desperation

#### Agent Prompt — Cover Letter Agent
```
You are a senior hiring manager.

Write a concise cover letter using:
- Tailored resume
- Job description
- Company context

Constraints:
- Max 350 words
- Professional, confident tone
- No generic phrases
```

#### Agent Prompt — Cold Email Agent
```
You are an experienced recruiter outreach specialist.

Write a short cold email:
- Friendly, human
- References role and company
- One clear CTA

Max 120 words.
```

---

### PHASE 5 — Frontend Assembly (4 hours)

#### Pages
- Landing page (simple)
- Upload CV
- Paste JD / URL
- Action buttons
- Results tabs:
  - Resume
  - Cover Letter
  - Cold Email
  - Company Intel

#### UX Rules
- Show loading states
- No long explanations
- Copy/download buttons

---

### PHASE 6 — Final Polish (1–2 hours)
- Error handling
- Empty states
- Disclaimers
- Demo-ready content

---

## DEVELOPMENT CHECKLIST

- [ ] **Phase 0**: Lock scope & confirm architecture
- [ ] **Phase 1**: PDF upload + CV parsing + JSON output
- [ ] **Phase 2**: JD input + Company intelligence via Perplexity
- [ ] **Phase 3**: Matching engine + Resume tailoring
- [ ] **Phase 4**: Cover letter + Cold email generation
- [ ] **Phase 5**: Frontend assembly with all tabs
- [ ] **Phase 6**: Final polish + error handling

---

## NOTES

> Always refer to this plan before starting any task.
> Follow phases sequentially.
> No scope creep — V1 is demo-ready, not production-ready.
