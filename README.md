# Help Desk Ticket Analysis

A descriptive analysis of help desk tickets using Python, pandas, and matplotlib. The project examines ticket volume, issue types, priority and status, data quality, and recorded resolution time. It includes the analysis script, source datasets, 14 analysis charts, supporting dataset documentation, and PDF findings.

## Questions explored

- How does ticket volume change by month and year, and how does it vary by issue type?
- What are the distributions of ticket priority and status? How do priority and status relate?
- How do recorded processing time and calendar time from creation to resolution compare?
- What data quality issues should be considered before interpreting the results?

## Key findings

The analysis covered **43,352 tickets**. **25,989 tickets (about 60%)** had an `Unknown` priority, which limits priority-based comparisons. Among **43,048 tickets with resolution dates**, mean calendar resolution time was **864.04 days** and the median was **45.46 days**, showing a strongly right-skewed distribution.

For tickets with a known priority, median calendar resolution time ranged from **3.75 days for Highest** to **9.05 days for Low**. This is an observed association; it does not show that priority caused the difference or prove operational effectiveness. Unknown-priority tickets had a median of **1,400.40 days**. The analysis cannot establish why; old records, migration, missing priority information, or other differences should be investigated before interpreting those durations as active service delays.

### Recommendations

1. Investigate why priority is missing so often, including whether the records predate a system or policy change. Consider requiring priority for new tickets where appropriate.
2. Review the longest calendar resolution times and validate their creation and resolution dates against ticket history and workflow records.
3. Compare resolution patterns alongside ticket type, workload, and service targets before drawing conclusions about team performance.
4. Treat the `Unknown` group separately until its data origin and record history are understood.

These findings are descriptive and should be read with the data limitations in mind. Calendar elapsed time is not the same as active staff effort.

## Data and attribution

The main analysis uses:

- `issues.csv` — ticket records, including type, priority, status, creation and resolution dates, and workflow-time fields.
- `issues_change_history.csv` — ticket history used to audit workflow and record timelines.
- `issues_snapshot.csv` — assignee-level snapshots used to examine assignment activity.

The repository also contains `holidays_by_country.csv`, `sample_utterances.csv`, and `issues_snapshot_sample.xlsx` as supporting dataset files. Dataset documentation (`FEATURES.md`, `EXAMPLE.md`) describes the data structure and masking. The provider notes that identifying details were masked.

**Source:** Abdellatif, Mohammad. *Help Desk Tickets*. Mendeley Data, Version 3. [https://doi.org/10.17632/btm76zndnt.3](https://doi.org/10.17632/btm76zndnt.3). The dataset record lists a [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) license. If using a different downloaded version, cite that version’s record.

## Charts

The 14 analysis charts are available in the repository:

- Ticket volume: [monthly trend](monthly_issue_volume_trend.png), [annual total](annual_issue_volume_chart.png), and [average monthly pattern](average_monthly_issue_pattern.png).
- Issue types: [annual volume by type](annual_issue_volume_by_issue_type.png), [top five annual volume](annual_issue_volume_by_top5_types.png), [annual share of top five](annual_percentage_share_top5_types.png), [share trend](ticket_share_trend.png), and [overall distribution](overall_issue_type_distribution.png).
- Priority and status: [priority distribution](ticket_priority_distribution.png) and [status by priority](ticket_status_by_priority.png).
- Resolution time: [median by year](median_resolution_time_by_year.png), [2016–2022 comparison](median_resolution_time_2016_2022.png), [known versus unknown priority](known_vs_unknown_priority_resolution_trend.png), and [priority by year](resolution_duration_by_priority_and_year.png).

`db.png` and `process-flow.png` are supporting dataset images, not analysis charts.

## Run the analysis

Requirements: Python 3, `pandas`, and `matplotlib`.

```bash
python -m pip install pandas matplotlib
```

The current `Project 4.py` script expects the input files at:

```text
%USERPROFILE%\Desktop\Help Desk Tickets
```

It loads `issues.csv`, `issues_change_history.csv`, and `issues_snapshot.csv` from that folder. To run the script as currently written on Windows, place those files in that location and run:

```bash
python "Project 4.py"
```

The script saves generated chart PNGs in its current working directory. In PyCharm, set the run configuration's working directory to the folder where you want the charts saved. If you cloned this repository elsewhere, update the `data_folder` path near the top of `Project 4.py` to the location of the datasets before running it.

## Files

- `Project 4.py` — analysis and chart-generation script.
- `*.csv`, `*.xlsx` — source and supporting data files.
- `*.png` — analysis charts and supporting images.
- `Help Desk Ticket Analysis_ Key Findings (1).pdf` — combined project overview, run instructions, source attribution, findings, and recommendations.
- `Help Desk Ticket Analysis_ Key Findings.pdf` — findings report.
- `FEATURES.md`, `EXAMPLE.md` — dataset reference documentation.
