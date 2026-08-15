"""
Analyzes results from results/trials.db to answer the core research question:
Does having more words to work with increase an attorney's chance of winning?

Sections:
1. Data loading + basic sanity checks (UNKNOWN rate, word-limit compliance)
2. Win rate for "more words" side
3. Descriptive stats on actual word counts used
4. Visualization

"""

import sqlite3
from pathlib import Path
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt

DB_PATH = Path('results/trials.db')
CHART_PATH = Path('results/win_rate_chart.png')

def load_data():
    if not DB_PATH.exists():
        raise FileNotFoundError(
            f"Could not find the database file '{DB_PATH}'"
        )

    connection = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM trials", connection)
    connection.close()

    if df.empty:
        raise ValueError("Trials table is empty - no data to analyze!")

    return df

def win_rate_analysis(df):
    print(f"Total trials: {len(df)}")
    print(df["winner"].value_counts())

    # Excluding "UNKNOWN" winner trials
    known_df = df[df["winner"].isin(["A", "B"])].copy()

    def more_words_won(row):
        more_words_side = "A" if row["word_limit_a"] > row["word_limit_b"] else "B"
        return row["winner"] == more_words_side

    known_df["more_words_won"] = known_df.apply(more_words_won, axis=1)

    n = len(known_df)
    wins = known_df["more_words_won"].sum()
    wr = wins / n

    print(f"\nMore words won: {wins} / {n} ({wr*100:.1f}%)")

    return known_df, wr

def confidence_interval(wins, n):
    result = stats.binomtest(wins, n, p=0.5, alternative="two-sided")
    ci = result.proportion_ci(confidence_level=0.95, method="wilson")

    print(f"Win rate: {wins / n * 100:.1f}%")
    print(f"95% CI: [{ci.low * 100:.1f}%, {ci.high * 100:.1f}%]")
    print(f"p-value: {result.pvalue:.4f}")

    return ci, result.pvalue


def make_chart(win_rate, ci, n):
    fig, ax = plt.subplots(figsize=(5, 5))

    bar = ax.bar(["More words side"], [win_rate * 100], color="#4C72B0", width=0.4)

    lower_err = (win_rate - ci.low) * 100
    upper_err = (ci.high - win_rate) * 100
    ax.errorbar(
        [0], [win_rate * 100],
        yerr=[[lower_err], [upper_err]],
        fmt="none", ecolor="black", capsize=8, linewidth=1.5
    )

    ax.axhline(50, color="gray", linestyle="--", linewidth=1, label="Chance (50%)")

    ax.text(0, win_rate * 100 + upper_err + 3, f"{win_rate * 100:.1f}%",
            ha="center", fontsize=11)

    ax.set_ylabel("Win rate (%)")
    ax.set_title(f"Win Rate vs. Chance (n={n})")
    ax.set_ylim(0, 100)
    ax.legend()

    plt.tight_layout()
    CHART_PATH.parent.mkdir(exist_ok=True)
    plt.savefig(CHART_PATH, dpi=150)
    plt.close()

if __name__ == "__main__":
    df = load_data()
    known_df, win_rate = win_rate_analysis(df)

    n = len(known_df)
    wins = known_df["more_words_won"].sum()

    ci, p_value = confidence_interval(wins, n)

    make_chart(win_rate, ci, n)




