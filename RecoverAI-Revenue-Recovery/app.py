
import streamlit as st
import pandas as pd
import os

# --------------------------------------------------
# Paths
# --------------------------------------------------

DATA_DIR = "/content/recoverai/data"

TRANSACTIONS_FILE = os.path.join(DATA_DIR, "transactions.csv")
CUSTOMERS_FILE = os.path.join(DATA_DIR, "customers.csv")
RECOVERY_LOGS_FILE = os.path.join(DATA_DIR, "recovery_logs.csv")


# --------------------------------------------------
# Load data
# --------------------------------------------------

transactions = pd.read_csv(TRANSACTIONS_FILE)
customers = pd.read_csv(CUSTOMERS_FILE)

if os.path.exists(RECOVERY_LOGS_FILE):
    recovery_logs = pd.read_csv(RECOVERY_LOGS_FILE)
else:
    recovery_logs = pd.DataFrame()


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="RecoverAI",
    page_icon="💳",
    layout="wide"
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("💳 RecoverAI")
st.subheader("AI Revenue Recovery Dashboard")

st.markdown(
    "Recover failed and abandoned payments using "
    "intelligent recovery strategies."
)


# --------------------------------------------------
# Metrics
# --------------------------------------------------

total_transactions = len(transactions)

failed_count = len(
    transactions[
        transactions["status"].isin(["failed", "abandoned"])
    ]
)

recovered_count = 0

if not recovery_logs.empty and "success" in recovery_logs.columns:
    recovered_count = int(
        recovery_logs["success"].astype(bool).sum()
    )

total_revenue = 0

if "amount" in transactions.columns:
    total_revenue = transactions["amount"].sum()


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Transactions",
        total_transactions
    )

with col2:
    st.metric(
        "Failed / Abandoned",
        failed_count
    )

with col3:
    st.metric(
        "Recovery Events",
        len(recovery_logs)
    )

with col4:
    st.metric(
        "Transaction Value",
        f"${total_revenue:,.2f}"
    )


# --------------------------------------------------
# Transactions
# --------------------------------------------------

st.divider()

st.header("📋 Transactions")

st.dataframe(
    transactions,
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# Recovery logs
# --------------------------------------------------

st.divider()

st.header("🔄 Recovery Activity")

if recovery_logs.empty:
    st.info("No recovery events available.")
else:
    st.dataframe(
        recovery_logs,
        use_container_width=True,
        hide_index=True
    )


# --------------------------------------------------
# Human review queue
# --------------------------------------------------

st.divider()

st.header("👤 Human Review Queue")

if not recovery_logs.empty and "recommended_strategy" in recovery_logs.columns:

    human_queue = recovery_logs[
        recovery_logs["recommended_strategy"].isin(
            ["escalate_to_human", "human_review"]
        )
    ]

    if len(human_queue) > 0:
        st.warning(
            f"{len(human_queue)} payment(s) require human review."
        )

        st.dataframe(
            human_queue,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.success(
            "No payments currently require human approval."
        )

else:
    st.info(
        "Human review information is not available yet."
    )


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()

st.caption(
    "RecoverAI — AI Revenue Recovery"
)
