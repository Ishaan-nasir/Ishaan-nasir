<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/header-dark.svg">
  <img src="assets/header-light.svg" width="100%" alt="Ishaan Nasir">
</picture>

I'm studying Computer Science at Manipal University Jaipur (2025 to 2029). I build AI products for work where a wrong number costs real money, so most of my code is the checking layer around the model.

### Working on

**Clyve**&ensp;<sub>private</sub><br>
Accounting software for Indian CAs and small businesses. Scanned invoices go through OCR and a model, then a rules layer checks totals, GSTIN, amount in words and dates before anything is posted. The model never does the arithmetic. Amounts are stored as integers and the ledger is append-only, enforced in Postgres.

**[Voiceraft](https://voiceraft.org)**&ensp;<sub>voiceraft.org</sub><br>
Phone agents for businesses. They answer the call, qualify the caller and book a slot in the calendar while still on the line, in English, French and Hinglish. Each call lands in the client's CRM as a structured record.

**LegaDoc**&ensp;<sub>Smart India Hackathon, team of six</sub><br>
Case-file system for Indian police: 57 document types and chain of custody across ten roles. I wrote the system design and built the PII redaction service, which sends low-confidence matches to a person for review.

### Shipped

| Project | Type | Built |
|---|---|---|
| [heri8age.in](https://heri8age.in) | D2C store | stock reservation, GST invoicing, fulfilment, admin panel |
| [heartartsindia.com](https://heartartsindia.com) | Client site | Next.js and Supabase, CMS with 94 editable fields |
| [ONCA waitlist](https://onca-waitlist-navy.vercel.app/) | Landing page | early-access signups for ONCA |
| [mt5-mac-python-bridge](https://github.com/Ishaan-nasir/mt5-mac-python-bridge) | Tool | MetaTrader 5 from Python on macOS, no Wine or VPS |
| [SnapCal](https://github.com/Ishaan-nasir/SnapCal) | Tool | photo of a timetable to an `.ics` calendar file |

### Claude Code skills

I write skills for Claude Code and run them on my own production repos. The security audit skill found four high-severity issues in Clyve, one of them a prompt-injection path. All four are fixed.

- [`reasoning-core`](https://github.com/Ishaan-nasir/reasoning-core): a step-by-step procedure with checkpoints. It won't answer from memory about versioned APIs.
- [`handover`](https://github.com/Ishaan-nasir/handover): saves a working session to a state file, so a long build picks up where it stopped after a context reset.

### Stack

<img src="https://skillicons.dev/icons?i=ts,python,postgres,supabase,nextjs,react,fastapi,docker,git&theme=dark" height="40" alt="TypeScript, Python, Postgres, Supabase, Next.js, React, FastAPI, Docker, Git">

```
backend    Postgres row-level security, job queues, FastAPI
ai         MCP tool design, retrieval, eval harnesses, local quantized models
security   threat modelling, code audits, C4 system design
```

### Elsewhere

- Smart India Hackathon 2026: top 95 of 700+ teams
- Dev Relay Hackathon: second place with Team Redact
- Google Developer Groups on Campus, MUJ: technical team

<img src="profile-3d-contrib/profile-night-green.svg" width="100%" alt="Contribution graph">

[Email](mailto:contact.ishaannasir@gmail.com) · [LinkedIn](https://www.linkedin.com/in/ishaan-nasir/) · [voiceraft.org](https://voiceraft.org)
