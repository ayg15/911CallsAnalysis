# 911 Calls Analysis

This project analyses 911 emergency-call data from Montgomery County, Pennsylvania, USA. It explores the most common call locations and emergency types, examines how call volumes change by date and time, and visualizes those patterns with count plots, line charts, heatmaps, and cluster maps.

The project started as a notebook and now exposes the full workflow as reusable Python functions plus a command-line script. The notebook remains as an interactive walkthrough in [`notebooks/`](notebooks/).

## Dataset

The analysis uses the [Montgomery County emergency calls dataset on Kaggle](https://www.kaggle.com/datasets/mchirico/montcoalert).
It contains the following fields:

- `lat`: latitude of the emergency call
- `lng`: longitude of the emergency call
- `desc`: description of the emergency call
- `zip`: ZIP code
- `title`: call title, including the responding department or reason
- `timeStamp`: call timestamp in `YYYY-MM-DD HH:MM:SS` format
- `twp`: township
- `addr`: address
- `e`: dummy variable that is always `1`

The analysis derives additional fields from this data:

- `reason`: department or call category extracted from `title`, such as EMS,
  Fire, or Traffic
- `hour`: hour of the day extracted from `timeStamp`
- `month`: calendar month extracted from `timeStamp`
- `day_of_week`: abbreviated weekday name
- `date`: calendar date of the call

The source dataset is not committed to this repository. Download `911.csv`
from Kaggle and place it in the repository root, or pass its location to
`main.py`.

## Analysis

The project reproduces the exploration performed in the original notebook:

- top five ZIP codes and townships by call volume
- number of unique call titles
- call totals grouped by EMS, Fire, and Traffic reason
- call distributions by weekday and month
- monthly and daily call-volume trends
- separate daily trends for each call reason
- weekday-by-hour and weekday-by-month heatmaps
- clustered views of the hourly and monthly call patterns

## Repository structure

```text
.
|-- analysis.py                       # loading, features, and aggregations
|-- visualizations.py                 # reusable plotting functions
|-- main.py                           # complete command-line workflow
|-- notebooks/
|   `-- 911 Calls Data Analysis.ipynb # interactive walkthrough
|-- requirements.txt
`-- README.md
```

## Setup

Use Python 3.10 or newer. Create a virtual environment and install the dependencies:

```powershell
python -m venv .venv
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

The execution-policy change applies only to the current PowerShell session.

## Run the analysis

With `911.csv` in the repository root:

```powershell
python main.py
```

For a dataset stored elsewhere, and a custom plot directory:

```powershell
python main.py path/to/911.csv --output-dir reports
```

The script prints the summary statistics and saves all charts from the
original analysis as PNG files in `output/`, or in the directory supplied with
`--output-dir`. Add `--show` to display the plots interactively as well.

## Use the modules directly

```python
from analysis import load_calls, prepare_calls, summarize_calls
from visualizations import plot_calls_by_reason

calls = prepare_calls(load_calls("911.csv"))
print(summarize_calls(calls))
figure = plot_calls_by_reason(calls)
figure.show()
```

Open `notebooks/911 Calls Data Analysis.ipynb` from the repository root to
step through the same analysis interactively.
