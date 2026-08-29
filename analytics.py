import pandas as pd


def get_total_spending(df):
    return df["amount"].sum()


def get_average_spending(df):
    if df.empty:
        return 0

    return df["amount"].mean()


def get_transaction_count(df):
    return len(df)


def get_category_summary(df):
    return (
        df.groupby("category")["amount"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )


def get_payment_summary(df):
    return (
        df.groupby("payment_method")["amount"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )


def get_monthly_summary(df):
    df = df.copy()

    df["date"] = pd.to_datetime(df["date"])

    monthly = (
        df.groupby(df["date"].dt.to_period("M"))["amount"]
        .sum()
        .reset_index()
    )

    monthly["date"] = monthly["date"].astype(str)

    return monthly


def get_daily_summary(df):
    df = df.copy()

    df["date"] = pd.to_datetime(df["date"])

    return (
        df.groupby("date")["amount"]
        .sum()
        .reset_index()
    )


def get_highest_category(df):
    if df.empty:
        return "No Data"

    category_summary = get_category_summary(df)

    return category_summary.iloc[0]["category"]