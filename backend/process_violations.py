import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
from datetime import datetime
import os

# ---------- CONFIG ----------
POINTS_PENALTY = 500  # points to reduce per violation
POINTS_REWARD = 10   # points for signal followers

# ---------- INIT FIREBASE ----------
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

print("[OK] Firebase Admin initialized")

def process_results(csv_file, points_change, is_positive=False):
    try:
        df = pd.read_csv(csv_file)
    except FileNotFoundError:
        print(f"[WARN] {csv_file} not found, skipping.")
        return

    action = "reward" if is_positive else "violation"
    print(f"\n[INFO] Loaded {len(df)} {action} records from {csv_file}")

    for index, row in df.iterrows():
        raw_plate = row["plate"]
        if pd.isna(raw_plate) or not isinstance(raw_plate, str):
            continue

        plate = raw_plate.strip().upper()
        if not plate:
            continue

        # If it's a violation file, double check the 'violated' flag
        if not is_positive and row.get("violated") == False:
            continue

        print(f"[ALERT] Processing {action} for plate: {plate}")

        # Find user with this vehicle number
        users_ref = db.collection("users")
        query = users_ref.where("vehicle", "==", plate).limit(1)
        results = query.stream()

        user_found = False

        for doc in results:
            user_found = True
            user_ref = users_ref.document(doc.id)
            user_data = doc.to_dict()

            # ---- 5-MINUTE BUFFER CHECK ----
            # If the user already got a Safe driving reward within the last 5 minutes, skip
            if is_positive:
                history = user_data.get("history", [])
                import re
                last_reward_time = None
                for entry in reversed(history):
                    if isinstance(entry, str) and "Safe driving reward" in entry:
                        m = re.search(r'at\s+([\d\-]+ [\d:]+)', entry)
                        if m:
                            try:
                                last_reward_time = datetime.strptime(m.group(1), "%Y-%m-%d %H:%M:%S")
                            except ValueError:
                                pass
                        break
                if last_reward_time:
                    elapsed = (datetime.now() - last_reward_time).total_seconds()
                    if elapsed < 300:  # 300 seconds = 5 minutes
                        user_name = user_data.get("name", doc.id)
                        print(f"[SKIP] {user_name} already got a Safe driving reward {int(elapsed)}s ago (buffer active). Skipping.")
                        user_found = True
                        continue
            # ---- END BUFFER CHECK ----

            old_points = user_data.get("points", 0)
            new_points = max(0, old_points + points_change)

            # Update points + log history
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if is_positive:
                history_msg = f"Safe driving reward <br> (+{points_change} pts) <br> at {timestamp}"
                update_data = {
                    "points": new_points,
                    "history": firestore.ArrayUnion([history_msg])
                }
            else:
                history_msg = f"Traffic Violation detected <br> ({points_change} pts) <br> at {timestamp}"
                update_data = {
                    "points": new_points,
                    "lastViolation": firestore.SERVER_TIMESTAMP,
                    "history": firestore.ArrayUnion([history_msg])
                }

            user_ref.update(update_data)
            user_name = user_data.get("name", doc.id)
            print(f"[OK] Updated user {user_name}: {old_points} → {new_points}")

        if not user_found:
            print(f"[FAIL] No user found for plate: {plate}")

# ---------- MAIN PROCESS ----------
# 1. Process Violations (Penalize)
violation_files = [
    "../red_light_project/dviolation.csv",
    "dviolation.csv"
]
processed_violation = False
for csv_file in violation_files:
    if os.path.exists(csv_file):
        process_results(csv_file, -POINTS_PENALTY, is_positive=False)
        processed_violation = True
        break
if not processed_violation:
    print("[WARN] No violation CSV files found.")

# 2. Process Positive Signals (Reward)
positive_files = [
    "../red_light_project/pviolation.csv",
    "pviolation.csv"
]
processed_positive = False
for csv_file in positive_files:
    if os.path.exists(csv_file):
        process_results(csv_file, POINTS_REWARD, is_positive=True)
        processed_positive = True
        break
if not processed_positive:
    print("[WARN] No positive signals CSV files found.")

print("\n[DONE] All processing completed")
