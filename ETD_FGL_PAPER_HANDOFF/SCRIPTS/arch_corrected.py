"""
Generate Publication-Grade Vector Architecture and Defense Workflow Diagram for ETD-FGL
"""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch

def create_architecture_diagram(output_pdf, output_png):
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
    plt.rcParams['mathtext.fontset'] = 'cm'

    fig = plt.figure(figsize=(15.2, 6.8), dpi=300)
    ax = fig.add_subplot(111)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 108)
    ax.axis('off')

    # Color palette (Modern, refined academic palette)
    c_client_bg = '#F4F7FA'
    c_client_border = '#4A6FA5'
    c_topo_bg = '#FFF9E6'
    c_topo_border = '#D49B24'
    c_upd_bg = '#EBF6ED'
    c_upd_border = '#388E3C'
    c_fusion_bg = '#F6EDF8'
    c_fusion_border = '#7B1FA2'
    c_global_bg = '#E6F4FB'
    c_global_border = '#0288D1'

    # 1. Main Section Containers
    # Container 1: Decentralized Clients (Left)
    box_clients = FancyBboxPatch((1.2, 9.5), 22.5, 94.5, boxstyle="round,pad=0.8,rounding_size=1.5",
                                 facecolor=c_client_bg, edgecolor=c_client_border, linewidth=1.5, linestyle='--')
    ax.add_patch(box_clients)
    ax.text(12.45, 101.5, 'Decentralized Graph Clients', fontsize=12, fontweight='bold', ha='center', color='#1A365D')
    ax.text(12.45, 98.5, r'Clients $i \in \{1, \dots, K\}$ with private graphs', fontsize=9.2, ha='center', color='#4A5568')

    # Container 2: Central Parameter Server (Right)
    box_server = FancyBboxPatch((25.2, 9.5), 73.6, 94.5, boxstyle="round,pad=0.8,rounding_size=1.5",
                                facecolor='#FAFAFA', edgecolor='#374151', linewidth=1.8)
    ax.add_patch(box_server)
    ax.text(62.0, 101.5, 'Central Parameter Server — ETD-FGL Defense Pipeline', fontsize=13, fontweight='bold', ha='center', color='#111827')

    # Sub-container 2A: Phase 1: Offline Structural Profiling
    box_phase1 = FancyBboxPatch((27.0, 56.5), 32.5, 38.0, boxstyle="round,pad=0.5,rounding_size=1.2",
                                facecolor=c_topo_bg, edgecolor=c_topo_border, linewidth=1.4)
    ax.add_patch(box_phase1)
    ax.text(43.25, 91.5, 'Phase 1: Offline Structural Profiling', fontsize=11, fontweight='bold', ha='center', color='#8C5B00')
    ax.text(43.25, 88.5, '(Label-Free Topological Drift Detection)', fontsize=9, ha='center', color='#6B4701', style='italic')

    # Sub-container 2B: Phase 2: Dynamic Update Profiling
    box_phase2 = FancyBboxPatch((27.0, 13.5), 32.5, 40.0, boxstyle="round,pad=0.5,rounding_size=1.2",
                                facecolor=c_upd_bg, edgecolor=c_upd_border, linewidth=1.4)
    ax.add_patch(box_phase2)
    ax.text(43.25, 50.5, 'Phase 2: Round-Wise Update Anomaly', fontsize=11, fontweight='bold', ha='center', color='#1B5E20')
    ax.text(43.25, 47.5, r'(Coordinate-wise Median in Model Space, Round $t$)', fontsize=8.5, ha='center', color='#2E7D32', style='italic')

    # Sub-container 2C: Evidence Fusion & Dynamic Trust Weighting
    box_phase3 = FancyBboxPatch((61.5, 13.5), 23.0, 81.0, boxstyle="round,pad=0.5,rounding_size=1.2",
                                facecolor=c_fusion_bg, edgecolor=c_fusion_border, linewidth=1.4)
    ax.add_patch(box_phase3)
    ax.text(73.0, 91.5, 'Fused Risk & Trust Weighting', fontsize=11, fontweight='bold', ha='center', color='#4A148C')

    # Sub-container 2D: Global Aggregation & Broadcast
    box_phase4 = FancyBboxPatch((86.2, 13.5), 11.2, 81.0, boxstyle="round,pad=0.5,rounding_size=1.2",
                                facecolor=c_global_bg, edgecolor=c_global_border, linewidth=1.4)
    ax.add_patch(box_phase4)
    ax.text(91.8, 91.5, 'Robust\nAggregation', fontsize=11, fontweight='bold', ha='center', color='#01579B')

    # ================= DETAIL BLOCKS =================

    # 1. Inside Decentralized Clients
    # Benign Client Box
    box_benign = FancyBboxPatch((3.0, 57.5), 18.8, 36.5, boxstyle="round,pad=0.4,rounding_size=1.0",
                                facecolor='#FFFFFF', edgecolor='#2B6CB0', linewidth=1.2)
    ax.add_patch(box_benign)
    ax.text(12.4, 91.0, r'Benign Client $i$ (Clean)', fontsize=10, fontweight='bold', ha='center', color='#2B6CB0')
    ax.text(12.4, 85.5, r'• Auth. Pre-attack Graph: $G_i^0$', fontsize=8.5, ha='center', color='#2D3748')
    ax.text(12.4, 80.5, r'• Current Graph: $G_i \approx G_i^0$', fontsize=8.5, ha='center', color='#2D3748')
    ax.text(12.4, 75.5, r'• Clean GCN Training on $G_i$', fontsize=8.5, ha='center', color='#2D3748')
    ax.text(12.4, 70.0, r'• Model Weights: $\mathbf{w}_i^t$', fontsize=8.5, ha='center', color='#2D3748')
    ax.text(12.4, 64.5, r'• Delta: $\Delta\mathbf{w}_i^t = \mathbf{w}_i^t - \mathbf{w}_{\mathrm{global}}^{t-1}$', fontsize=8, ha='center', color='#1A365D')

    # Malicious Client Box
    box_mal = FancyBboxPatch((3.0, 15.0), 18.8, 38.0, boxstyle="round,pad=0.4,rounding_size=1.0",
                             facecolor='#FFF5F5', edgecolor='#E53E3E', linewidth=1.2)
    ax.add_patch(box_mal)
    ax.text(12.4, 49.5, r'Attacker Client $m$ (Poisoned)', fontsize=10, fontweight='bold', ha='center', color='#C53030')
    ax.text(12.4, 44.0, r'• Injected Backdoor Trigger:', fontsize=8.5, ha='center', color='#2D3748')
    ax.text(12.4, 40.0, r'  Dense Clique Trigger on test nodes', fontsize=8, ha='center', color='#742A2A', style='italic')
    ax.text(12.4, 35.5, r'• Poisoned Graph: $G_m \neq G_m^0$', fontsize=8.5, ha='center', color='#C53030')
    ax.text(12.4, 31.0, r'• Dual Objective (Clean Acc + ASR)', fontsize=8, ha='center', color='#2D3748')
    ax.text(12.4, 26.5, r'• Poisoned Model Delta:', fontsize=8.5, ha='center', color='#2D3748')
    ax.text(12.4, 21.5, r'$\Delta\mathbf{w}_m^t = \mathbf{w}_m^t - \mathbf{w}_{\mathrm{global}}^{t-1}$', fontsize=8.5, ha='center', color='#9B2C2C', fontweight='bold')

    # 2. Inside Phase 1: Offline Structural Profiling
    # 5D Descriptor Box
    box_desc = FancyBboxPatch((28.5, 75.0), 29.5, 11.5, boxstyle="round,pad=0.3,rounding_size=0.8",
                             facecolor='#FFFFFF', edgecolor=c_topo_border, linewidth=1.0)
    ax.add_patch(box_desc)
    ax.text(43.25, 82.5, r'5D Label-Free Topology Descriptor $\mathbf{d}(G)$:', fontsize=8.8, fontweight='bold', ha='center', color='#744210')
    ax.text(43.25, 78.0, r'$\mathbf{d}(G) = [\rho,\; \bar{k},\; \mathrm{Var}_{\mathrm{norm}}(k),\; \bar{C},\; \tau]$', fontsize=9, ha='center', color='#975A16')

    # Drift Box
    box_drift = FancyBboxPatch((28.5, 58.5), 29.5, 14.5, boxstyle="round,pad=0.3,rounding_size=0.8",
                              facecolor='#FFFFFF', edgecolor=c_topo_border, linewidth=1.0)
    ax.add_patch(box_drift)
    ax.text(43.25, 69.5, r'Pairwise Standardized Structural Drift:', fontsize=8.5, fontweight='bold', ha='center', color='#744210')
    ax.text(43.25, 65.0, r'$\Delta_i^{\mathrm{topo}} = \|\mathbf{s}^{-1} \odot (\mathbf{d}(G_i) - \mathbf{d}(G_i^0))\|_2$', fontsize=8.8, ha='center', color='#1A202C')
    ax.text(43.25, 60.5, r'Topology Anomaly: $A_{\mathrm{topo}, i} = \mathcal{R}(\Delta_i^{\mathrm{topo}}) \in [0, 1]$', fontsize=8.5, fontweight='bold', ha='center', color='#C05621')

    # 3. Inside Phase 2: Dynamic Update Profiling
    box_upd_median = FancyBboxPatch((28.5, 31.5), 29.5, 13.5, boxstyle="round,pad=0.3,rounding_size=0.8",
                                   facecolor='#FFFFFF', edgecolor=c_upd_border, linewidth=1.0)
    ax.add_patch(box_upd_median)
    ax.text(43.25, 41.0, r'Robust Coordinate-Wise Update Median:', fontsize=8.5, fontweight='bold', ha='center', color='#1B5E20')
    ax.text(43.25, 37.0, r'$\mathbf{m}^t = \mathrm{median}_{j \in \{1,\dots,K\}} (\Delta\mathbf{w}_j^t)$', fontsize=9, ha='center', color='#1A202C')
    ax.text(43.25, 33.5, r'Update Distance: $d_i^t = \|\Delta\mathbf{w}_i^t - \mathbf{m}^t\|_2$', fontsize=8.5, ha='center', color='#2E7D32')

    box_upd_score = FancyBboxPatch((28.5, 15.5), 29.5, 14.0, boxstyle="round,pad=0.3,rounding_size=0.8",
                                  facecolor='#FFFFFF', edgecolor=c_upd_border, linewidth=1.0)
    ax.add_patch(box_upd_score)
    ax.text(43.25, 26.0, r'One-Sided Robust Scaling $\mathcal{R}(\cdot)$:', fontsize=8.5, fontweight='bold', ha='center', color='#1B5E20')
    ax.text(43.25, 21.5, r'$z = \max(0, (v - \mathrm{med})/\mathrm{MAD})$', fontsize=8.5, ha='center', color='#1A202C')
    ax.text(43.25, 17.5, r'Update Anomaly: $A_{\mathrm{upd}, i}^t = \mathcal{R}(d_i^t) \in [0, 1]$', fontsize=8.5, fontweight='bold', ha='center', color='#2E7D32')

    # 4. Inside Fused Risk & Trust Weighting
    box_fusion = FancyBboxPatch((62.5, 54.5), 21.0, 32.5, boxstyle="round,pad=0.3,rounding_size=0.8",
                               facecolor='#FFFFFF', edgecolor=c_fusion_border, linewidth=1.0)
    ax.add_patch(box_fusion)
    ax.text(73.0, 82.5, 'Fused Client Risk', fontsize=9.5, fontweight='bold', ha='center', color='#4A148C')
    ax.text(73.0, 77.0, r'$R_i^t = \frac{9}{13} A_{\mathrm{topo}, i} + \frac{4}{13} A_{\mathrm{upd}, i}^t$', fontsize=9.5, fontweight='bold', ha='center', color='#6A1B9A')
    ax.text(73.0, 71.5, r'($\alpha_{\mathrm{topo}} = 9/13, \; \alpha_{\mathrm{upd}} = 4/13$)', fontsize=8, ha='center', color='#4A5568')
    ax.text(73.0, 66.0, 'Exponential Trust Mapping:', fontsize=8.5, fontweight='bold', ha='center', color='#4A148C')
    ax.text(73.0, 60.5, r'$T_i^t = \mathrm{clip}\left(e^{-3 R_i^t}, 0.02, 1.0\right)$', fontsize=9.2, fontweight='bold', ha='center', color='#7B1FA2')

    box_weights = FancyBboxPatch((62.5, 16.0), 21.0, 34.5, boxstyle="round,pad=0.3,rounding_size=0.8",
                                facecolor='#FFFFFF', edgecolor=c_fusion_border, linewidth=1.0)
    ax.add_patch(box_weights)
    ax.text(73.0, 46.0, 'Sample-Weighted Share', fontsize=9.5, fontweight='bold', ha='center', color='#4A148C')
    ax.text(73.0, 39.5, r'$w_i^t = \frac{n_i T_i^t}{\sum_{j=1}^K n_j T_j^t}$', fontsize=11, fontweight='bold', ha='center', color='#4A148C')
    ax.text(73.0, 32.5, r'Benign mean trust: 0.86-0.95', fontsize=8, ha='center', color='#2B6CB0')
    ax.text(73.0, 27.5, r'Attacker Weight Suppressed:', fontsize=8, ha='center', color='#C53030')
    ax.text(73.0, 22.5, r'$w_0$ = 2.5-4.8% (mean; uniform: 20%)', fontsize=8.5, fontweight='bold', ha='center', color='#9B2C2C')

    # 5. Inside Global Aggregation
    box_agg = FancyBboxPatch((86.8, 50.0), 10.0, 37.0, boxstyle="round,pad=0.3,rounding_size=0.8",
                            facecolor='#FFFFFF', edgecolor=c_global_border, linewidth=1.0)
    ax.add_patch(box_agg)
    ax.text(91.8, 82.0, 'Server Model\nUpdate', fontsize=9.5, fontweight='bold', ha='center', color='#01579B')
    ax.text(91.8, 70.5, r'$\mathbf{w}_{\mathrm{global}}^t = \sum_{i=1}^K w_i^t \mathbf{w}_i^t$', fontsize=9.5, fontweight='bold', ha='center', color='#0277BD')
    ax.text(91.8, 61.0, 'Robust Clean\nAggregation', fontsize=8, ha='center', color='#00838F')
    ax.text(91.8, 54.5, r'ASR $< 5$% (Cora)', fontsize=7.8, ha='center', color='#004D40')

    box_bcast = FancyBboxPatch((86.8, 16.0), 10.0, 30.0, boxstyle="round,pad=0.3,rounding_size=0.8",
                             facecolor='#FFFFFF', edgecolor=c_global_border, linewidth=1.0)
    ax.add_patch(box_bcast)
    ax.text(91.8, 40.0, 'Broadcast\nto Clients', fontsize=9.5, fontweight='bold', ha='center', color='#01579B')
    ax.text(91.8, 31.0, r'Distribute' + '\n' + r'$\mathbf{w}_{\mathrm{global}}^t$' + '\n' + r'for Round $t+1$', fontsize=8.5, ha='center', color='#0277BD')

    # ================= FLOW ARROWS =================
    arrow_props = dict(arrowstyle="-|>", color="#2D3748", lw=1.5, mutation_scale=12)

    # From Clients to Phase 1 (Graphs $G_i^0, G_i$)
    ax.annotate('', xy=(27.0, 77.0), xytext=(22.5, 77.0), arrowprops=arrow_props)
    ax.text(24.75, 78.5, r'$G_i, G_i^0$', fontsize=8.2, ha='center', color='#2D3748', fontweight='bold')

    # From Clients to Phase 2 (Model Deltas $\Delta\mathbf{w}_i^t$)
    ax.annotate('', xy=(27.0, 31.0), xytext=(22.5, 31.0), arrowprops=arrow_props)
    ax.text(24.75, 32.5, r'$\Delta\mathbf{w}_i^t$', fontsize=8.2, ha='center', color='#2D3748', fontweight='bold')

    # Inside Phase 1: Desc -> Drift
    ax.annotate('', xy=(43.25, 73.0), xytext=(43.25, 75.0), arrowprops=dict(arrowstyle="-|>", color=c_topo_border, lw=1.2, mutation_scale=10))

    # Inside Phase 2: Median -> Score
    ax.annotate('', xy=(43.25, 29.5), xytext=(43.25, 31.5), arrowprops=dict(arrowstyle="-|>", color=c_upd_border, lw=1.2, mutation_scale=10))

    # Phase 1 to Fused Risk (Route cleanly)
    ax.annotate('', xy=(62.5, 74.0), xytext=(58.0, 65.0),
                arrowprops=dict(arrowstyle="-|>", color='#C05621', lw=1.5, mutation_scale=12, connectionstyle="arc3,rad=-0.12"))
    ax.text(59.5, 72.0, r'$A_{\mathrm{topo}, i}$', fontsize=9, fontweight='bold', color='#C05621', ha='center')

    # Phase 2 to Fused Risk (Route cleanly)
    ax.annotate('', xy=(62.5, 61.0), xytext=(58.0, 22.5),
                arrowprops=dict(arrowstyle="-|>", color='#2E7D32', lw=1.5, mutation_scale=12, connectionstyle="arc3,rad=0.14"))
    ax.text(59.5, 43.0, r'$A_{\mathrm{upd}, i}^t$', fontsize=9, fontweight='bold', color='#2E7D32', ha='center')

    # Fused Risk to Trust Weights
    ax.annotate('', xy=(73.0, 50.5), xytext=(73.0, 54.5), arrowprops=dict(arrowstyle="-|>", color='#7B1FA2', lw=1.5, mutation_scale=10))
    ax.text(75.5, 52.5, r'$T_i^t$', fontsize=8.5, fontweight='bold', color='#7B1FA2')

    # Trust Weights to Aggregation (Route through top-right)
    ax.annotate('', xy=(86.8, 66.0), xytext=(83.5, 33.0),
                arrowprops=dict(arrowstyle="-|>", color='#4A148C', lw=1.5, mutation_scale=12, connectionstyle="arc3,rad=-0.14"))
    ax.text(85.5, 51.0, r'$w_i^t$', fontsize=9, fontweight='bold', color='#4A148C')

    # Aggregation to Broadcast
    ax.annotate('', xy=(91.8, 46.0), xytext=(91.8, 50.0), arrowprops=dict(arrowstyle="-|>", color='#0277BD', lw=1.5, mutation_scale=10))

    # Broadcast back to Clients (Feedback Loop cleanly at the bottom, outside all boxes)
    ax.annotate('', xy=(12.4, 4.0), xytext=(91.8, 4.0),
                arrowprops=dict(arrowstyle="-|>", color='#0288D1', lw=2.2, mutation_scale=14, linestyle='-'))
    # Connect from Broadcast box to loop
    ax.annotate('', xy=(91.8, 4.0), xytext=(91.8, 16.0),
                arrowprops=dict(arrowstyle="-", color='#0288D1', lw=2.2, linestyle='-'))
    # Connect from loop to Clients box
    ax.annotate('', xy=(12.4, 9.5), xytext=(12.4, 4.0),
                arrowprops=dict(arrowstyle="-|>", color='#0288D1', lw=2.2, mutation_scale=14, linestyle='-'))

    ax.text(52.0, 5.8, r'Global Model Broadcast: $\mathbf{w}_{\mathrm{global}}^t$ distributed to all clients for Round $t+1$',
            fontsize=10.0, fontweight='bold', ha='center', color='#01579B')

    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)
    plt.savefig(output_pdf, format='pdf', bbox_inches='tight', dpi=300)
    plt.savefig(output_png, format='png', bbox_inches='tight', dpi=300)
    plt.close()
    print(f"Successfully generated: {output_pdf} and {output_png}")

if __name__ == '__main__':
    pdf_path = os.path.abspath('images/etdfgl/etdfgl_architecture_workflow.pdf')
    png_path = os.path.abspath('images/etdfgl/etdfgl_architecture_workflow.png')
    create_architecture_diagram(pdf_path, png_path)
