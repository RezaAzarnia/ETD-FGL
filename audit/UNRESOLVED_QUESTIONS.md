# ETD-FGL Unresolved Scientific Decisions

**Status:** Awaiting Author / Principal Investigator (PI) Approval
**Auditor:** Senior ML Research Engineer & Scientific Code Auditor
**Date:** October 2026

Per strict research integrity guidelines, the auditor has repaired all verified software bugs, exception handling flaws, and test inconsistencies while leaving foundational scientific modeling decisions untouched. The following methodological questions require explicit author sign-off prior to journal resubmission or final camera-ready revision.

---

## 1. Threat Model & Clean Reference Availability
- **Context:** The production ETD-FGL defense computes topological anomaly scores using the exact clean pre-attack client graph $G_i^{(0)}$ as a reference.
- **Decision Required from Authors:**
  - **Option A (Recommended for current revision):** Explicitly document in Section 3/4 that the experimental evaluation operates under an *authenticated initialization / simulation reference* assumption (i.e., the server establishes a clean topological baseline during a trusted warm-up phase).
  - **Option B (Algorithmic Modification - Class D):** Modify the defense to use inter-round temporal drift:
    $$\Delta_i^{(t)} = \|\mathbf{d}(G_i^{(t)}) - \mathbf{d}(G_i^{(t-1)})\|_2$$
    or a cross-client median reference:
    $$\Delta_i^{(t)} = \|\mathbf{d}(G_i^{(t)}) - \text{median}_{j}(\mathbf{d}(G_j^{(t)}))\|_2$$
  - *Auditor Recommendation:* Choose Option A to preserve existing benchmark reproducibility, while introducing Option B in the discussion as future work for zero-trust initializations.

---

## 2. Test-Label Information in Graph Partitioning
- **Context:** The partitioning logic in `multidata_suite/data.py` uses class labels across all node masks (including `test_mask`) to allocate balanced class distributions across clients, preventing degenerate empty-class clients on Planetoid Cora (which has only 140 training nodes).
- **Decision Required from Authors:**
  - **Option A (Recommended):** Retain the existing stratified partition protocol to ensure historical consistency and comparability, but add an explicit footnote/paragraph in Section 4.1 clarifying that stratification across all splits is used strictly to guarantee viable graph partitions for sparse benchmark graphs.
  - **Option B (New Protocol - Class D):** Implement a fully label-blind partitioner (e.g., METIS graph partitioning or uniform node assignment) and re-run all benchmark tables under a separate "Partition Protocol B" tag.

---

## 3. Client Scalability Study Design
- **Context:** In `run_extended_experiments.py`, client scalability sweeps $K \in \{5, 10, 20, 30, 50\}$ while fixing malicious clients $M = 1$. The adversarial fraction drops from $20\%$ at $K=5$ to $2\%$ at $K=50$.
- **Decision Required from Authors:**
  - **Option A (Current):** Retain the existing experiment and explicitly describe the result as "Scalability Under Fixed Single Attacker ($M=1$)."
  - **Option B (Expanded Study):** Add an additional parallel study with a constant $20\%$ adversarial fraction ($M = \max(1, \text{round}(0.2 \cdot K))$).

---

## 4. FedTGE Baseline Comparator Protocol
- **Context:** The official FedTGE implementation evaluates cosine similarity between zero-padded node energy vectors, which is sensitive to local node ordering across client partitions.
- **Decision Required from Authors:**
  - **Option A (Recommended):** Retain the exact official comparator implementation to maintain published baseline comparability, with an accompanying methodological disclosure in the baseline description.
  - **Option B (Baseline Adaptation):** Replace cosine similarity of raw vectors with a permutation-invariant metric (such as Wasserstein distance or energy histogram matching) and re-evaluate FedTGE as an "Adapted Permutation-Invariant FedTGE."

---

## 5. Multiple-Victim Simultaneous Inference during ASR Evaluation
- **Context:** When computing Attack Success Rate (ASR), triggers are currently attached to multiple victim test nodes in the test graph simultaneously.
- **Decision Required from Authors:**
  - **Option A (Current):** Keep simultaneous multi-victim evaluation, which measures practical aggregate backdoor vulnerability on the shared graph.
  - **Option B (Isolated Single-Victim Inference):** Evaluate each test victim in isolation by creating separate single-triggered graphs to eliminate potential multi-trigger graph interaction effects.
