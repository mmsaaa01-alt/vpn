# database.py
import json
import os

DB_FILE = "progress.json"

def load_progress():
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except Exception:
        return {}

def save_progress(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def mark_unit_done(unit_name):
    progress = load_progress()
    progress[unit_name] = True
    save_progress(progress)

def is_done(unit_name):
    progress = load_progress()
    return progress.get(unit_name, False)

def get_subject_stats(curriculum_data):
    """Calculates total vs completed TOPICS per subject (full 6-level traversal)."""
    progress = load_progress()
    stats = {}
    # Only use the grade keys, matched by prefix (typo-proof)
    grade_dicts = [
        val for key, val in curriculum_data.items()
        if key.startswith("Grade 9") or key.startswith("Grade 10")
    ]
    for months in grade_dicts:
        for month_name, weeks in months.items():
            for week_name, days in weeks.items():
                for day_name, subjects in days.items():
                    for subject, topics in subjects.items():
                        if subject not in stats:
                            stats[subject] = {"total": 0, "completed": 0}
                        for topic in topics:
                            stats[subject]["total"] += 1
                            if progress.get(topic, False):
                                stats[subject]["completed"] += 1
    return stats
