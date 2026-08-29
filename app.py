import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, datetime, timedelta

from database import (
    initialize_database,
    add_expense,
    get_expenses,
    delete_expense,
    set_budget,
    get_budget,
)

from analytics import (
    get_total_spending,
    get_average_spending,
    get_transaction_count,
    get_category_summary,
    get_payment_summary,
    get_monthly_summary,
    get_highest_category,
)

from report_generator import (
    generate_csv_report,
    generate_pdf_report,
)


# ============================================================
# CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="SpendWise",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# DESIGN SYSTEM
# ============================================================

BG = "#0f1117"
SURFACE = "#1a1d27"
SURFACE_2 = "#242837"
ACCENT = "#4f8ef7"
ACCENT_LIGHT = "#6ba3ff"
TEXT = "#f0f2f8"
TEXT_SECONDARY = "#8b92a8"
BORDER = "#2d3245"
SUCCESS = "#22c55e"
WARNING = "#f59e0b"
DANGER = "#ef4444"


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
    <style>

    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
    );

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background: {BG};
        color: {TEXT};
    }

    .main {
        background: {BG};
    }

    /* Hide Streamlit branding */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    /* Main content width */
    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: {SURFACE};
        border-right: 1px solid {BORDER};
    }

    section[data-testid="stSidebar"] > div {
        padding: 1.5rem 1rem;
    }

    /* Sidebar branding */
    .brand {
        padding: 10px 8px 28px 8px;
    }

    .brand-name {
        font-size: 25px;
        font-weight: 800;
        color: {TEXT};
        letter-spacing: -0.8px;
    }

    .brand-tagline {
        font-size: 12px;
        color: {TEXT_SECONDARY};
        margin-top: 4px;
    }

    .sidebar-label {
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: {TEXT_SECONDARY};
        margin: 18px 8px 10px 8px;
    }

    /* Page header */
    .page-eyebrow {
        color: {ACCENT_LIGHT};
        font-size: 12px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1.4px;
        margin-bottom: 7px;
    }

    .page-title {
        color: {TEXT};
        font-size: 34px;
        font-weight: 800;
        letter-spacing: -1.2px;
        line-height: 1.15;
        margin: 0;
    }

    .page-subtitle {
        color: {TEXT_SECONDARY};
        font-size: 14px;
        margin-top: 8px;
        margin-bottom: 28px;
    }

    /* KPI cards */
    .kpi-card {
        background: {SURFACE};
        border: 1px solid {BORDER};
        border-radius: 16px;
        padding: 20px;
        min-height: 138px;
        position: relative;
        overflow: hidden;
    }

    .kpi-card::before {
        content: "";
        position: absolute;
        left: 0;
        top: 0;
        bottom: 0;
        width: 3px;
        background: {ACCENT};
    }

    .kpi-label {
        color: {TEXT_SECONDARY};
        font-size: 12px;
        font-weight: 600;
        margin-bottom: 12px;
    }

    .kpi-value {
        color: {TEXT};
        font-size: 27px;
        font-weight: 800;
        letter-spacing: -0.8px;
    }

    .kpi-description {
        color: {TEXT_SECONDARY};
        font-size: 11px;
        margin-top: 9px;
    }

    /* General cards */
    .card {
        background: {SURFACE};
        border: 1px solid {BORDER};
        border-radius: 16px;
        padding: 22px;
    }

    .card-title {
        color: {TEXT};
        font-size: 16px;
        font-weight: 700;
        margin-bottom: 4px;
    }

    .card-description {
        color: {TEXT_SECONDARY};
        font-size: 12px;
        margin-bottom: 16px;
    }

    /* Budget */
    .budget-card {
        background: {SURFACE};
        border: 1px solid {BORDER};
        border-radius: 16px;
        padding: 24px;
        margin-top: 22px;
    }

    .budget-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    .budget-title {
        font-size: 17px;
        font-weight: 700;
        color: {TEXT};
    }

    .budget-month {
        font-size: 12px;
        color: {TEXT_SECONDARY};
    }

    .budget-numbers {
        display: flex;
        gap: 42px;
        margin-top: 22px;
        margin-bottom: 16px;
    }

    .budget-number-label {
        font-size: 11px;
        color: {TEXT_SECONDARY};
    }

    .budget-number-value {
        font-size: 19px;
        font-weight: 700;
        color: {TEXT};
        margin-top: 3px;
    }

    .progress-track {
        height: 8px;
        background: {SURFACE_2};
        border-radius: 100px;
        overflow: hidden;
        margin-top: 15px;
    }

    .progress-fill {
        height: 100%;
        border-radius: 100px;
    }

    .progress-text {
        display: flex;
        justify-content: space-between;
        margin-top: 9px;
        font-size: 14px;
        color: {TEXT_SECONDARY};
    }

    /* Transaction cards */
    .transaction {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 14px 0;
        border-bottom: 1px solid {BORDER};
    }

    .transaction:last-child {
        border-bottom: none;
    }

    .transaction-left {
        display: flex;
        align-items: center;
        gap: 13px;
    }

    .transaction-icon {
        width: 38px;
        height: 38px;
        border-radius: 11px;
        background: {SURFACE_2};
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
    }

    .transaction-category {
        color: {TEXT};
        font-size: 13px;
        font-weight: 600;
    }

    .transaction-description {
        color: {TEXT_SECONDARY};
        font-size: 11px;
        margin-top: 3px;
    }

    .transaction-amount {
        color: {TEXT};
        font-size: 13px;
        font-weight: 700;
    }

    /* Section spacing */
    .section-gap {
        height: 22px;
    }

    /* Buttons */
    .stButton > button {
        background: {ACCENT};
        color: white;
        border: none;
        border-radius: 9px;
        font-weight: 600;
        min-height: 42px;
        transition: 0.15s ease;
    }

    .stButton > button:hover {
        background: {ACCENT_LIGHT};
        color: white;
        border: none;
    }

    /* Form */
    div[data-testid="stForm"] {
        background: {SURFACE};
        border: 1px solid {BORDER};
        border-radius: 16px;
        padding: 26px;
    }

    /* Inputs */
    .stTextInput input,
    .stNumberInput input,
    .stDateInput input {
        background: {SURFACE_2} !important;
        color: {TEXT} !important;
        border: 1px solid {BORDER} !important;
        border-radius: 9px !important;
    }

    div[data-baseweb="select"] > div {
        background: {SURFACE_2} !important;
        border-color: {BORDER} !important;
        border-radius: 9px !important;
    }

    /* Dataframe */
    div[data-testid="stDataFrame"] {
        border: 1px solid {BORDER};
        border-radius: 12px;
        overflow: hidden;
    }

    /* Download buttons */
    .stDownloadButton > button {
        width: 100%;
        background: {SURFACE_2};
        color: {TEXT};
        border: 1px solid {BORDER};
        border-radius: 9px;
        min-height: 42px;
        font-weight: 600;
    }

    .stDownloadButton > button:hover {
        border-color: {ACCENT};
        color: {ACCENT_LIGHT};
    }

    /* Tabs */
    button[data-baseweb="tab"] {
        color: {TEXT_SECONDARY};
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: {ACCENT_LIGHT};
    }

    /* Alerts */
    div[data-testid="stAlert"] {
        border-radius: 10px;
    }

        /* =========================================================
       READABLE TYPOGRAPHY
       ========================================================= */

    /* Main application text */
    .stApp {
        font-size: 16px !important;
    }

    /* Page supporting text */
    .card-description,
    .subtitle,
    .helper-text,
    .progress-text {
        font-size: 15px !important;
        line-height: 1.5 !important;
    }

    /* Transaction text */
    .transaction {
        font-size: 16px !important;
        line-height: 1.5 !important;
    }

    /* Metric labels */
    [data-testid="stMetricLabel"] {
        font-size: 15px !important;
        font-weight: 600 !important;
    }

    /* Metric values */
    [data-testid="stMetricValue"] {
        font-size: 30px !important;
        font-weight: 700 !important;
    }

    /* Metric supporting text */
    [data-testid="stMetricDelta"] {
        font-size: 14px !important;
    }

    /* Normal Streamlit text */
    .stMarkdown {
        font-size: 16px !important;
    }

    /* Captions */
    .stCaption {
        font-size: 14px !important;
    }

    /* Input fields */
    .stTextInput input,
    .stNumberInput input,
    .stDateInput input {
        font-size: 16px !important;
    }

    /* Select boxes */
    .stSelectbox,
    .stMultiSelect {
        font-size: 16px !important;
    }

    /* Buttons */
    .stButton button,
    .stDownloadButton button {
        font-size: 16px !important;
        font-weight: 600 !important;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        font-size: 16px !important;
    }

    section[data-testid="stSidebar"] label {
        font-size: 15px !important;
    }
    

    </style>
    """.replace("{BG}", BG).replace("{TEXT}", TEXT).replace("{SURFACE}", SURFACE).replace("{BORDER}", BORDER).replace("{TEXT_SECONDARY}", TEXT_SECONDARY).replace("{ACCENT}", ACCENT).replace("{ACCENT_LIGHT}", ACCENT_LIGHT).replace("{SURFACE_2}", SURFACE_2),
    unsafe_allow_html=True,
)


# ============================================================
# HELPERS
# ============================================================

def money(value):
    return f"₹{value:,.0f}"


def get_category_icon(category):
    icons = {
        "Food": "🍴",
        "Transport": "↗",
        "Shopping": "◈",
        "Bills": "▣",
        "Entertainment": "▶",
        "Healthcare": "+",
        "Education": "◇",
        "Other": "•",
    }

    return icons.get(category, "•")


def style_plot(fig, height=330):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(
            family="Inter",
            color=TEXT_SECONDARY,
            size=11,
        ),
        margin=dict(
            l=10,
            r=10,
            t=15,
            b=10,
        ),
        hoverlabel=dict(
            bgcolor=SURFACE_2,
            font_color=TEXT,
        ),
        legend=dict(
            font=dict(color=TEXT_SECONDARY),
        ),
    )

    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        linecolor=BORDER,
    )

    fig.update_yaxes(
        showgrid=True,
        gridcolor=BORDER,
        zeroline=False,
    )

    return fig


def page_header(eyebrow, title, subtitle):
    st.markdown(
        f"""
        <div class="page-eyebrow">{eyebrow}</div>
        <h1 class="page-title">{title}</h1>
        <div class="page-subtitle">{subtitle}</div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# DATABASE
# ============================================================

initialize_database()

df = get_expenses()

if not df.empty:
    df["date"] = pd.to_datetime(df["date"])


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand">
            <div class="brand-name">SpendWise</div>
            <div class="brand-tagline">Personal Finance Manager</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-label">Workspace</div>',
        unsafe_allow_html=True,
    )

    page = st.radio(
        "Navigation",
        [
            "Overview",
            "Add Expense",
            "Transactions",
            "Analytics",
            "Reports",
        ],
        label_visibility="collapsed",
    )

    st.markdown("---")

    if not df.empty:

        st.markdown(
            '<div class="sidebar-label">Quick Stats</div>',
            unsafe_allow_html=True,
        )

        sidebar_total = get_total_spending(df)

        st.caption(f"Total tracked: {money(sidebar_total)}")
        st.caption(f"Transactions: {len(df)}")

    st.markdown("---")

    st.caption("SpendWise v1.0")
    st.caption("Personal finance analytics")


# ============================================================
# OVERVIEW
# ============================================================

if page == "Overview":

    current_hour = datetime.now().hour

    if current_hour < 12:
        greeting = "Good morning"
    elif current_hour < 18:
        greeting = "Good afternoon"
    else:
        greeting = "Good evening"

    page_header(
        "Overview",
        f"{greeting}",
        "Here's your spending overview for the current period.",
    )

    if df.empty:

        st.markdown(
            """
            <div class="card">
                <div class="card-title">Your dashboard is ready</div>
                <div class="card-description">
                    Start by adding your first expense to begin tracking
                    your spending.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("###")

        col1, col2 = st.columns(2)

        with col1:
            if st.button(
                "＋  Add your first expense",
                use_container_width=True,
            ):
                st.session_state["navigation"] = "Add Expense"
                st.rerun()

        with col2:
            st.info(
                "Your spending analytics will appear here once you add transactions."
            )

    else:

        # ----------------------------------------------------
        # KPI DATA
        # ----------------------------------------------------

        total_spending = get_total_spending(df)

        current_month = date.today().strftime("%Y-%m")

        monthly_df = df[
            df["date"].dt.strftime("%Y-%m") == current_month
        ]

        monthly_spending = monthly_df["amount"].sum()

        monthly_budget = get_budget(current_month)

        remaining = monthly_budget - monthly_spending

        transactions = get_transaction_count(df)

        # ----------------------------------------------------
        # KPI CARDS
        # ----------------------------------------------------

        c1, c2, c3, c4 = st.columns(4)

        with c1:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-label">TOTAL SPENDING</div>
                    <div class="kpi-value">{money(total_spending)}</div>
                    <div class="kpi-description">
                        Across all tracked expenses
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with c2:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-label">MONTHLY BUDGET</div>
                    <div class="kpi-value">
                        {money(monthly_budget) if monthly_budget else "—"}
                    </div>
                    <div class="kpi-description">
                        {date.today().strftime("%B %Y")}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with c3:

            remaining_display = (
                money(remaining)
                if monthly_budget
                else "—"
            )

            description = (
                "Available this month"
                if monthly_budget
                else "Set a monthly budget"
            )

            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-label">REMAINING</div>
                    <div class="kpi-value">{remaining_display}</div>
                    <div class="kpi-description">
                        {description}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with c4:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-label">TRANSACTIONS</div>
                    <div class="kpi-value">{transactions}</div>
                    <div class="kpi-description">
                        Recorded transactions
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # ----------------------------------------------------
        # BUDGET
        # ----------------------------------------------------

        st.markdown(
            """
            <div class="section-gap"></div>
            """,
            unsafe_allow_html=True,
        )

        budget_col1, budget_col2 = st.columns(
            [2.4, 1],
            gap="large",
        )

        with budget_col1:

            if monthly_budget > 0:

                usage = monthly_spending / monthly_budget
                percentage = usage * 100

                if usage >= 1:
                    progress_color = DANGER
                    status = "Budget exceeded"
                elif usage >= 0.8:
                    progress_color = WARNING
                    status = "Approaching budget limit"
                else:
                    progress_color = SUCCESS
                    status = "Within budget"

                width = min(percentage, 100)

                st.markdown(
                    f"""
                    <div class="budget-card">
                        <div class="budget-top">
                            <div>
                                <div class="budget-title">
                                    Monthly Budget
                                </div>
                                <div class="budget-month">
                                    {date.today().strftime("%B %Y")}
                                </div>
                            </div>
                            <div style="
                                color:{progress_color};
                                font-size:12px;
                                font-weight:700;
                            ">
                                {status}
                            </div>
                        </div>

                        <div class="budget-numbers">

                            <div>
                                <div class="budget-number-label">
                                    SPENT
                                </div>
                                <div class="budget-number-value">
                                    {money(monthly_spending)}
                                </div>
                            </div>

                            <div>
                                <div class="budget-number-label">
                                    BUDGET
                                </div>
                                <div class="budget-number-value">
                                    {money(monthly_budget)}
                                </div>
                            </div>

                            <div>
                                <div class="budget-number-label">
                                    REMAINING
                                </div>
                                <div class="budget-number-value">
                                    {money(max(remaining, 0))}
                                </div>
                            </div>

                        </div>

                        <div class="progress-track">
                            <div class="progress-fill"
                                style="
                                    width:{width}%;
                                    background:{progress_color};
                                ">
                            </div>
                        </div>

                        <div class="progress-text">
                            <span>
                                {percentage:.1f}% used
                            </span>
                            <span>
                                {money(monthly_budget)}
                            </span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            else:

                st.markdown(
                    """
                    <div class="budget-card">
                        <div class="budget-title">
                            Monthly Budget
                        </div>
                        <div class="budget-month">
                            Set a limit to monitor your spending.
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        with budget_col2:

            st.markdown(
                '<div class="card-title">Budget Settings</div>',
                unsafe_allow_html=True,
            )

            budget_input = st.number_input(
                "Monthly limit",
                min_value=0.0,
                value=float(monthly_budget),
                step=500.0,
                label_visibility="collapsed",
            )

            if st.button(
                "Update Budget",
                use_container_width=True,
            ):

                set_budget(
                    current_month,
                    budget_input,
                )

                st.success("Budget updated.")

                st.rerun()

        # ----------------------------------------------------
        # CHARTS
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-gap"></div>',
            unsafe_allow_html=True,
        )

        chart1, chart2 = st.columns(
            [1.55, 1],
            gap="large",
        )

        with chart1:

            st.markdown(
                """
                <div class="card-title">
                    Spending Over Time
                </div>
                <div class="card-description">
                    Track how your expenses change over time.
                </div>
                """,
                unsafe_allow_html=True,
            )

            daily = (
                df.groupby("date")["amount"]
                .sum()
                .reset_index()
            )

            fig = px.area(
                daily,
                x="date",
                y="amount",
                labels={
                    "date": "",
                    "amount": "Amount",
                },
            )

            fig.update_traces(
                line=dict(
                    color=ACCENT,
                    width=2,
                ),
                fillcolor="rgba(79,142,247,0.14)",
            )

            fig = style_plot(fig, 315)

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={
                    "displayModeBar": False,
                },
            )

        with chart2:

            st.markdown(
                """
                <div class="card-title">
                    Category Breakdown
                </div>
                <div class="card-description">
                    Where your money is going.
                </div>
                """,
                unsafe_allow_html=True,
            )

            category_data = get_category_summary(df)

            fig = px.pie(
                category_data,
                names="category",
                values="amount",
                hole=0.62,
            )

            fig.update_traces(
                textposition="outside",
                textinfo="percent",
                marker=dict(
                    line=dict(
                        color=BG,
                        width=2,
                    )
                ),
            )

            fig = style_plot(fig, 315)

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={
                    "displayModeBar": False,
                },
            )

        # ----------------------------------------------------
        # RECENT TRANSACTIONS
        # ----------------------------------------------------

        st.markdown(
            '<div class="section-gap"></div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="card-title">
                Recent Transactions
            </div>
            <div class="card-description">
                Your latest recorded expenses.
            </div>
            """,
            unsafe_allow_html=True,
        )

        recent = df.sort_values(
            "date",
            ascending=False,
        ).head(5)

        for _, row in recent.iterrows():

            description = (
                row["description"]
                if pd.notna(row["description"])
                else "No description"
            )

            st.markdown(
                f"""
                <div class="transaction">

                    <div class="transaction-left">

                        <div class="transaction-icon">
                            {get_category_icon(row["category"])}
                        </div>

                        <div>
                            <div class="transaction-category">
                                {row["category"]}
                            </div>
                            <div class="transaction-description">
                                {description}
                                · {row["date"].strftime("%d %b %Y")}
                            </div>
                        </div>

                    </div>

                    <div class="transaction-amount">
                        {money(row["amount"])}
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )


# ============================================================
# ADD EXPENSE
# ============================================================

elif page == "Add Expense":

    page_header(
        "Transactions",
        "Add Expense",
        "Record a new transaction and keep your finances organized.",
    )

    with st.form("add_expense_form"):

        st.markdown(
            """
            <div class="card-title">
                Transaction Details
            </div>
            <div class="card-description">
                Enter the details of your expense below.
            </div>
            """,
            unsafe_allow_html=True,
        )

        row1_col1, row1_col2 = st.columns(2)

        with row1_col1:
            expense_date = st.date_input(
                "Date",
                value=date.today(),
            )

        with row1_col2:
            expense_category = st.selectbox(
                "Category",
                [
                    "Food",
                    "Transport",
                    "Shopping",
                    "Bills",
                    "Entertainment",
                    "Healthcare",
                    "Education",
                    "Other",
                ],
            )

        row2_col1, row2_col2 = st.columns(2)

        with row2_col1:
            expense_amount = st.number_input(
                "Amount (₹)",
                min_value=1.0,
                step=50.0,
            )

        with row2_col2:
            expense_payment = st.selectbox(
                "Payment Method",
                [
                    "UPI",
                    "Cash",
                    "Card",
                    "Net Banking",
                ],
            )

        expense_description = st.text_input(
            "Description",
            placeholder="e.g. Lunch with friends",
        )

        st.markdown("")

        submitted = st.form_submit_button(
            "Add Expense",
            use_container_width=True,
        )

        if submitted:

            add_expense(
                expense_date,
                expense_category,
                expense_amount,
                expense_payment,
                expense_description,
            )

            st.success(
                "Expense added successfully."
            )

            st.rerun()


# ============================================================
# TRANSACTIONS
# ============================================================

elif page == "Transactions":

    page_header(
        "Transactions",
        "Transaction History",
        "Search, filter and manage your recorded expenses.",
    )

    if df.empty:

        st.info(
            "No transactions have been recorded yet."
        )

    else:

        # ----------------------------------------------------
        # FILTERS
        # ----------------------------------------------------

        filter1, filter2, filter3 = st.columns(
            [1.4, 1, 1],
            gap="medium",
        )

        with filter1:
            search = st.text_input(
                "Search",
                placeholder="Search descriptions...",
            )

        with filter2:
            category_filter = st.multiselect(
                "Category",
                sorted(df["category"].unique()),
            )

        with filter3:

            min_date = df["date"].min().date()
            max_date = df["date"].max().date()

            date_range = st.date_input(
                "Date range",
                value=(min_date, max_date),
            )

        filtered_df = df.copy()

        # Search
        if search:

            search_lower = search.lower()

            filtered_df = filtered_df[
                filtered_df["description"]
                .fillna("")
                .str.lower()
                .str.contains(
                    search_lower,
                    regex=False,
                )
            ]

        # Category
        if category_filter:

            filtered_df = filtered_df[
                filtered_df["category"].isin(
                    category_filter
                )
            ]

        # Date range
        if isinstance(date_range, tuple) and len(date_range) == 2:

            start_date = pd.Timestamp(date_range[0])
            end_date = (
                pd.Timestamp(date_range[1])
                + pd.Timedelta(days=1)
            )

            filtered_df = filtered_df[
                (filtered_df["date"] >= start_date)
                & (filtered_df["date"] < end_date)
            ]

        st.markdown("###")

        # ----------------------------------------------------
        # TABLE
        # ----------------------------------------------------

        table_df = filtered_df.copy()

        table_df["date"] = table_df["date"].dt.strftime(
            "%d %b %Y"
        )

        table_df["amount"] = table_df["amount"].apply(
            lambda x: f"₹{x:,.2f}"
        )

        table_df = table_df[
            [
                "id",
                "date",
                "category",
                "amount",
                "payment_method",
                "description",
            ]
        ]

        table_df.columns = [
            "ID",
            "Date",
            "Category",
            "Amount",
            "Payment Method",
            "Description",
        ]

        st.dataframe(
            table_df,
            use_container_width=True,
            hide_index=True,
        )

        st.caption(
            f"Showing {len(filtered_df)} transaction(s)"
        )

        # ----------------------------------------------------
        # DELETE
        # ----------------------------------------------------

        st.markdown("---")

        st.markdown(
            """
            <div class="card-title">
                Manage Transaction
            </div>
            <div class="card-description">
                Permanently remove a transaction from your database.
            </div>
            """,
            unsafe_allow_html=True,
        )

        if not filtered_df.empty:

            selected_id = st.selectbox(
                "Transaction",
                filtered_df["id"].tolist(),
                format_func=lambda x: (
                    f"Transaction #{x}"
                ),
            )

            confirm_delete = st.checkbox(
                "I understand that this transaction will be permanently deleted."
            )

            if st.button(
                "Delete Transaction",
                disabled=not confirm_delete,
            ):

                delete_expense(selected_id)

                st.success(
                    "Transaction deleted successfully."
                )

                st.rerun()


# ============================================================
# ANALYTICS
# ============================================================

elif page == "Analytics":

    page_header(
        "Analytics",
        "Spending Analytics",
        "Understand your spending patterns with interactive analysis.",
    )

    if df.empty:

        st.info(
            "Add expenses to unlock your financial analytics."
        )

    else:

        average = get_average_spending(df)

        transactions = get_transaction_count(df)

        highest = get_highest_category(df)

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-label">AVERAGE EXPENSE</div>
                    <div class="kpi-value">{money(average)}</div>
                    <div class="kpi-description">
                        Average transaction amount
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with c2:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-label">TRANSACTIONS</div>
                    <div class="kpi-value">{transactions}</div>
                    <div class="kpi-description">
                        Total recorded transactions
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with c3:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-label">TOP CATEGORY</div>
                    <div class="kpi-value">{highest}</div>
                    <div class="kpi-description">
                        Highest spending category
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.markdown("###")

        # ----------------------------------------------------
        # CATEGORY
        # ----------------------------------------------------

        st.markdown(
            """
            <div class="card-title">
                Category Spending
            </div>
            <div class="card-description">
                Compare total spending across categories.
            </div>
            """,
            unsafe_allow_html=True,
        )

        category_data = get_category_summary(df)

        fig = px.bar(
            category_data,
            x="category",
            y="amount",
            labels={
                "category": "Category",
                "amount": "Spending (₹)",
            },
            text_auto=".0f",
        )

        fig.update_traces(
            marker_color=ACCENT,
            textposition="outside",
        )

        fig = style_plot(fig, 360)

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displayModeBar": False,
            },
        )

        # ----------------------------------------------------
        # MONTHLY + PAYMENT
        # ----------------------------------------------------

        col1, col2 = st.columns(2, gap="large")

        with col1:

            st.markdown(
                """
                <div class="card-title">
                    Monthly Spending Trend
                </div>
                <div class="card-description">
                    Track how spending changes month by month.
                </div>
                """,
                unsafe_allow_html=True,
            )

            monthly_data = get_monthly_summary(df)

            fig = px.line(
                monthly_data,
                x="date",
                y="amount",
                markers=True,
                labels={
                    "date": "",
                    "amount": "Spending (₹)",
                },
            )

            fig.update_traces(
                line=dict(
                    color=ACCENT,
                    width=2,
                ),
                marker=dict(
                    size=7,
                ),
            )

            fig = style_plot(fig, 330)

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={
                    "displayModeBar": False,
                },
            )

        with col2:

            st.markdown(
                """
                <div class="card-title">
                    Payment Methods
                </div>
                <div class="card-description">
                    Distribution of spending by payment method.
                </div>
                """,
                unsafe_allow_html=True,
            )

            payment_data = get_payment_summary(df)

            fig = px.pie(
                payment_data,
                names="payment_method",
                values="amount",
                hole=0.58,
            )

            fig.update_traces(
                textinfo="percent",
                marker=dict(
                    line=dict(
                        color=BG,
                        width=2,
                    )
                ),
            )

            fig = style_plot(fig, 330)

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={
                    "displayModeBar": False,
                },
            )

        # ----------------------------------------------------
        # DAILY TREND
        # ----------------------------------------------------

        st.markdown("###")

        st.markdown(
            """
            <div class="card-title">
                Daily Spending
            </div>
            <div class="card-description">
                Detailed view of spending activity by day.
            </div>
            """,
            unsafe_allow_html=True,
        )

        daily_data = (
            df.groupby("date")["amount"]
            .sum()
            .reset_index()
        )

        fig = px.area(
            daily_data,
            x="date",
            y="amount",
            labels={
                "date": "Date",
                "amount": "Spending (₹)",
            },
        )

        fig.update_traces(
            line=dict(
                color=ACCENT,
                width=2,
            ),
            fillcolor="rgba(79,142,247,0.12)",
        )

        fig = style_plot(fig, 340)

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={
                "displayModeBar": False,
            },
        )


# ============================================================
# REPORTS
# ============================================================

elif page == "Reports":

    page_header(
        "Reports",
        "Financial Reports",
        "Export your transaction data and financial summary.",
    )

    if df.empty:

        st.info(
            "Add expenses before generating a report."
        )

    else:

        total = get_total_spending(df)

        average = get_average_spending(df)

        col1, col2 = st.columns(2, gap="large")

        with col1:

            st.markdown(
                """
                <div class="card">

                    <div style="
                        font-size:30px;
                        margin-bottom:12px;
                    ">
                        CSV
                    </div>

                    <div class="card-title">
                        Expense Data Export
                    </div>

                    <div class="card-description">
                        Download your complete transaction history
                        as a CSV file for further analysis.
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

            csv_data = generate_csv_report(df)

            st.download_button(
                "Download CSV",
                data=csv_data,
                file_name="spendwise_expenses.csv",
                mime="text/csv",
                use_container_width=True,
            )

        with col2:

            st.markdown(
                """
                <div class="card">

                    <div style="
                        font-size:30px;
                        margin-bottom:12px;
                    ">
                        PDF
                    </div>

                    <div class="card-title">
                        Financial Summary
                    </div>

                    <div class="card-description">
                        Generate a formatted PDF containing
                        your key financial metrics.
                    </div>

                </div>
                """,
                unsafe_allow_html=True,
            )

            pdf_data = generate_pdf_report(
                df,
                total,
                average,
            )

            st.download_button(
                "Download PDF",
                data=pdf_data,
                file_name="spendwise_report.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

        st.markdown("###")

        # Report preview

        st.markdown(
            """
            <div class="card-title">
                Report Summary
            </div>
            <div class="card-description">
                Current dataset overview.
            </div>
            """,
            unsafe_allow_html=True,
        )

        r1, r2, r3 = st.columns(3)

        with r1:
            st.metric(
                "Total Spending",
                money(total),
            )

        with r2:
            st.metric(
                "Average Expense",
                money(average),
            )

        with r3:
            st.metric(
                "Transactions",
                len(df),
            )