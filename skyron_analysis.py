import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.animation as animation

# ====== DATA SETUP (12 QUARTERS) ======
quarters = [f'Q{i//4+1}-{2026+i//4}' for i in range(12)]
df = pd.DataFrame({
    "quarter": quarters,
    "revenue_cr": [0, 0.10, 0.25, 0.5, 1, 1.5, 2.5, 3, 5, 7, 15, 22],
    "investment_lakhs": [20, 15, 12, 13, 0, 0, 0, 0, 0, 0, 0, 0],
    "manufacturing_lakhs": [7.4, 5.6, 4.4, 4.8, 0, 0, 0, 0, 0, 0, 0, 0],
    "gross_margin": np.linspace(0.65, 0.85, 12),
    "cac": np.linspace(2000, 550, 12),
    "ltv": np.linspace(8000, 40000, 12),
})
df["cumulative_revenue"] = df["revenue_cr"].cumsum()
df["cash_position"] = (df["revenue_cr"]*100 - df["investment_lakhs"]).cumsum()

# ====== 1. QUARTERLY & CUMULATIVE REVENUE CHART ======
plt.figure(figsize=(10, 7))
plt.bar(df["quarter"], df["revenue_cr"], color="skyblue", label="Quarterly Revenue")
plt.plot(df["quarter"], df["cumulative_revenue"], color="navy", linestyle="--", marker="o", label="Cumulative Revenue")
plt.xlabel("Quarter")
plt.ylabel("Revenue (Cr)")
plt.title("Projected Quarterly & Cumulative Revenue")
plt.legend()
plt.tight_layout()
plt.savefig("skyron_revenue.png")
plt.clf()

# ====== 2. INVESTMENT & MANUFACTURING CHART ======
plt.figure(figsize=(10, 7))
plt.bar(df["quarter"], df["investment_lakhs"], color="coral", label="Total Investment")
plt.bar(df["quarter"], df["manufacturing_lakhs"], color="gold", alpha=0.7, label="Manufacturing", bottom=0)
plt.xlabel("Quarter")
plt.ylabel("Investment (Lakh ₹)")
plt.title("Quarterly Investment & Manufacturing Spend")
plt.legend()
plt.tight_layout()
plt.savefig("skyron_investment.png")
plt.clf()

# ====== 3. PROFITABILITY: GROSS MARGIN & CASH POSITION ======
fig, ax1 = plt.subplots(figsize=(10,7))
ax2 = ax1.twinx()
ax1.plot(df["quarter"], df["gross_margin"]*100, color="green", marker="^", label="Gross Margin (%)")
ax2.plot(df["quarter"], df["cash_position"], color="darkred", marker="*", label="Cash Position")
ax1.set_ylabel("Gross Margin (%)", color="green")
ax2.set_ylabel("Cumulative Cash (₹ Lakh)", color="darkred")
plt.title("Margin Improvement & Cash Flow Evolution")
fig.legend(loc="upper left", bbox_to_anchor=(0.12, 0.92))
plt.tight_layout()
plt.savefig("skyron_margin_cash.png")
plt.clf()

# ====== 4. CAC & LTV PROGRESSION ======
plt.figure(figsize=(10, 7))
plt.plot(df["quarter"], df["cac"], color="red", label="Customer Acquisition Cost")
plt.plot(df["quarter"], df["ltv"], color="blue", label="Lifetime Value")
plt.xlabel("Quarter")
plt.ylabel("₹")
plt.title("CAC Reduction & LTV Growth")
plt.legend()
plt.tight_layout()
plt.savefig("skyron_cac_ltv.png")
plt.clf()

# ====== 5. PAYBACK & ROI SCENARIO ======
roi = (df["cumulative_revenue"].iloc[-1]/0.6) * 100  # Final revenue / ₹60L seed capital in cr * 100
quarters_profitable = np.argmax(df["cash_position"] > 0)
plt.figure(figsize=(8, 5))
plt.plot(df["quarter"], df["cash_position"], color="royalblue")
plt.axhline(0, color='gray', linestyle=':', linewidth=1)
plt.annotate("Payback Occurs", (quarters_profitable, df["cash_position"].iloc[quarters_profitable]), 
             textcoords="offset points", xytext=(0, 10), ha='center', color="red")
plt.title(f"Cumulative Cash Position | ROI: {roi:.1f}% | Payback: Q{quarters_profitable+1}")
plt.ylabel("Cumulative Cash (₹ Lakh)")
plt.tight_layout()
plt.savefig("skyron_payback.png")
plt.clf()

# ====== 6. ANIMATED REVENUE CHART ======
fig_anim, ax_anim = plt.subplots(figsize=(10, 6))
bar_anim = ax_anim.bar(df["quarter"], np.zeros_like(df["revenue_cr"]), color="teal")
def animate_revenue(i):
    for idx, bar in enumerate(bar_anim):
        bar.set_height(df["revenue_cr"].iloc[idx] if idx <= i else 0)
    ax_anim.set_title(f"Quarterly Revenue Progression (Q{i+1} Highlighted)")
ani = animation.FuncAnimation(fig_anim, animate_revenue, frames=len(df), repeat=False)
ani.save("skyron_animated_revenue.gif", writer='imagemagick')

# ====== 7. GROSS MARGIN SENSITIVITY SCENARIO ======
margins = [0.65, 0.7, 0.75, 0.8, 0.85]
end_revenue = []
for mg in margins:
    df["gm"] = np.linspace(mg, mg+0.2, 12)
    df["cash"] = (df["revenue_cr"] * 100 * df["gm"] - df["investment_lakhs"]).cumsum()
    end_revenue.append(df["cash"].iloc[-1])
plt.figure(figsize=(8, 5))
plt.plot([f"{int(m*100)}%" for m in margins], end_revenue, color='purple', marker="o")
plt.title("End Cash Position vs Gross Margin Scenario")
plt.xlabel("Gross Margin (%)")
plt.ylabel("End Cash (₹ Lakh)")
plt.tight_layout()
plt.savefig("skyron_margin_sensitivity.png")
plt.clf()
