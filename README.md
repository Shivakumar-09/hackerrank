# 🏆 Multi-Domain Support Triage Agent
> **Advanced Support Intelligence Engine for HackerRank, Claude, and Visa Ecosystems**

---

## 📌 1. Problem Statement
Scale-stage companies face extreme ticket volumes that overwhelm human support teams. This project provides a production-ready **Terminal-based Triage Agent** designed to automate the initial support lifecycle for three distinct domains: EdTech (HackerRank), AI (Claude), and Fintech (Visa). The system ensures 100% grounded classification and context-aware escalation for high-liability issues.

## ✨ 2. Features
*   **Intelligent Domain Routing**: Automated company inference for tickets with missing metadata.
*   **Risk-Based Escalation**: Proactive detection of fraud, security breaches, and account blockers.
*   **Grounded Resolution**: Support article retrieval using a TF-IDF semantic engine.
*   **Transparent Justification**: Audit-ready reasoning for every automated decision.
*   **Enterprise Observability**: Real-time transcript logging and deterministic CSV output.

## 📂 3. Folder Structure
```text
hackerrank-orchestrate-may26/
├── code/
│   ├── main.py         # Entry point & pipeline orchestrator
│   ├── triage.py       # Layered Decision Pipeline (LDP)
│   ├── rules.py        # Domain-specific heuristics & templates
│   ├── retrieval.py    # Company-filtered search engine
│   ├── logger.py       # High-fidelity audit logging
│   ├── utils.py        # Text processing utilities
│   └── requirements.txt
└── README.md
```

## ⚙️ 4. Setup & Execution

### Dependency Installation
Ensure you have Python 3.10+ installed. Install the required libraries via pip:
```bash
pip install -r code/requirements.txt
```

### Run Command
Execute the triage pipeline from the project root:
```bash
python code/main.py
```

## 📥 5. Inputs & Outputs
*   **Input**: `support_tickets/support_tickets.csv` (Target corpus for triage).
*   **Generated Outputs**:
    *   **`support_tickets/output.csv`**: Structured predictions for all rows.
    *   **`log.txt`**: Real-time audit transcript (Saved to `~/hackerrank_orchestrate/log.txt`).

## 📊 6. Output CSV Schema
| Column | Description |
| :--- | :--- |
| `status` | Action taken: `replied` or `escalated`. |
| `product_area` | The identified company-specific functional area. |
| `response` | The grounded resolution or handoff message. |
| `justification` | Transparent logic for the decision. |
| `request_type` | Detected intent: `bug`, `feature_request`, `product_issue`, or `invalid`. |

## 🧠 7. Approach Overview
The agent implements a **Hybrid AI Pipeline** designed for safety and precision:
1.  **Rule-based Classification**: Uses weighted keyword scoring for deterministic routing.
2.  **Company Inference**: Semantic analysis of text to resolve domain context.
3.  **Risk Escalation Engine**: Scans for 15+ liability triggers (fraud, theft, security) to bypass automation.
4.  **TF-IDF Retrieval Layer**: Indexes company support docs to provide grounded, non-hallucinated answers.
5.  **Confidence Scoring**: Automatically escalates any decision with a semantic match score below 0.55.
6.  **Safe Response Generation**: Uses contextual templates to ensure professional and accurate communication.

## 🚀 8. Performance & Strength
*   **Safe**: Implements **Closed-World Retrieval**—no hallucinated policies.
*   **Explainable**: Every action includes a trace justifying the agent's logic.
*   **Fast**: Processes large ticket batches in sub-second latency.
*   **Robust**: Multi-domain support with zero cross-contamination between company datasets.

---
**Author**: Created by Shiva  
*Senior AI Engineering - HackerRank Orchestrate Hackathon Submission*
