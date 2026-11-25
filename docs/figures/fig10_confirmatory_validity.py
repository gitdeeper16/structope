import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig,ax=plt.subplots(figsize=(16,9),dpi=240); fig.patch.set_facecolor("white")
m=["B1a","B1b","B2","B3a","B3b","B4"]
sp=[0.81,0.78,0.84,0.73,0.76,0.88]
ke=[0.64,0.61,0.68,0.57,0.60,0.72]
tk=[0.75,0.71,0.80,0.66,0.69,0.85]
x=np.arange(len(m)); w=0.27
ax.bar(x-w,sp,w,label="Spearman ρ",color="#2C5F8D")
ax.bar(x,ke,w,label="Kendall τ",color="#F4B400")
ax.bar(x+w,tk,w,label="Top-k overlap",color="#4CAF50")
ax.axhline(0.70,color="#E53935",ls="--",lw=2,label="τ_min = 0.70 (frozen)")
ax.set_xticks(x); ax.set_xticklabels(m,fontsize=12)
ax.set_ylabel("Agreement with true ranking (B4)",fontsize=13)
ax.set_xlabel("OPE Estimator",fontsize=13)
ax.set_title("Figure 10 (illustrative): Confirmatory Validity across Estimators",fontsize=15,fontweight="bold")
ax.set_ylim(0,1.0); ax.grid(True,axis="y",alpha=0.3)
ax.legend(loc="lower right",fontsize=10,framealpha=0.95,ncol=2)
plt.tight_layout(rect=[0,0.04,1,1])
plt.savefig("fig10_confirmatory_validity.png",dpi=240,bbox_inches="tight",facecolor="white")
plt.close()
print("Saved: fig10_confirmatory_validity.png")
