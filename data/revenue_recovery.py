import pandas as pd


def calculate_recovery_priority(df):
    """
    Calculate a recovery priority score for overdue invoices.
    """

    df = df.copy()

    # Only overdue invoices are candidates for recovery
    df["is_overdue"] = df["payment_status"].str.lower() == "overdue"

    # Start score at zero
    df["recovery_score"] = 0

    # Higher invoice value = higher recovery priority
    df.loc[df["invoice_amount"] >= 30000, "recovery_score"] += 40
    df.loc[
        (df["invoice_amount"] >= 15000)
        & (df["invoice_amount"] < 30000),
        "recovery_score"
    ] += 25
    df.loc[df["invoice_amount"] < 15000, "recovery_score"] += 10

    # More overdue days = higher priority
    df.loc[df["days_overdue"] >= 60, "recovery_score"] += 40
    df.loc[
        (df["days_overdue"] >= 30)
        & (df["days_overdue"] < 60),
        "recovery_score"
    ] += 25
    df.loc[
        (df["days_overdue"] > 0)
        & (df["days_overdue"] < 30),
        "recovery_score"
    ] += 10

    # Paid invoices should not receive recovery priority
    df.loc[~df["is_overdue"], "recovery_score"] = 0

    # Assign priority category
    def assign_priority(score):
        if score >= 70:
            return "High"
        elif score >= 40:
            return "Medium"
        elif score > 0:
            return "Low"
        return "None"

    df["priority"] = df["recovery_score"].apply(assign_priority)

    return df


def calculate_recovery_metrics(df):
    """
    Calculate overall revenue recovery metrics.
    """

    overdue = df[df["is_overdue"]]

    total_overdue = overdue["invoice_amount"].sum()

    high_priority = overdue[
        overdue["priority"] == "High"
    ]

    high_priority_revenue = high_priority["invoice_amount"].sum()

    # Assumption for initial model:
    # 40% of high-priority overdue revenue is potentially recoverable.
    estimated_recovery = high_priority_revenue * 0.40

    return {
        "total_overdue_revenue": total_overdue,
        "high_priority_revenue": high_priority_revenue,
        "estimated_recovery": estimated_recovery,
    }
