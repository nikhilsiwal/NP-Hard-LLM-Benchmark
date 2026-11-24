
import sqlite3
import json
import os


def initialize_database(db_path="results/experiments.db"):

    folder = os.path.dirname(db_path)

    if folder:
        os.makedirs(folder, exist_ok=True)

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS experiments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            problem_name TEXT NOT NULL,
            provider TEXT NOT NULL,
            solution TEXT,
            validity BOOLEAN,
            accuracy REAL,
            optimality_gap REAL,
            latency REAL,
            tokens_used INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


def save_experiment(
    problem_name,
    provider,
    solution,
    metrics,
    db_path="results/experiments.db"
):

    initialize_database(db_path)

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO experiments (
            problem_name,
            provider,
            solution,
            validity,
            accuracy,
            optimality_gap,
            latency,
            tokens_used
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        problem_name,
        provider,
        json.dumps(solution),
        metrics.get("validity"),
        metrics.get("accuracy"),
        metrics.get("optimality_gap"),
        metrics.get("latency"),
        metrics.get("tokens_used")
    ))

    connection.commit()
    experiment_id = cursor.lastrowid
    connection.close()

    return experiment_id


def get_all_experiments(db_path="results/experiments.db"):

    initialize_database(db_path)

    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM experiments
        ORDER BY id DESC
    """)

    experiments = [
        dict(row) for row in cursor.fetchall()
    ]

    connection.close()

    for experiment in experiments:
        if experiment["solution"] is not None:
            experiment["solution"] = json.loads(
                experiment["solution"]
            )

    return experiments


if __name__ == "__main__":

    initialize_database()

    sample_metrics = {
        "validity": True,
        "accuracy": 1.0,
        "optimality_gap": 0.0,
        "latency": 1.5,
        "tokens_used": 150
    }

    experiment_id = save_experiment(
        problem_name="subset_sum",
        provider="mock",
        solution=[1, 0, 1, 0],
        metrics=sample_metrics
    )

    print("Experiment Saved!")
    print("Experiment ID:", experiment_id)

    experiments = get_all_experiments()

    print("\nSaved Experiments:")

    for experiment in experiments:
        print(experiment)
