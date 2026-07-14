import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="EMI Calculator",
    page_icon="💰",
    layout="wide"
)

st.title("💰 EMI Calculator")
st.write("Calculate your EMI and view the repayment schedule.")

# -----------------------------
# Sidebar Inputs
# -----------------------------

st.sidebar.header("Loan Details")

principal = st.sidebar.number_input(
    "Loan Amount (₹)",
    min_value=1000.0,
    value=1500000.0,
    step=10000.0
)

annual_rate = st.sidebar.number_input(
    "Annual Interest Rate (%)",
    min_value=0.1,
    value=8.0,
    step=0.1
)

years = st.sidebar.number_input(
    "Loan Tenure (Years)",
    min_value=1,
    value=5,
    step=1
)

# -----------------------------
# EMI Function
# -----------------------------

r = annual_rate / (12 * 100)
n = years * 12

emi = (principal * r * (1 + r) ** n) / ((1 + r) ** n - 1)

balance = principal

data = []

total_interest = 0

for month in range(1, n + 1):

    interest = balance * r
    principal_paid = emi - interest
    closing_balance = balance - principal_paid

    if closing_balance < 0:
        principal_paid += closing_balance
        closing_balance = 0

    total_interest += interest

    data.append({
        "Month": month,
        "Opening Balance": round(balance,2),
        "Interest": round(interest,2),
        "Principal": round(principal_paid,2),
        "EMI": round(emi,2),
        "Closing Balance": round(closing_balance,2)
    })

    balance = closing_balance

df = pd.DataFrame(data)

# -----------------------------
# Top Metrics
# -----------------------------

col1, col2, col3 = st.columns(3)

col1.metric("Monthly EMI", f"₹{emi:,.2f}")

col2.metric("Total Interest", f"₹{total_interest:,.2f}")

col3.metric("Total Payment", f"₹{principal+total_interest:,.2f}")

st.divider()

# -----------------------------
# First 5 Months Preview
# -----------------------------

st.subheader("First 5 Months")

st.dataframe(df.head(), use_container_width=True)

# -----------------------------
# Full Schedule
# -----------------------------

show = st.checkbox("Show Full Repayment Schedule")

if show:
    st.dataframe(df, use_container_width=True)

# -----------------------------
# Download CSV
# -----------------------------

csv = df.to_csv(index=False).encode()

st.download_button(
    "📥 Download Schedule",
    csv,
    file_name="EMI_Schedule.csv",
    mime="text/csv"
)

st.divider()

# -----------------------------
# Loan Balance Graph
# -----------------------------

st.subheader("Loan Balance")

fig, ax = plt.subplots(figsize=(10,4))

ax.plot(df["Month"], df["Closing Balance"])

ax.set_xlabel("Month")

ax.set_ylabel("Remaining Loan")

st.pyplot(fig)

# -----------------------------
# Interest vs Principal
# -----------------------------

st.subheader("Interest vs Principal")

fig2, ax2 = plt.subplots(figsize=(10,4))

ax2.plot(df["Month"], df["Interest"], label="Interest")

ax2.plot(df["Month"], df["Principal"], label="Principal")

ax2.legend()

ax2.set_xlabel("Month")

st.pyplot(fig2)

st.divider()

with st.expander("📚 Learn About EMI"):

    st.header("What is EMI?")

    st.write("""
EMI (Equated Monthly Installment) is the fixed amount that you pay every month to repay a loan.

Each EMI consists of:

- Interest Amount
- Principal Amount

In the beginning, most of your EMI goes towards interest.
As time passes, a larger portion goes towards repaying the principal.
""")

    st.subheader("EMI Formula")

    st.latex(r"""
EMI=
\frac{P\times R\times(1+R)^N}
{(1+R)^N-1}
""")

    st.subheader("Meaning of Variables")

    st.markdown("""
| Symbol | Meaning |
|--------|---------|
| **P** | Loan Amount (Principal) |
| **R** | Monthly Interest Rate = Annual Rate / (12 × 100) |
| **N** | Total Number of Monthly Installments |
| **EMI** | Monthly Payment |
""")

    st.subheader("Monthly Interest Formula")

    st.latex(r"""
R=\frac{\text{Annual Interest Rate}}
{12\times100}
""")

    st.subheader("Example")

    st.write("""
Loan Amount = ₹15,00,000

Interest Rate = 8%

Time = 5 Years
""")

    st.latex(r"""
R=\frac{8}{12\times100}=0.0066667
""")

    st.latex(r"""
N=5\times12=60
""")

    st.latex(r"""
EMI=
\frac{
1500000\times0.0066667\times(1.0066667)^{60}
}
{
(1.0066667)^{60}-1
}
""")

    st.success("Monthly EMI ≈ ₹30,415")

    st.subheader("How EMI Changes Every Month")

    st.markdown("""
Month 1

- Interest is Highest
- Principal Repaid is Lowest

Middle Months

- Interest decreases
- Principal repayment increases

Final Months

- Interest becomes very small
- Almost the entire EMI repays the principal
""")

    st.subheader("Why Does Interest Reduce Every Month?")

    st.info("""
Interest is always calculated on the remaining loan balance.

As your loan balance decreases every month, the interest amount also decreases.
""")

    st.subheader("Formula Used in This Calculator")

    st.code("""
r = annual_rate / (12 * 100)

n = years * 12

emi = (principal * r * (1+r)**n) / ((1+r)**n - 1)
""", language="python")