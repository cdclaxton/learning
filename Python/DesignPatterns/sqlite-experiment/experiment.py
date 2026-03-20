import os
import sqlite3
from dataclasses import dataclass
from datetime import datetime, timedelta

import numpy as np

# SQL statement to make the vessels table
sql_statement = """CREATE TABLE vessels (
    timestamp TIMESTAMP,
    name TEXT,
    latitude REAL,
    longitude REAL
);"""


@dataclass
class VesselObservation:
    """Class for representing a vessel observation."""

    timestamp: datetime  # Observation time
    name: str  # Vessel name
    latitude: float  # Vessel latitude
    longitude: float  # Vessel longitude


def delete_database(database_filepath: str):
    """Delete the database file."""

    if os.path.exists(database_filepath):
        print(f"Removing database file: {database_filepath}")
        os.remove(database_filepath)


def create_database(database_filepath: str):
    """Create the database."""

    print(f"Creating database at: {database_filepath}")
    with sqlite3.connect(
        database_filepath, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
    ) as conn:
        cursor = conn.cursor()
        cursor.execute(sql_statement)
        conn.commit()


def generate_data(n_vessels: int):
    """Generate synthetic data."""

    mean_time_interval_seconds = 60
    std_dev_time_interval_seconds = 4
    std_dev_position = 0.01
    p_detection = 0.7

    # Synthetic vessel data
    vessel_data: list[VesselObservation] = []

    for i in range(n_vessels):
        date = datetime.now() - timedelta(days=1)
        vessel_name = f"vessel-{i + 1}"
        latitude = 46.4
        longitude = -10.99

        while date < datetime.now():
            # Time interval between transmissions
            interval = np.random.normal(
                loc=mean_time_interval_seconds, scale=std_dev_time_interval_seconds
            )
            date += timedelta(seconds=interval)

            # Is the transmission detected?
            is_detected = np.random.uniform(0, 1) < p_detection

            # New vessel position
            latitude += np.random.normal(0, std_dev_position)
            longitude += np.random.normal(0, std_dev_position)

            if is_detected:
                vessel_data.append(
                    VesselObservation(date, vessel_name, latitude, longitude)
                )

    return vessel_data


def write_data_to_database(
    database_filepath: str, vessel_data: list[VesselObservation]
):
    """Write the vessel data to the database."""

    print(f"Writing to database at: {database_filepath}")
    with sqlite3.connect(
        database_filepath, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
    ) as conn:
        cursor = conn.cursor()

        for data in vessel_data:
            cursor.execute(
                "INSERT INTO vessels VALUES (?, ?, ?, ?)",
                (data.timestamp, data.name, data.latitude, data.longitude),
            )

        conn.commit()


def read_data_from_database(database_filepath: str) -> list[VesselObservation]:
    """Read all data from the database."""

    all_vessels = []

    print(f"Reading from database at: {database_filepath}")
    with sqlite3.connect(
        database_filepath, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
    ) as conn:
        cursor = conn.cursor()
        res = cursor.execute("SELECT * FROM vessels")

        for single_result in res.fetchall():
            all_vessels.append(VesselObservation(*single_result))

    return all_vessels


if __name__ == "__main__":
    # Database filepath
    filepath = "./database.db"

    # If the database file exists, then delete it
    delete_database(filepath)

    # Create the database
    create_database(filepath)

    # Generate synthetic vessel data
    vessel_data = generate_data(2)
    print(f"Generated {len(vessel_data)} vessel observations")

    # Write data to the database
    write_data_to_database(filepath, vessel_data)

    # Read the data from the database
    vessel_data_read = read_data_from_database(filepath)
    print(f"Read {len(vessel_data)} vessel observations")

    # Check the data from the database matches that generated
    assert len(vessel_data_read) == len(vessel_data)
    for idx in range(len(vessel_data)):
        assert vessel_data[idx] == vessel_data_read[idx], (
            f"Expected: {vessel_data[idx]}, actual: {vessel_data_read[idx]}"
        )
    print("Data matches")

    # Clean up
    delete_database(filepath)
