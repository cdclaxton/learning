import json
import logging
import matplotlib.pyplot as plt

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List

# Set the logger
logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)


def load_stop_words(filepath):
    """Loads the stop words from a text file into a set (for quick lookup)."""

    stop_words = set()
    with open(filepath, "r") as fp:
        for line in fp:
            stop_words.add(line.strip())

    assert len(stop_words) > 0
    return stop_words


def extract_tokens(record, stop_words):
    """Extract text tokens from a single record."""

    assert type(record) == dict
    assert "headline" in record, f"Headline missing in {record}"
    assert "short_description" in record, f"Short description missing in {record}"
    assert type(stop_words) == set

    # Concatenate fields
    text = record["headline"] + " " + record["short_description"]

    # Make the text all lower case
    text = text.lower()

    # Perform tokenisation (this is simplistic because of the way the data is
    # structured)
    tokens = text.replace(".", " ").split(" ")

    # Remove stop words
    tokens = [t for t in tokens if t not in stop_words]

    # Remove short tokens
    tokens = [t for t in tokens if len(t) >= 4]

    return tokens


def extract_date(record):
    """Extract and parse the date from a record."""

    assert type(record) == dict
    assert "date" in record, f"Date is missing in {record}"

    return datetime.strptime(record["date"], "%Y-%m-%d")


@dataclass
class TimeStampedTokens:
    """Represents time-stamped list of tokens."""

    tokens: List[str]
    date: datetime.date


def load_data(filepath, stop_words):
    """Load the news data into memory."""

    assert type(filepath) == str
    assert type(stop_words) == set

    records = []

    with open(filepath, "r") as fp:
        for line in fp:
            # Parse the JSON line
            record = json.loads(line)

            # Extract the tokens and the text's associated date
            records.append(
                TimeStampedTokens(
                    tokens=extract_tokens(record, stop_words), date=extract_date(record)
                )
            )

    return records


class DateToCount:
    def __init__(self):
        self.date_to_count = {}

    def add(self, date):
        """Add an entry on a given date."""

        if date not in self.date_to_count:
            self.date_to_count[date] = 1
        else:
            self.date_to_count[date] += 1

    def dense_timeseries(self, min_date, max_date):
        """Returns a dense timeseries between the min and max dates."""

        dates = [min_date]
        while dates[-1] != max_date:
            dates.append(dates[-1] + timedelta(days=1))

        counts = [0 for _ in range(len(dates))]
        for date, count in self.date_to_count.items():
            if count > 0:
                idx = dates.index(date)
                counts[idx] = count

        assert type(dates) == list
        assert type(counts) == list
        assert len(dates) == len(counts)

        return dates, counts

    def min_date(self):
        """Returns the earliest date."""

        assert len(self.date_to_count) > 0
        return min(self.date_to_count.keys())

    def max_date(self):
        """Returns the latest date."""

        assert len(self.date_to_count) > 0
        return max(self.date_to_count.keys())

    def __len__(self):
        """Returns the number of distinct dates."""
        return len(self.date_to_count)


def record_to_timeseries(records):
    """Convert the records to a timeseries dataset."""

    assert type(records) == list

    # Create a dict of a token to the dates on which the token appears
    token_to_date_count = {}

    for r in records:
        assert type(r) == TimeStampedTokens

        for token in r.tokens:
            if not token in token_to_date_count:
                token_to_date_count[token] = DateToCount()

            token_to_date_count[token].add(r.date)

    return token_to_date_count


def plot_hist_number_distinct_tokens(timeseries):
    """Plot a histogram of the number of distinct dates for a token."""

    num_dates = [len(c) for c in timeseries.values()]

    plt.hist(num_dates, bins=250)
    plt.xlabel("Number of distinct dates for a token")
    plt.ylabel("Log frequency")
    plt.yscale("log")
    plt.tight_layout()
    plt.savefig("./images/distinct_dates_hist.png")
    plt.close()


def plot_total_tokens_per_day(timeseries):
    """Plot the total number of tokens on a given day."""

    date_to_total_tokens = {}

    for _, date_count in timeseries.items():
        assert type(date_count) == DateToCount

        for date, count in date_count.date_to_count.items():
            if date not in date_to_total_tokens:
                date_to_total_tokens[date] = 0

            date_to_total_tokens[date] += count

    plt.plot(date_to_total_tokens.keys(), date_to_total_tokens.values(), ".")
    plt.xlabel("Date")
    plt.ylabel("Number of tokens")
    plt.tight_layout()
    plt.savefig("./images/number_of_tokens_per_day.png")
    plt.close()


def calc_min_max_date(timeseries):
    """Calculate the minimum and maximum date."""

    assert type(timeseries) == dict
    min_date = None
    max_date = None

    for _, date_to_count in timeseries.items():
        token_min_date = date_to_count.min_date()
        token_max_date = date_to_count.max_date()

        if min_date is None or min_date > token_min_date:
            min_date = token_min_date

        if max_date is None or max_date < token_max_date:
            max_date = token_max_date

    assert min_date <= max_date

    return min_date, max_date


def plot_token_date_counts(timeseries, tokens):
    """Plot the counts of a list of tokens."""

    assert type(timeseries) == dict
    assert type(tokens) == list
    assert len(tokens) > 0

    min_date, max_date = calc_min_max_date(timeseries)

    fig, axs = plt.subplots(len(tokens))
    for idx, token in enumerate(tokens):
        dates, counts = timeseries[token].dense_timeseries(min_date, max_date)
        assert type(dates) == list
        assert type(counts) == list

        axs[idx].plot(dates, counts, ".", label=token)
        axs[idx].set_ylabel("Count")
        axs[idx].legend(loc="upper left")

        if idx == len(tokens) - 1:
            axs[idx].set_xlabel("Date")

    plt.tight_layout()
    plt.savefig("./images/token_counts.png")
    plt.close()


def calculate_statistics(timeseries):
    assert type(timeseries) == dict

    plot_hist_number_distinct_tokens(timeseries)
    plot_total_tokens_per_day(timeseries)
    plot_token_date_counts(
        timeseries, ["afghanistan", "covid", "climate", "trump", "drugs"]
    )


if __name__ == "__main__":
    # Load the stop words
    logging.info(f"Reading stop words")
    stop_words = load_stop_words("./data/stop-words.txt")

    # Load the data into memory
    logging.info(f"Reading dataset")
    dataset = load_data("./data/News_Category_Dataset_v3.json", stop_words)
    logging.info(f"Read {len(dataset)} records")

    # Convert the data to a timeseries
    logging.info(f"Converting dataset to a timeseries")
    timeseries = record_to_timeseries(dataset)
    logging.info(f"Dataset has {len(timeseries)} distinct tokens")

    # Calculate statistics
    calculate_statistics(timeseries)
