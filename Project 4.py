from pathlib import Path
import pandas as pd

# Locate the downloaded dataset
data_folder = Path.home() / "Desktop" / "Help Desk Tickets"

print("DATA FOLDER EXISTS:", data_folder.exists())

# Locate the main issues CSV
csv_files = list(data_folder.glob("issues*"))

print("\nMATCHING FILES:")
for file in csv_files:
    print(file.name)

# Load the main dataset
issues_file = next(
    file for file in csv_files
    if file.stem == "issues"
)

df = pd.read_csv(issues_file)

print("\nDATASET INFORMATION")
df.info()

print("\nMISSING VALUES BY COLUMN")
print(df.isnull().sum())

print("\nTOTAL MISSING VALUES")
print(df.isnull().sum().sum())

print("\nDUPLICATE ROW COUNT")
print(df.duplicated().sum())

print("\nDUPLICATE TICKET ID COUNT")
print(df["id"].duplicated().sum())

print("\nUNIQUE TICKET ID COUNT")
print(df["id"].nunique())

print("\nCOLUMNS WITH MISSING VALUES")

missing_counts = df.isnull().sum()

print(
    missing_counts[missing_counts > 0]
    .sort_values(ascending=False)
)

print("\nUNIQUE TICKET ID COUNT")
print(df["id"].nunique())

print("\nMISSING TICKET ID COUNT")
print(df["id"].isnull().sum())

print("\nDATASET MEMORY USAGE")
print(df.memory_usage(deep=True).sum() / (1024 ** 2), "MB")

# Load supporting datasets

history_file = data_folder / "issues_change_history.csv"
snapshot_file = data_folder / "issues_snapshot.csv"

history_df = pd.read_csv(history_file)
snapshot_df = pd.read_csv(snapshot_file)

print("\nCHANGE HISTORY DATASET")
print("Shape:", history_df.shape)
print("Columns:", history_df.columns.tolist())

print("\nSNAPSHOT DATASET")
print("Shape:", snapshot_df.shape)
print("Columns:", snapshot_df.columns.tolist())

print("\nFIRST FIVE CHANGE HISTORY RECORDS")
print(history_df.head())

print("\nFIRST FIVE SNAPSHOT RECORDS")
print(snapshot_df.head())

# CHANGE HISTORY DATA QUALITY AUDIT

print("\nCHANGE HISTORY AUDIT")

print("Total records:", len(history_df))

print("Missing issue IDs:", history_df["issueid"].isnull().sum())

print("Unique issue IDs:", history_df["issueid"].nunique())

print("Duplicate change record IDs:", history_df["id"].duplicated().sum())

print("Missing change record IDs:", history_df["id"].isnull().sum())

print("Exact duplicate rows:", history_df.duplicated().sum())


# SNAPSHOT DATA QUALITY AUDIT

print("\nSNAPSHOT AUDIT")

print("Total records:", len(snapshot_df))

print("Missing issue IDs:", snapshot_df["id"].isnull().sum())

print("Unique issue IDs:", snapshot_df["id"].nunique())

print("Duplicate snapshot indexes:", snapshot_df["idx"].duplicated().sum())

print("Missing snapshot indexes:", snapshot_df["idx"].isnull().sum())

print("Exact duplicate rows:", snapshot_df.duplicated().sum())


# CHECK ISSUE ID COVERAGE

print("\nISSUE ID COVERAGE")

main_ids = set(df["id"].dropna())

history_ids = set(history_df["issueid"].dropna())

snapshot_ids = set(snapshot_df["id"].dropna())

print("Main issues:", len(main_ids))

print("History issue IDs matching main:", len(history_ids & main_ids))

print("Snapshot issue IDs matching main:", len(snapshot_ids & main_ids))

print("History issue IDs not in main:", len(history_ids - main_ids))

print("Snapshot issue IDs not in main:", len(snapshot_ids - main_ids))

# Records per issue in change history

history_records = history_df.groupby("issueid").size()

print("\nCHANGE HISTORY RECORDS PER ISSUE")
print(history_records.describe())

print("\nNUMBER OF ISSUES BY CHANGE RECORD COUNT")
print(history_records.value_counts().sort_index().head(15))


# Records per issue in snapshot

snapshot_records = snapshot_df.groupby("id").size()

print("\nSNAPSHOT RECORDS PER ISSUE")
print(snapshot_records.describe())

print("\nNUMBER OF ISSUES BY SNAPSHOT RECORD COUNT")
print(snapshot_records.value_counts().sort_index().head(15))


# Issues with multiple snapshot records

print("\nISSUES WITH MULTIPLE SNAPSHOT RECORDS")
print((snapshot_records > 1).sum())

print("\nMAXIMUM SNAPSHOT RECORDS FOR ONE ISSUE")
print(snapshot_records.max())

# Assignment analysis

print("\nSNAPSHOT ASSIGNEE INFORMATION")

print("Missing assignees:")
print(snapshot_df["issue_assignee"].isnull().sum())

print("\nUnique assignees:")
print(snapshot_df["issue_assignee"].nunique())

print("\nTop 10 assignees by snapshot record count:")
print(snapshot_df["issue_assignee"].value_counts().head(10))


# Distinct assignees per issue

assignees_per_issue = (
    snapshot_df.groupby("id")["issue_assignee"]
    .nunique()
)

print("\nDISTINCT ASSIGNEES PER ISSUE")
print(assignees_per_issue.describe())

print("\nISSUES WITH MULTIPLE DISTINCT ASSIGNEES")
print((assignees_per_issue > 1).sum())

print("\nISSUES WITH NO RECORDED ASSIGNEE")
print((assignees_per_issue == 0).sum())

# TASK 11: TICKET STATUS ANALYSIS

print("\nTICKET STATUS DISTRIBUTION")

status_counts = df["issue_status"].value_counts()

print(status_counts)

print("\nTICKET STATUS PERCENTAGES")

status_percentages = (
    df["issue_status"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

print(status_percentages)

print("\nUNIQUE TICKET STATUSES")

print(df["issue_status"].unique())

# TASK 12: STATUS AND RESOLUTION DATA AUDIT

print("\nRESOLUTION DATE AUDIT")

print("Missing resolution dates:")
print(df["issue_resolution_date"].isnull().sum())

print("\nMissing resolution descriptions:")
print(df["issue_resolution"].isnull().sum())


print("\nSTATUS VS RESOLUTION DATE")

resolution_date_status = pd.crosstab(
    df["issue_status"],
    df["issue_resolution_date"].isnull(),
    margins=True
)

print(resolution_date_status)


print("\nSTATUS VS RESOLUTION DESCRIPTION")

resolution_status = pd.crosstab(
    df["issue_status"],
    df["issue_resolution"].isnull(),
    margins=True
)

print(resolution_status)

# TASK 13: ISSUE TYPE ANALYSIS

print("\nISSUE TYPE DISTRIBUTION")

issue_type_counts = df["issue_type"].value_counts()

print(issue_type_counts)


print("\nISSUE TYPE PERCENTAGES")

issue_type_percentages = (
    df["issue_type"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

print(issue_type_percentages)


print("\nUNIQUE ISSUE TYPES")

print(df["issue_type"].unique())
# TASK 14: ISSUE PRIORITY ANALYSIS

print("\nISSUE PRIORITY DISTRIBUTION")

priority_counts = df["issue_priority"].value_counts()

print(priority_counts)


print("\nISSUE PRIORITY PERCENTAGES")

priority_percentages = (
    df["issue_priority"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

print(priority_percentages)


print("\nUNIQUE PRIORITY VALUES")

print(df["issue_priority"].unique())

# TASK 15: PRIORITY VS STATUS ANALYSIS

print("\nPRIORITY VS TICKET STATUS")

priority_status = pd.crosstab(
    df["issue_priority"],
    df["issue_status"],
    margins=True
)

print(priority_status)


print("\nHIGH PRIORITY TICKETS BY STATUS")

high_priority_tickets = df[
    df["issue_priority"].isin(["High", "Highest", "Blocker"])
]

print(
    high_priority_tickets["issue_status"]
    .value_counts()
)


print("\nHIGH PRIORITY TICKET COUNT")

print(len(high_priority_tickets))

# TASK 16: PRIORITY-WISE STATUS PERCENTAGES

print("\nPRIORITY-WISE STATUS PERCENTAGES")

priority_status_percentage = pd.crosstab(
    df["issue_priority"],
    df["issue_status"],
    normalize="index"
) * 100

print(priority_status_percentage.round(2))

# DISPLAY COMPLETE PRIORITY-STATUS TABLE

print("\nCOMPLETE PRIORITY-WISE STATUS PERCENTAGES")

print(
    priority_status_percentage
    .round(2)
    .to_string()
)
# TASK 17: AVERAGE PROCESSING TIME BY PRIORITY

print("\nAVERAGE PROCESSING TIME BY PRIORITY")

priority_processing_time = (
    df.groupby("issue_priority")["wf_total_time"]
    .agg(["count", "mean", "median"])
    .sort_values("mean", ascending=False)
)

print(priority_processing_time.round(2))
# TASK 18: PROCESSING TIME IN DAYS

print("\nPROCESSING TIME BY PRIORITY - DAYS")

priority_processing_days = (
    df.groupby("issue_priority")["wf_total_time"]
    .agg(["count", "mean", "median"])
)

priority_processing_days["mean_days"] = (
    priority_processing_days["mean"] / 86400
)

priority_processing_days["median_days"] = (
    priority_processing_days["median"] / 86400
)

print(
    priority_processing_days[
        ["count", "mean_days", "median_days"]
    ].round(2)
)

# TASK 19: PROCESSING TIME DISTRIBUTION AUDIT

print("\nPROCESSING TIME DISTRIBUTION AUDIT")

print(
    df["wf_total_time"].describe(
        percentiles=[0.25, 0.50, 0.75, 0.90, 0.95, 0.99]
    ).round(2)
)

# TASK 20: INSPECT EXTREME PROCESSING-TIME RECORDS

print("\nTOP 10 RECORDS BY PROCESSING TIME")

top_processing_records = (
    df.nlargest(10, "wf_total_time")[
        [
            "id",
            "issue_type",
            "issue_priority",
            "issue_status",
            "issue_created",
            "issue_resolution_date",
            "wf_total_time"
        ]
    ].copy()
)

top_processing_records["processing_days"] = (
    top_processing_records["wf_total_time"] / 86400
)

print(top_processing_records.to_string(index=False))

# TASK 21: COMPARE PROCESSING TIME WITH DATE DIFFERENCE

print("\nPROCESSING TIME VS DATE DIFFERENCE")

comparison_df = df[
    [
        "id",
        "issue_created",
        "issue_resolution_date",
        "wf_total_time"
    ]
].copy()

# Convert date columns into datetime format
comparison_df["issue_created"] = pd.to_datetime(
    comparison_df["issue_created"],
    format="mixed",
    utc=True
)

comparison_df["issue_resolution_date"] = pd.to_datetime(
    comparison_df["issue_resolution_date"],
    format="mixed",
    utc=True
)
# Calculate date difference in days
comparison_df["date_difference_days"] = (
    comparison_df["issue_resolution_date"]
    - comparison_df["issue_created"]
).dt.total_seconds() / 86400

# Convert processing time into days
comparison_df["processing_days"] = (
    comparison_df["wf_total_time"] / 86400
)

# Display the 10 largest processing-time records
comparison_df = comparison_df.nlargest(
    10, "wf_total_time"
)

print(
    comparison_df[
        [
            "id",
            "date_difference_days",
            "processing_days"
        ]
    ].round(2).to_string(index=False)
)

# TASK 22: VALIDATE PROCESSING TIME ACROSS ALL RECORDS

print("\nFULL DATASET PROCESSING TIME VALIDATION")

# Keep records with both dates available
valid_dates = df[
    [
        "id",
        "issue_type",
        "issue_priority",
        "issue_status",
        "issue_created",
        "issue_resolution_date",
        "wf_total_time"
    ]
].dropna(
    subset=["issue_created", "issue_resolution_date"]
).copy()

# Convert dates
valid_dates["issue_created"] = pd.to_datetime(
    valid_dates["issue_created"],
    format="mixed",
    utc=True
)

valid_dates["issue_resolution_date"] = pd.to_datetime(
    valid_dates["issue_resolution_date"],
    format="mixed",
    utc=True
)

# Calculate elapsed time in days
valid_dates["date_difference_days"] = (
    valid_dates["issue_resolution_date"]
    - valid_dates["issue_created"]
).dt.total_seconds() / 86400

valid_dates["processing_days"] = (
    valid_dates["wf_total_time"] / 86400
)

# Calculate absolute difference
valid_dates["absolute_difference"] = (
    valid_dates["date_difference_days"]
    - valid_dates["processing_days"]
).abs()

print("\nCOMPARISON SUMMARY")

print(
    valid_dates["absolute_difference"].describe().round(6)
)

print(
    "\nRecords with negative date differences:",
    (valid_dates["date_difference_days"] < 0).sum()
)

print(
    "Records with processing time different from date difference:",
    (valid_dates["absolute_difference"] > 0.000001).sum()
)

print(
    "Total records compared:",
    len(valid_dates)
)

# TASK 23: INVESTIGATE PROCESSING-TIME MISMATCHES

print("\nTOP 15 PROCESSING-TIME MISMATCHES")

mismatch_records = valid_dates[
    valid_dates["absolute_difference"] > 0.000001
].copy()

top_mismatches = mismatch_records.nlargest(
    15, "absolute_difference"
)

print(
    top_mismatches[
        [
            "id",
            "issue_type",
            "issue_priority",
            "issue_status",
            "issue_created",
            "issue_resolution_date",
            "date_difference_days",
            "processing_days",
            "absolute_difference"
        ]
    ].round(2).to_string(index=False)
)

# TASK 24: INVESTIGATE STARTED AND ENDED TIMESTAMPS

print("\nSTARTED AND ENDED TIMESTAMP INVESTIGATION")

investigation_records = df.loc[
    df["id"].isin(top_mismatches["id"]),
    [
        "id",
        "started",
        "ended",
        "issue_created",
        "issue_resolution_date",
        "wf_total_time",
        "processing_steps"
    ]
].copy()

investigation_records["processing_days"] = (
    investigation_records["wf_total_time"] / 86400
)

print(
    investigation_records[
        [
            "id",
            "started",
            "ended",
            "issue_created",
            "issue_resolution_date",
            "processing_days",
            "processing_steps"
        ]
    ].to_string(index=False)
)
# TASK 25: VALIDATE PROCESSING TIME USING STARTED AND ENDED

print("\nFULL DATASET PROCESSING TIME VALIDATION")

# Create a separate analysis DataFrame
time_validation = df[
    ["id", "started", "ended", "wf_total_time"]
].copy()

# Convert timestamps
time_validation["started"] = pd.to_datetime(
    time_validation["started"],
    format="mixed",
    utc=True
)

time_validation["ended"] = pd.to_datetime(
    time_validation["ended"],
    format="mixed",
    utc=True
)

# Calculate elapsed time in days
time_validation["elapsed_days"] = (
    time_validation["ended"] - time_validation["started"]
).dt.total_seconds() / 86400

# Convert recorded processing time into days
time_validation["processing_days"] = (
    time_validation["wf_total_time"] / 86400
)

# Calculate absolute difference
time_validation["absolute_difference"] = (
    time_validation["elapsed_days"]
    - time_validation["processing_days"]
).abs()

# Display validation results
print("\nABSOLUTE DIFFERENCE SUMMARY")

print(
    time_validation["absolute_difference"]
    .describe()
    .round(6)
)

print(
    "\nNegative elapsed-time records:",
    (time_validation["elapsed_days"] < 0).sum()
)

print(
    "Records with differences above tolerance:",
    (time_validation["absolute_difference"] > 0.000001).sum()
)

print(
    "Total records compared:",
    len(time_validation)
)
# TASK 26: INVESTIGATE REMAINING TIME MISMATCHES

print("\nTOP 15 STARTED-ENDED TIME MISMATCHES")

time_mismatches = time_validation[
    time_validation["absolute_difference"] > 0.000001
].copy()

top_time_mismatches = time_mismatches.nlargest(
    15, "absolute_difference"
)

print(
    top_time_mismatches[
        [
            "id",
            "started",
            "ended",
            "wf_total_time",
            "elapsed_days",
            "processing_days",
            "absolute_difference"
        ]
    ].to_string(index=False)
)

print("\nTOTAL MISMATCHED RECORDS:", len(time_mismatches))

# TASK 27: MISMATCH DISTRIBUTION BY ISSUE TYPE AND PRIORITY

print("\nMISMATCH DISTRIBUTION BY ISSUE TYPE")

mismatch_details = df.loc[
    df["id"].isin(time_mismatches["id"]),
    ["id", "issue_type", "issue_priority", "issue_status"]
].copy()

print(
    mismatch_details["issue_type"]
    .value_counts()
)

print("\nMISMATCH DISTRIBUTION BY PRIORITY")

print(
    mismatch_details["issue_priority"]
    .value_counts()
)

print("\nMISMATCH DISTRIBUTION BY STATUS")

print(
    mismatch_details["issue_status"]
    .value_counts()
)

# TASK 28: MISMATCH RATE BY ISSUE TYPE

# Total records by issue type
total_by_type = df["issue_type"].value_counts()

# Mismatched records by issue type
mismatches_by_type = mismatch_details["issue_type"].value_counts()

# Combine both counts
type_mismatch_analysis = pd.DataFrame({
    "total_records": total_by_type,
    "mismatched_records": mismatches_by_type
})

# Replace missing mismatch counts with zero
type_mismatch_analysis["mismatched_records"] = (
    type_mismatch_analysis["mismatched_records"].fillna(0)
)

# Calculate matching records
type_mismatch_analysis["matching_records"] = (
    type_mismatch_analysis["total_records"]
    - type_mismatch_analysis["mismatched_records"]
)

# Calculate mismatch percentage
type_mismatch_analysis["mismatch_percentage"] = (
    type_mismatch_analysis["mismatched_records"]
    / type_mismatch_analysis["total_records"]
) * 100

# Sort by mismatch percentage
type_mismatch_analysis = type_mismatch_analysis.sort_values(
    "mismatch_percentage",
    ascending=False
)

print("\nMISMATCH RATE BY ISSUE TYPE")

print(type_mismatch_analysis.round(2).to_string())

# TASK 29: INVESTIGATE TASK RECORD MISMATCHES

# Select all Task records
task_records = df[
    df["issue_type"] == "Task"
].copy()

# Select Task records with mismatched processing time
task_mismatches = task_records[
    task_records["id"].isin(time_mismatches["id"])
].copy()

# Compare status distribution
print("\nTASK RECORDS BY STATUS")

print(task_records["issue_status"].value_counts())

print("\nMISMATCHED TASK RECORDS BY STATUS")

print(task_mismatches["issue_status"].value_counts())

# Compare processing steps
print("\nPROCESSING STEPS - ALL TASK RECORDS")

print(task_records["processing_steps"].describe())

print("\nPROCESSING STEPS - MISMATCHED TASK RECORDS")

print(task_mismatches["processing_steps"].describe())
# TASK 30: WORKFLOW-STAGE INVESTIGATION

workflow_columns = [
    "wf_open",
    "wf_in_progress",
    "wf_done",
    "wf_closed",
    "wf_resolved",
    "wf_waiting",
    "wfe_open",
    "wfe_in_progress",
    "wfe_done",
    "wfe_closed",
    "wfe_resolved",
    "wfe_waiting"
]

print("\nWORKFLOW INFORMATION - MISMATCHED TASKS")

print(
    task_mismatches[workflow_columns]
    .describe()
    .round(2)
    .to_string()
)

print("\nWORKFLOW INFORMATION - MATCHING TASKS")

matching_task_records = task_records[
    ~task_records["id"].isin(time_mismatches["id"])
]

print(
    matching_task_records[workflow_columns]
    .describe()
    .round(2)
    .to_string()
)
# TASK 31: RECORD-LEVEL INVESTIGATION

task_mismatch_sample = task_mismatches[
    [
        "id",
        "started",
        "ended",
        "issue_created",
        "issue_resolution_date",
        "issue_status",
        "wf_total_time",
        "processing_steps",
        "wf_open",
        "wf_in_progress",
        "wf_done",
        "wfe_open",
        "wfe_in_progress",
        "wfe_done"
    ]
].head(5)

print("\nFIVE MISMATCHED TASK RECORDS")

print(task_mismatch_sample.to_string(index=False))

# TASK 32: VALIDATE WORKFLOW TIME TOTALS

task_workflow_columns = [
    "wf_in_review",
    "wf_deployment",
    "wf_resolved",
    "wf_open",
    "wf_monitoring",
    "wf_done",
    "wf_pending_customer_approval",
    "wf_rejected",
    "wf_testing_monitoring",
    "wf_in_progress",
    "wf_reopened",
    "wf_to_do",
    "wf_validation",
    "wf_resolved_under_monitoring",
    "wf_closed",
    "wf_waiting",
    "wf_cancelled",
    "wf_under_review",
    "wf_approved",
    "wf_pending_deployment"
]

task_workflow_totals = task_mismatches[
    task_workflow_columns
].sum(axis=1, min_count=1)

task_workflow_comparison = pd.DataFrame({
    "id": task_mismatches["id"],
    "wf_total_time": task_mismatches["wf_total_time"],
    "workflow_time_sum": task_workflow_totals
})

task_workflow_comparison["difference"] = (
    task_workflow_comparison["wf_total_time"]
    - task_workflow_comparison["workflow_time_sum"]
)

print("\nWORKFLOW TIME VALIDATION")

print(
    task_workflow_comparison[
        ["wf_total_time", "workflow_time_sum", "difference"]
    ].describe().round(2)
)

print("\nMATCHING WORKFLOW TOTALS")

print(
    (task_workflow_comparison["difference"].abs() <= 0.01)
    .value_counts()
)

print("\nTOP 10 DIFFERENCES")

print(
    task_workflow_comparison.assign(
        absolute_difference=task_workflow_comparison["difference"].abs()
    )
    .nlargest(10, "absolute_difference")
    .to_string(index=False)
)

# TASK 33: VALIDATE WORKFLOW TIME FOR ALL 374 MISMATCHES

# TASK 33: VALIDATE WORKFLOW TIME FOR ALL 374 MISMATCHES

# Retrieve original records from the main dataset
all_mismatch_records = df[
    df["id"].isin(time_mismatches["id"])
].copy()

print("\nNUMBER OF MISMATCHED RECORDS:")
print(len(all_mismatch_records))

# Calculate workflow-stage time totals
all_workflow_totals = all_mismatch_records[
    task_workflow_columns
].sum(axis=1, min_count=1)

# Compare the two time measures
all_workflow_comparison = pd.DataFrame({
    "id": all_mismatch_records["id"],
    "wf_total_time": all_mismatch_records["wf_total_time"],
    "workflow_time_sum": all_workflow_totals
})

all_workflow_comparison["difference"] = (
    all_workflow_comparison["wf_total_time"]
    - all_workflow_comparison["workflow_time_sum"]
)

print("\nWORKFLOW TIME VALIDATION:")
print(
    all_workflow_comparison[
        ["wf_total_time", "workflow_time_sum", "difference"]
    ].describe().round(4)
)

print("\nWORKFLOW TOTAL MATCHING:")
print(
    (all_workflow_comparison["difference"].abs() <= 0.01)
    .value_counts()
)

print("\nRECORDS WITHOUT WORKFLOW TIME:")
print(all_workflow_comparison["workflow_time_sum"].isna().sum())

print("\nTOP 10 DIFFERENCES:")
print(
    all_workflow_comparison.assign(
        absolute_difference=all_workflow_comparison["difference"].abs()
    )
    .nlargest(10, "absolute_difference")
    .to_string(index=False)
)

# TASK 33: FULL DATASET WORKFLOW TIME VALIDATION

all_workflow_totals = df[
    task_workflow_columns
].sum(axis=1, min_count=1)

full_workflow_comparison = pd.DataFrame({
    "id": df["id"],
    "wf_total_time": df["wf_total_time"],
    "workflow_time_sum": all_workflow_totals
})

full_workflow_comparison["difference"] = (
    full_workflow_comparison["wf_total_time"]
    - full_workflow_comparison["workflow_time_sum"]
)

# Compare within a tolerance of 0.01 seconds
full_workflow_comparison["matches"] = (
    full_workflow_comparison["difference"].abs() <= 0.01
)

print("\nFULL DATASET WORKFLOW VALIDATION")

print("\nMATCHING VS NON-MATCHING RECORDS:")
print(full_workflow_comparison["matches"].value_counts())

print("\nRECORDS WITHOUT WORKFLOW-STAGE TIME:")
print(full_workflow_comparison["workflow_time_sum"].isna().sum())

print("\nNON-MATCHING RECORDS:")
print(
    full_workflow_comparison[
        ~full_workflow_comparison["matches"]
    ].head(10).to_string(index=False)
)
# TASK 34: INVESTIGATE RECORDS WITHOUT WORKFLOW-STAGE TIME

no_workflow_records = full_workflow_comparison[
    full_workflow_comparison["workflow_time_sum"].isna()
].copy()

# Retrieve the corresponding records from the main dataset
no_workflow_details = df[
    df["id"].isin(no_workflow_records["id"])
].copy()

print("\nRECORD COUNT:")
print(len(no_workflow_details))

print("\nTOTAL WORKFLOW TIME DISTRIBUTION:")
print(no_workflow_details["wf_total_time"].value_counts(dropna=False))

print("\nISSUE STATUS DISTRIBUTION:")
print(no_workflow_details["issue_status"].value_counts())

print("\nISSUE TYPE DISTRIBUTION:")
print(no_workflow_details["issue_type"].value_counts())

print("\nPROCESSING STEPS:")
print(no_workflow_details["processing_steps"].value_counts().sort_index())

print("\nSAMPLE OF 10 RECORDS:")
print(
    no_workflow_details[
        [
            "id",
            "issue_type",
            "issue_priority",
            "issue_status",
            "started",
            "ended",
            "wf_total_time",
            "processing_steps"
        ]
    ].head(10).to_string(index=False)
)

# TASK 35: INVESTIGATE THE CLOSED RECORD WITH ZERO WORKFLOW TIME

closed_zero_record = df[df["id"] == 33245000].copy()

print("\nRECORD DETAILS")
print(
    closed_zero_record[
        [
            "id",
            "issue_type",
            "issue_priority",
            "issue_status",
            "issue_created",
            "issue_resolution_date",
            "issue_resolution",
            "started",
            "ended",
            "wf_total_time",
            "processing_steps"
        ]
    ].to_string(index=False)
)

print("\nWORKFLOW-STAGE DURATIONS")
print(
    closed_zero_record[
        [col for col in df.columns if col.startswith("wf_")]
    ].to_string(index=False)
)
# TASK 36: CHECK THE EXCEPTIONAL TICKET IN SNAPSHOT DATA

snapshot_record = snapshot_df[
    snapshot_df["id"] == 33245000
].copy()

print("\nSNAPSHOT RECORD COUNT:")
print(len(snapshot_record))

print("\nSNAPSHOT DETAILS:")
print(
    snapshot_record[
        [
            "idx",
            "id",
            "started",
            "ended",
            "issue_assignee",
            "issue_status",
            "issue_resolution_date",
            "wf_total_time",
            "processing_steps"
        ]
    ].to_string(index=False)
)

print("\nSNAPSHOT WORKFLOW DURATIONS:")
snapshot_workflow_columns = [
    col for col in snapshot_df.columns
    if col.startswith("wf_")
]

print(
    snapshot_record[snapshot_workflow_columns].to_string(index=False)
)

# TASK 37: CHECK CHANGE HISTORY FOR THE EXCEPTIONAL TICKET

ticket_history = history_df[
    history_df["issueid"] == 33245000
].copy()

print("\nCHANGE HISTORY RECORD COUNT:")
print(len(ticket_history))

print("\nCHANGE HISTORY DETAILS:")
print(
    ticket_history[
        ["id", "issueid", "field", "value", "created", "change_group_id"]
    ].sort_values("created").to_string(index=False)
)
# TASK 38: INVESTIGATE CLOSED RECORDS WITH ZERO WORKFLOW TIME

closed_zero_workflow = df[
    (df["issue_status"] == "closed") &
    (df["wf_total_time"] == 0)
].copy()

print("\nCLOSED RECORDS WITH ZERO WORKFLOW TIME:")
print(len(closed_zero_workflow))

print("\nISSUE TYPE DISTRIBUTION:")
print(closed_zero_workflow["issue_type"].value_counts())

print("\nRESOLUTION DATE AVAILABILITY:")
print(closed_zero_workflow["issue_resolution_date"].notna().value_counts())

print("\nRESOLUTION DESCRIPTION DISTRIBUTION:")
print(closed_zero_workflow["issue_resolution"].value_counts(dropna=False))

print("\nPROCESSING STEPS DISTRIBUTION:")
print(closed_zero_workflow["processing_steps"].value_counts())
# TASK 38: INVESTIGATE CLOSED RECORDS WITH ZERO WORKFLOW TIME

closed_zero_workflow = df[
    (df["issue_status"] == "closed") &
    (df["wf_total_time"] == 0)
].copy()

print("\nCLOSED RECORDS WITH ZERO WORKFLOW TIME:")
print(len(closed_zero_workflow))

print("\nISSUE TYPE DISTRIBUTION:")
print(closed_zero_workflow["issue_type"].value_counts())

print("\nRESOLUTION DATE AVAILABILITY:")
print(closed_zero_workflow["issue_resolution_date"].notna().value_counts())

print("\nRESOLUTION DESCRIPTION DISTRIBUTION:")
print(closed_zero_workflow["issue_resolution"].value_counts(dropna=False))

print("\nPROCESSING STEPS DISTRIBUTION:")
print(closed_zero_workflow["processing_steps"].value_counts())
# TASK 39: AUDIT OPEN RECORDS WITH ZERO WORKFLOW TIME

open_zero_workflow = df[
    (df["issue_status"] == "open") &
    (df["wf_total_time"] == 0)
].copy()

print("\nOPEN RECORDS WITH ZERO WORKFLOW TIME:")
print(len(open_zero_workflow))

print("\nISSUE TYPE DISTRIBUTION:")
print(open_zero_workflow["issue_type"].value_counts())

print("\nPROCESSING STEPS:")
print(open_zero_workflow["processing_steps"].value_counts())

print("\nRESOLUTION DATE AVAILABILITY:")
print(open_zero_workflow["issue_resolution_date"].notna().value_counts())

print("\nSTARTED AND ENDED TIMESTAMP COMPARISON:")
print(
    (
        open_zero_workflow["started"] ==
        open_zero_workflow["ended"]
    ).value_counts()
)

print("\nWORKFLOW DURATION AVAILABILITY:")
print(
    open_zero_workflow[
        [col for col in df.columns if col.startswith("wf_")]
    ].notna().sum()
)
# TASK 40: AUDIT PROJECT DISTRIBUTION

print("\nTOTAL UNIQUE PROJECTS:")
print(df["issue_proj"].nunique())

print("\nPROJECT DISTRIBUTION:")
print(df["issue_proj"].value_counts().to_string())

print("\nISSUE TYPES BY PROJECT:")
project_issue_types = pd.crosstab(
    df["issue_proj"],
    df["issue_type"]
)

print(project_issue_types.to_string())

print("\nNUMBER OF ISSUE TYPES PER PROJECT:")
print(
    project_issue_types.gt(0).sum(axis=1).sort_values(
        ascending=False
    ).to_string()
)
# TASK 41: PROJECT CONCENTRATION ANALYSIS

project_counts = df["issue_proj"].value_counts()

project_summary = pd.DataFrame({
    "issue_count": project_counts,
    "percentage": (
        project_counts / len(df) * 100
    )
})

project_summary["cumulative_percentage"] = (
    project_summary["percentage"].cumsum()
)

print("\nTOP 10 PROJECTS:")
print(project_summary.head(10).round(2).to_string())

print("\nTOP 5 PROJECTS - TOTAL RECORDS:")
print(project_summary.head(5)["issue_count"].sum())

print("\nTOP 10 PROJECTS - TOTAL RECORDS:")
print(project_summary.head(10)["issue_count"].sum())

print("\nTOP 10 PROJECTS - CUMULATIVE SHARE:")
print(
    round(
        project_summary.head(10)["percentage"].sum(),
        2
    ),
    "%"
)

print("\nPROJECT COUNT DISTRIBUTION:")
print(project_counts.describe().round(2))
# TASK 42: MONTHLY ISSUE VOLUME ANALYSIS

# Convert issue_created into datetime
df["issue_created"] = pd.to_datetime(
    df["issue_created"],
    format="mixed",
    utc=True
)

# Extract year and month
df["created_month"] = (
    df["issue_created"]
    .dt.to_period("M")
    .astype(str)
)

# Count issues created each month
monthly_issue_volume = (
    df.groupby("created_month")
    .size()
    .reset_index(name="issue_count")
)

# Sort chronologically
monthly_issue_volume = monthly_issue_volume.sort_values(
    "created_month"
)

print("\nMONTHLY ISSUE VOLUME:")
print(monthly_issue_volume.to_string(index=False))

print("\nMONTHLY ISSUE VOLUME SUMMARY:")
print(monthly_issue_volume["issue_count"].describe().round(2))

print("\nMONTH WITH HIGHEST ISSUE VOLUME:")
print(
    monthly_issue_volume.loc[
        monthly_issue_volume["issue_count"].idxmax()
    ]
)

print("\nMONTH WITH LOWEST ISSUE VOLUME:")
print(
    monthly_issue_volume.loc[
        monthly_issue_volume["issue_count"].idxmin()
    ]
)
# TASK 43: MONTHLY ISSUE VOLUME TREND

import matplotlib.pyplot as plt

plt.figure(figsize=(15, 6))

plt.plot(
    monthly_issue_volume["created_month"],
    monthly_issue_volume["issue_count"]
)

plt.title("Monthly Issue Volume Trend")
plt.xlabel("Month")
plt.ylabel("Number of Issues")

plt.xticks(
    range(0, len(monthly_issue_volume), 12),
    monthly_issue_volume["created_month"][::12],
    rotation=45
)

plt.grid(True)
plt.tight_layout()

plt.savefig("monthly_issue_volume_trend.png", dpi=300)

plt.show()

# TASK 44: ANNUAL ISSUE VOLUME ANALYSIS

# Extract year from issue creation date
df["created_year"] = df["issue_created"].dt.year

# Count issues created each year
annual_issue_volume = (
    df.groupby("created_year")
    .size()
    .reset_index(name="issue_count")
)

print("\nANNUAL ISSUE VOLUME:")
print(annual_issue_volume.to_string(index=False))

print("\nANNUAL ISSUE VOLUME SUMMARY:")
print(annual_issue_volume["issue_count"].describe().round(2))

print("\nYEAR WITH HIGHEST ISSUE VOLUME:")
print(
    annual_issue_volume.loc[
        annual_issue_volume["issue_count"].idxmax()
    ]
)

print("\nYEAR WITH LOWEST ISSUE VOLUME:")
print(
    annual_issue_volume.loc[
        annual_issue_volume["issue_count"].idxmin()
    ]
)

# TASK 45: ANNUAL ISSUE VOLUME CHART

plt.figure(figsize=(12, 6))

plt.bar(
    annual_issue_volume["created_year"].astype(str),
    annual_issue_volume["issue_count"]
)

plt.title("Annual Issue Volume Trend")
plt.xlabel("Year")
plt.ylabel("Number of Issues")
plt.xticks(rotation=45)
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig("annual_issue_volume_chart.png", dpi=300)
plt.show()

# TASK 46: MONTH-OF-YEAR PATTERN ANALYSIS

# Keep only complete calendar years
complete_years = df[
    df["created_year"].between(2008, 2022)
].copy()

# Extract calendar month
complete_years["month_number"] = (
    complete_years["issue_created"].dt.month
)

# Count issues for each year and month
year_month_counts = (
    complete_years.groupby(
        ["created_year", "month_number"]
    )
    .size()
    .unstack(fill_value=0)
)

# Ensure all 12 months are included
year_month_counts = year_month_counts.reindex(
    columns=range(1, 13),
    fill_value=0
)

# Calculate average issue volume for each calendar month
monthly_pattern = year_month_counts.mean(axis=0)

month_names = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December"
]

monthly_pattern.index = month_names

print("\nAVERAGE ISSUE VOLUME BY CALENDAR MONTH:")
print(monthly_pattern.round(2).to_string())

print("\nHIGHEST AVERAGE MONTH:")
print(monthly_pattern.idxmax(), round(monthly_pattern.max(), 2))

print("\nLOWEST AVERAGE MONTH:")
print(monthly_pattern.idxmin(), round(monthly_pattern.min(), 2))
# TASK 47: MONTH-OF-YEAR PATTERN CHART

import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))

monthly_pattern.plot(
    kind="bar",
    title="Average Issue Volume by Calendar Month (2008–2022)",
    xlabel="Calendar Month",
    ylabel="Average Number of Issues",
    rot=45
)

plt.tight_layout()
plt.savefig("average_monthly_issue_pattern.png", dpi=300)
plt.show()
# TASK 48: ANNUAL ISSUE VOLUME BY ISSUE TYPE

# Create a year-wise issue type summary
annual_issue_type = pd.crosstab(
    complete_years["created_year"],
    complete_years["issue_type"]
)

print("\nANNUAL ISSUE VOLUME BY ISSUE TYPE:")
print(annual_issue_type.to_string())

print("\nTOTAL RECORDS BY ISSUE TYPE (2008–2022):")
print(
    annual_issue_type.sum()
    .sort_values(ascending=False)
    .to_string()
)

print("\nTOTAL RECORDS BY YEAR (2008–2022):")
print(
    annual_issue_type.sum(axis=1)
    .to_string()
)# TASK 48: ANNUAL ISSUE VOLUME BY ISSUE TYPE

annual_issue_type = pd.crosstab(
    complete_years["created_year"],
    complete_years["issue_type"]
)

print("\nANNUAL ISSUE VOLUME BY ISSUE TYPE:")
print(annual_issue_type.to_string())

print("\nTOTAL RECORDS BY ISSUE TYPE (2008–2022):")
print(
    annual_issue_type.sum()
    .sort_values(ascending=False)
    .to_string()
)

print("\nTOTAL RECORDS BY YEAR (2008–2022):")
print(
    annual_issue_type.sum(axis=1)
    .to_string()
)
# TASK 49: ANNUAL ISSUE VOLUME BY ISSUE TYPE CHART

import matplotlib.pyplot as plt

annual_issue_type.plot(
    kind="bar",
    stacked=True,
    figsize=(14, 7),
    title="Annual Issue Volume by Issue Type (2008–2022)",
    xlabel="Year",
    ylabel="Number of Issues"
)

plt.xticks(rotation=45)
plt.legend(
    title="Issue Type",
    bbox_to_anchor=(1.02, 1),
    loc="upper left"
)

plt.tight_layout()
plt.savefig(
    "annual_issue_volume_by_issue_type.png",
    dpi=300,
    bbox_inches="tight"
)
plt.show()

# TASK 50: DOMINANT ISSUE TYPE BY YEAR

dominant_issue_type = annual_issue_type.idxmax(axis=1)

dominant_issue_count = annual_issue_type.max(axis=1)

dominant_issue_summary = pd.DataFrame({
    "dominant_issue_type": dominant_issue_type,
    "issue_count": dominant_issue_count
})

print("\nDOMINANT ISSUE TYPE BY YEAR:")
print(dominant_issue_summary.to_string())

# TASK 51: TICKET SHARE BY YEAR

ticket_share = (
    annual_issue_type["Ticket"]
    / annual_issue_type.sum(axis=1)
) * 100

ticket_share = ticket_share.round(2)

print("\nTICKET SHARE BY YEAR:")
print(ticket_share.to_string())

print("\nAVERAGE TICKET SHARE (2008–2022):")
print(round(ticket_share.mean(), 2), "%")

print("\nHIGHEST TICKET SHARE:")
print(ticket_share.idxmax(), ticket_share.max(), "%")

print("\nLOWEST TICKET SHARE:")
print(ticket_share.idxmin(), ticket_share.min(), "%")

# TASK 52: TICKET SHARE TREND

import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))

ticket_share.plot(
    kind="line",
    marker="o",
    linewidth=2,
    title="Ticket Share of Total Issues (2008–2022)",
    xlabel="Year",
    ylabel="Ticket Share (%)"
)

plt.ylim(0, 100)
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    "ticket_share_trend.png",
    dpi=300
)

plt.show()

# TASK 53: OVERALL TICKET SHARE

total_tickets = annual_issue_type["Ticket"].sum()

total_issues = annual_issue_type.sum().sum()

overall_ticket_share = (
    total_tickets / total_issues
) * 100

print("TOTAL TICKETS:", total_tickets)
print("TOTAL ISSUES:", total_issues)
print("OVERALL TICKET SHARE:", round(overall_ticket_share, 2), "%")

# TASK 54: OVERALL ISSUE-TYPE DISTRIBUTION

issue_type_distribution = pd.DataFrame({
    "issue_count": annual_issue_type.sum(),
    "percentage": (
        annual_issue_type.sum()
        / annual_issue_type.sum().sum()
    ) * 100
})

issue_type_distribution = (
    issue_type_distribution
    .sort_values("issue_count", ascending=False)
)

print("\nOVERALL ISSUE-TYPE DISTRIBUTION:")
print(issue_type_distribution.round(2).to_string())


# TASK 55: OVERALL ISSUE-TYPE DISTRIBUTION CHART

import matplotlib.pyplot as plt

# Sort issue types in ascending order for horizontal bars
plot_data = issue_type_distribution.sort_values(
    "issue_count",
    ascending=True
)

plt.figure(figsize=(13, 9))

# Create horizontal bar chart
plt.barh(
    plot_data.index,
    plot_data["issue_count"]
)

plt.title(
    "Overall Issue-Type Distribution (2008–2022)",
    fontsize=16
)

plt.xlabel("Number of Issues", fontsize=12)
plt.ylabel("Issue Type", fontsize=12)

plt.xticks(fontsize=10)
plt.yticks(fontsize=10)

plt.grid(axis="x", alpha=0.3)

plt.tight_layout()

plt.savefig(
    "overall_issue_type_distribution.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()


# TASK 56: TICKET PRIORITY DISTRIBUTION

ticket_data = complete_years[
    complete_years["issue_type"] == "Ticket"
].copy()

ticket_priority = (
    ticket_data["issue_priority"]
    .value_counts()
)

ticket_priority_percentage = (
    ticket_data["issue_priority"]
    .value_counts(normalize=True) * 100
)

ticket_priority_summary = pd.DataFrame({
    "ticket_count": ticket_priority,
    "percentage": ticket_priority_percentage
})

print("\nTICKET PRIORITY DISTRIBUTION:")
print(ticket_priority_summary.round(2).to_string())

print("\nTOTAL TICKET RECORDS:")
print(len(ticket_data))

# TASK 57: TICKET PRIORITY DISTRIBUTION CHART

import matplotlib.pyplot as plt

plt.figure(figsize=(11, 6))

ticket_priority_summary["ticket_count"].sort_values().plot(
    kind="barh",
    title="Ticket Distribution by Priority (2008–2022)",
    xlabel="Number of Tickets",
    ylabel="Priority"
)

plt.tight_layout()

plt.savefig(
    "ticket_priority_distribution.png",
    dpi=300,
    bbox_inches="tight"
)
plt.xlabel("Number of Tickets")
plt.grid(axis="x", alpha=0.3)
plt.show()


# TASK 58: TICKET STATUS BY PRIORITY

ticket_priority_status = pd.crosstab(
    ticket_data["issue_priority"],
    ticket_data["issue_status"]
)

print("\nTICKET STATUS BY PRIORITY:")
print(ticket_priority_status.to_string())

print("\nTOTAL TICKETS BY PRIORITY:")
print(ticket_priority_status.sum(axis=1).to_string())

print("\nTOTAL TICKETS BY STATUS:")
print(ticket_priority_status.sum(axis=0).to_string())

# TASK 59: STATUS PERCENTAGES BY PRIORITY

ticket_priority_status_pct = pd.crosstab(
    ticket_data["issue_priority"],
    ticket_data["issue_status"],
    normalize="index"
) * 100

print("\nTICKET STATUS PERCENTAGES BY PRIORITY:")
print(ticket_priority_status_pct.round(2).to_string())

# TASK 60: TICKET STATUS PERCENTAGES CHART

import matplotlib.pyplot as plt

ax = ticket_priority_status_pct.plot(
    kind="bar",
    stacked=True,
    figsize=(16, 8),
    title="Ticket Status Distribution by Priority (2008–2022)",
    xlabel="Ticket Priority",
    ylabel="Percentage of Tickets"
)

ax.set_xticklabels(
    ticket_priority_status_pct.index,
    rotation=0
)

plt.ylim(0, 100)

plt.legend(
    title="Ticket Status",
    bbox_to_anchor=(1.02, 1),
    loc="upper left",
    fontsize=9
)

plt.tight_layout(rect=[0, 0, 0.82, 1])

plt.savefig(
    "ticket_status_by_priority.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# TASK 61: TICKET RESOLUTION-DATE COMPLETENESS

ticket_resolution_audit = complete_years[
    complete_years["issue_type"] == "Ticket"
].copy()

total_tickets = len(ticket_resolution_audit)

missing_resolution_dates = (
    ticket_resolution_audit["issue_resolution_date"].isna().sum()
)

available_resolution_dates = (
    ticket_resolution_audit["issue_resolution_date"].notna().sum()
)

print("\nTICKET RESOLUTION-DATE AUDIT:")
print("Total Tickets:", total_tickets)
print("Available Resolution Dates:", available_resolution_dates)
print("Missing Resolution Dates:", missing_resolution_dates)

print(
    "Resolution Date Completeness:",
    round(available_resolution_dates / total_tickets * 100, 2),
    "%"
)

print(
    "Missing Resolution Date Percentage:",
    round(missing_resolution_dates / total_tickets * 100, 2),
    "%"
)

# TASK 62: RESOLUTION-DATE AVAILABILITY BY STATUS

resolution_status_audit = pd.crosstab(
    ticket_resolution_audit["issue_status"],
    ticket_resolution_audit["issue_resolution_date"].isna()
)

resolution_status_audit.columns = [
    "Available Resolution Date",
    "Missing Resolution Date"
]

print("\nRESOLUTION-DATE AVAILABILITY BY STATUS:")
print(resolution_status_audit.to_string())

print("\nTOTAL MISSING DATES BY STATUS:")
print(
    resolution_status_audit["Missing Resolution Date"]
    .sort_values(ascending=False)
    .to_string()
)

# TASK 63: RESOLUTION-DATE COMPLETENESS BY STATUS

resolution_status_percentage = pd.crosstab(
    ticket_resolution_audit["issue_status"],
    ticket_resolution_audit["issue_resolution_date"].notna(),
    normalize="index"
) * 100

resolution_status_percentage.columns = [
    "Missing Date %",
    "Available Date %"
]

print("\nRESOLUTION-DATE COMPLETENESS BY STATUS:")
print(resolution_status_percentage.round(2).to_string())

# TASK 64: TICKET RESOLUTION DURATION

ticket_resolution_audit["issue_created"] = pd.to_datetime(
    ticket_resolution_audit["issue_created"],
    format="mixed",
    utc=True
)

ticket_resolution_audit["issue_resolution_date"] = pd.to_datetime(
    ticket_resolution_audit["issue_resolution_date"],
    format="mixed",
    utc=True
)

ticket_resolution_audit["resolution_days"] = (
    ticket_resolution_audit["issue_resolution_date"]
    - ticket_resolution_audit["issue_created"]
).dt.total_seconds() / 86400

print("\nTICKET RESOLUTION DURATION:")
print(
    ticket_resolution_audit["resolution_days"]
    .describe()
    .round(2)
)

print("\nNEGATIVE RESOLUTION DURATIONS:")
print(
    (ticket_resolution_audit["resolution_days"] < 0).sum()
)

print("\nZERO RESOLUTION DURATIONS:")
print(
    (ticket_resolution_audit["resolution_days"] == 0).sum()
)
# TASK 65: RESOLUTION-TIME OUTLIER INVESTIGATION

print("\nRESOLUTION DURATION PERCENTILES:")

print(
    ticket_resolution_audit["resolution_days"]
    .quantile([0.90, 0.95, 0.99, 0.995, 1.00])
    .round(2)
)

print("\nTOP 15 LONGEST-RESOLVED TICKETS:")

longest_tickets = ticket_resolution_audit.nlargest(
    15,
    "resolution_days"
)[
    [
        "id",
        "issue_created",
        "issue_resolution_date",
        "issue_priority",
        "issue_status",
        "resolution_days"
    ]
]

print(longest_tickets.to_string(index=False))

# TASK 66: RESOLUTION DURATION BY CREATION YEAR

ticket_resolution_audit["created_year"] = (
    ticket_resolution_audit["issue_created"].dt.year
)

resolution_by_year = (
    ticket_resolution_audit.groupby("created_year")["resolution_days"]
    .agg(["count", "median", "mean"])
)

print("\nRESOLUTION DURATION BY CREATION YEAR:")
print(resolution_by_year.round(2).to_string())
# TASK 67: RESOLUTION DURATION BY PRIORITY

resolution_by_priority = (
    ticket_resolution_audit.groupby("issue_priority")["resolution_days"]
    .agg(["count", "median", "mean"])
    .sort_values("median", ascending=True)
)

print("\nRESOLUTION DURATION BY PRIORITY:")
print(resolution_by_priority.round(2).to_string())
# TASK 68: RESOLUTION DURATION BY PRIORITY AND YEAR

priority_year_analysis = (
    ticket_resolution_audit
    .groupby(["created_year", "issue_priority"])["resolution_days"]
    .agg(["count", "median"])
    .reset_index()
)

print("\nRESOLUTION DURATION BY YEAR AND PRIORITY:")
print(priority_year_analysis.to_string(index=False))
print("\nANNUAL ISSUE VOLUME BY ISSUE TYPE:")
print(annual_issue_type.to_string())

print("\nTOTAL RECORDS BY ISSUE TYPE (2008–2022):")
print(
    annual_issue_type.sum()
    .sort_values(ascending=False)
    .to_string()
)

# TASK 69: ANNUAL ISSUE VOLUME BY TOP 5 ISSUE TYPES

import matplotlib.pyplot as plt

# Identify the five most frequent issue types
top_5_types = (
    annual_issue_type.sum()
    .sort_values(ascending=False)
    .head(5)
    .index
)

# Filter the annual summary
top_5_annual = annual_issue_type[top_5_types]

# Create the line chart
plt.figure(figsize=(14, 7))

for issue_type in top_5_annual.columns:
    plt.plot(
        top_5_annual.index,
        top_5_annual[issue_type],
        marker="o",
        label=issue_type
    )

plt.title(
    "Annual Issue Volume by Top 5 Issue Types (2008–2022)",
    fontsize=15
)

plt.xlabel("Year", fontsize=12)
plt.ylabel("Number of Issues", fontsize=12)

plt.xticks(rotation=45, fontsize=10)
plt.yticks(fontsize=10)

plt.legend(title="Issue Type", fontsize=10)
plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    "annual_issue_volume_by_top5_types.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()

# TASK 70: ANNUAL PERCENTAGE SHARE BY TOP 5 ISSUE TYPES

# Calculate each issue type's percentage of total annual records
annual_issue_percentage = (
    annual_issue_type
    .div(annual_issue_type.sum(axis=1), axis=0)
    * 100
)

# Select the five most frequent issue types
top_5_percentage = annual_issue_percentage[top_5_types]

print("\nANNUAL PERCENTAGE SHARE BY TOP 5 ISSUE TYPES:")
print(top_5_percentage.round(2).to_string())

# TASK 71: VISUALISE ANNUAL PERCENTAGE SHARE

plt.figure(figsize=(12, 6))

for issue_type in top_5_percentage.columns:
    plt.plot(
        top_5_percentage.index,
        top_5_percentage[issue_type],
        marker="o",
        label=issue_type
    )

plt.title("Annual Percentage Share by Top 5 Issue Types (2008–2022)")
plt.xlabel("Year")
plt.ylabel("Percentage of Total Issues")
plt.xticks(top_5_percentage.index, rotation=45)
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("annual_percentage_share_top5_types.png", dpi=300)
plt.show()

# TASK 72: MONTHLY TICKET VOLUME

monthly_ticket_volume = (
    ticket_resolution_audit
    .groupby("created_month")
    .size()
)

print("\nMONTHLY TICKET VOLUME:")
print(monthly_ticket_volume.to_string())

print("\nMONTHLY TICKET VOLUME SUMMARY:")
print(monthly_ticket_volume.describe().round(2))

print("\nHIGHEST TICKET VOLUME MONTH:")
print(monthly_ticket_volume.idxmax())
print(monthly_ticket_volume.max())

print("\nLOWEST TICKET VOLUME MONTH:")
print(monthly_ticket_volume.idxmin())
print(monthly_ticket_volume.min())

# TASK 71: MEDIAN RESOLUTION TIME BY CREATION YEAR

import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))

plt.plot(
    resolution_by_year.index,
    resolution_by_year["median"],
    marker="o"
)

plt.title("Median Ticket Resolution Time by Creation Year (2008–2022)")
plt.xlabel("Ticket Creation Year")
plt.ylabel("Median Resolution Time (Days)")

plt.xticks(resolution_by_year.index, rotation=45)
plt.grid(True, alpha=0.3)
plt.yscale("log")
plt.tight_layout()
plt.savefig("median_resolution_time_by_year.png", dpi=300)
plt.show()

# RECENT-YEAR MEDIAN RESOLUTION TIME (2016–2022)

recent_resolution = resolution_by_year.loc[2016:2022]

plt.figure(figsize=(10, 5))

plt.plot(
    recent_resolution.index,
    recent_resolution["median"],
    marker="o"
)

plt.title("Median Ticket Resolution Time (2016–2022)")
plt.xlabel("Ticket Creation Year")
plt.ylabel("Median Resolution Time (Days)")

plt.xticks(recent_resolution.index)
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig("median_resolution_time_2016_2022.png", dpi=300)
plt.show()

# TASK 74: MEDIAN RESOLUTION TIME BY PRIORITY

priority_resolution_median = (
    ticket_resolution_audit
    .groupby("issue_priority")["resolution_days"]
    .median()
    .sort_values()
)

print("\nMEDIAN RESOLUTION TIME BY PRIORITY:")
print(priority_resolution_median.round(2).to_string())

# TASK 75: UNKNOWN PRIORITY — RESOLUTION TIME BY CREATION YEAR

unknown_priority_analysis = (
    ticket_resolution_audit[
        ticket_resolution_audit["issue_priority"] == "unknown"
    ]
    .groupby("created_year")["resolution_days"]
    .agg(["count", "median", "mean"])
    .reset_index()
)

print("\nUNKNOWN PRIORITY — RESOLUTION TIME BY CREATION YEAR:")
print(unknown_priority_analysis.round(2).to_string(index=False))

# TASK 76: KNOWN VS UNKNOWN PRIORITY — YEARLY MEDIAN RESOLUTION TIME

ticket_resolution_audit["priority_group"] = (
    ticket_resolution_audit["issue_priority"]
    .apply(lambda x: "Unknown" if x == "unknown" else "Known")
)

priority_group_yearly = (
    ticket_resolution_audit
    .groupby(["created_year", "priority_group"])["resolution_days"]
    .agg(["count", "median"])
    .reset_index()
)

print("\nYEARLY RESOLUTION TIME: KNOWN VS UNKNOWN PRIORITY")
print(priority_group_yearly.round(2).to_string(index=False))

# TASK 77: KNOWN VS UNKNOWN PRIORITY — RESOLUTION TIME TREND

import matplotlib.pyplot as plt

priority_median_pivot = priority_group_yearly.pivot(
    index="created_year",
    columns="priority_group",
    values="median"
)

plt.figure(figsize=(12, 6))

for group in priority_median_pivot.columns:
    plt.plot(
        priority_median_pivot.index,
        priority_median_pivot[group],
        marker="o",
        label=group
    )

plt.yscale("log")

plt.title("Yearly Median Resolution Time: Known vs Unknown Priority")
plt.xlabel("Ticket Creation Year")
plt.ylabel("Median Resolution Time (Days, Log Scale)")

plt.xticks(priority_median_pivot.index, rotation=45)
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

plt.savefig(
    "known_vs_unknown_priority_resolution_trend.png",
    dpi=300
)

plt.show()

# TASK 78: RESOLUTION DURATION BY PRIORITY AND CREATION YEAR

import matplotlib.pyplot as plt

priority_year_pivot = priority_year_analysis.pivot(
    index="created_year",
    columns="issue_priority",
    values="median"
)

plt.figure(figsize=(14, 7))

for priority in priority_year_pivot.columns:
    plt.plot(
        priority_year_pivot.index,
        priority_year_pivot[priority],
        marker="o",
        label=priority
    )

plt.yscale("log")

plt.title("Yearly Median Resolution Duration by Priority")
plt.xlabel("Ticket Creation Year")
plt.ylabel("Median Resolution Duration (Days, Log Scale)")

plt.xticks(priority_year_pivot.index, rotation=45)
plt.legend(
    title="Priority",
    loc="upper right",
    fontsize=9
)
plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    "resolution_duration_by_priority_and_year.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
print("Total ticket records:", len(ticket_data))

print(
    "Missing priority values:",
    ticket_data["issue_priority"].isna().sum()
)

print("\nPriority counts (including missing values):")

print(
    ticket_data["issue_priority"]
    .value_counts(dropna=False)
    .to_string()
)