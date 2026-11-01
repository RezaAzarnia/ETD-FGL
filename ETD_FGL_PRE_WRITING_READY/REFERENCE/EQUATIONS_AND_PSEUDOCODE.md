# Equations and pseudocode (matched to code; branch HEAD 3084163)

## Equations
**Graph simplification.** Each client graph is turned into an undirected simple graph (self-loops dropped, parallel/directed duplicates merged) before the descriptor (`defenses.py:_graph_descriptor`).

**5-D descriptor** d(G) = [ρ, k̄, V, C̄, τ]:
- ρ = 2|E| / (|V|(|V|−1)); k̄ = (1/|V|) Σ d_v;
- V = [(1/|V|) Σ (d_v − k̄)²] / (k̄² + 10⁻¹²)  (population variance);
- C̄ = (1/|V|) Σ C_v with C_v = 2T_v/(d_v(d_v−1)), C_v = 0 if d_v < 2 (networkx default);
- τ = (Σ_v T_v / 3) / max(1, |V|).

**Standardized drift.** s_j = std_i(d_j(G_i⁰)) (ddof = 0, over the K clean descriptors); s_j ← 1 if s_j < 10⁻⁸.
Δ_i = ‖(d(G_i) − d(G_i⁰)) ⊘ s‖₂.

**One-sided robust map** 𝓡(v) for v ∈ ℝ^K_{≥0}: m = median(v); S = max(1.4826·median|v − m|, std(v), 10⁻⁸) (std ddof = 0); z_i = max((v_i − m)/S, 0); 𝓡_i = clip(2(σ(z_i) − ½), 0, 1).
**Topology anomaly (once):** A_topo,i = 𝓡(Δ)_i.
**Update anomaly (round t):** u_i^t = θ_i^t − θ^{t−1} (all float parameters flattened); μ^t = coordinate-wise median_j u_j^t; q_i^t = ‖u_i^t − μ^t‖₂; A_upd,i^t = 𝓡(q^t)_i.
**Fusion:** R_i^t = (9/13) A_topo,i + (4/13) A_upd,i^t.
**Trust:** T_i^t = clip(exp(−3 R_i^t), 0.02, 1).
**Weights:** w_i^t = n_i T_i^t / Σ_j n_j T_j^t, n_i = # local training nodes. **Aggregation:** θ^t = Σ_i w_i^t θ_i^t.
**Degenerate-regime identity (K=5, M=1, benign Δ=0, attacker Δ=d≥2.5·10⁻⁸):** S = std = 0.4d ⇒ z₀ = 2.5 ⇒ A_topo,0 = 2(σ(2.5)−½) = 0.848284; with A_upd,0 = 0: R₀ = 0.5873, T₀ = 0.1717; equal n_i ⇒ w₀ = 0.1717/(0.1717+4) = 4.117 %.
**Metrics.** Acc = mean 1[ŷ=y] on test mask. CTR = mean_{v∈V_¬0} 1[ŷ(v)=0]; ASR = mean_{v∈V_¬0} 1[ŷ(v ⊕ K3)=0]; effect = ASR − CTR; V_¬0 = non-target test nodes.
**Ablations.** Controlled: R = c_t A_topo + c_u A_upd with (c_t,c_u) ∈ {(9/13,4/13), (9/13,0), (0,4/13)}. Standard: weights (c_t,c_e,c_u)/Σc with β = 3: Topology-only (1,0,0), Update-only (0,0,1), Historical (0.45,0.35,0.20) (explanation = GNNExplainer score), No-trust (T≡1).

## Pseudocode
```
Input: client graphs {G_i}, clean refs {G_i^0}, rounds T=50, epochs E=3
Setup:  D0 = [d(G_i^0)], D = [d(G_i)]; s = std(D0, axis=0) (floor→1)
        Δ_i = ||(D_i − D0_i)/s||_2 ;  A_topo = R(Δ)            # static
θ ← init GCN
for t = 1..T:
    for i in 1..K:   θ_i ← E Adam epochs on G_i starting from θ  # client 0 trains on poisoned G_0
    u_i = θ_i − θ ;  μ = coordinatewise_median(u) ;  q_i = ||u_i − μ||_2
    A_upd = R(q) ;  R = 9/13·A_topo + 4/13·A_upd
    T_i = clip(exp(−3 R_i), 0.02, 1) ; w_i = n_i T_i / Σ n_j T_j
    θ ← Σ_i w_i θ_i
    evaluate(θ): val/test acc on clean global graph; CTR, ASR on triggered global graph
    if val_acc > best: best, ckpt ← θ, t
report evaluate(ckpt)
```
```
R(v): m=median(v); S=max(1.4826*median|v-m|, std(v), 1e-8); z=max((v-m)/S,0); return clip(2*(sigmoid(z)-0.5),0,1)
```
