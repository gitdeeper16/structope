import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
np.random.seed(42)
fig, ax = plt.subplots(figsize=(16,9), dpi=240)
fig.patch.set_facecolor("white")
sc=["S1","S2","S3","S4","S5","S6"]
co=["#4C72B0","#DD8452","#55A868","#C44E52","#8172B3","#937860"]
rh=[0.82,0.79,0.85,0.71,0.88,0.76]
for i,(s,c) in enumerate(zip(sc,co)):
    n=7 if i<4 else 6
    t=np.random.uniform(0.15,0.9,n)
    o=t+np.random.normal(0,(1-rh[i])*0.35,n)
    ax.scatter(t,o,s=90,color=c,alpha=0.75,edgecolor="black",linewidth=0.6,label=f"{s}: ρ={rh[i]:.2f}")
ax.plot([0,1],[0,1],"k--",lw=1.2,alpha=0.6,label="y = x")
ax.set_xlim(0,1); ax.set_ylim(0,1)
ax.set_xlabel("True Utility (B4 direct)",fontsize=13)
ax.set_ylabel("OPE-Estimated Utility",fontsize=13)
ax.set_title("Figure 8 (illustrative): Pilot-1 Ranking Fidelity",fontsize=15,fontweight="bold")
ax.legend(loc="lower right",fontsize=10,framealpha=0.95)
plt.tight_layout(rect=[0,0.04,1,1])
plt.savefig("fig08_pilot1_ranking_fidelity.png",dpi=240,bbox_inches="tight",facecolor="white")
plt.close()
print("Saved: fig08_pilot1_ranking_fidelity.png")
