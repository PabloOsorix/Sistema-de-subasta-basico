import os

current_dir = os.path.dirname(os.path.abspath(__file__))
json_users_database_path = os.path.join(current_dir, "subastaUsers.json")
json_operations_database_path = os.path.join(current_dir, "subastaOperations.json")
json_event_database_path = os.path.join(current_dir, "subastaEvents.json")
json_bids_database_path = os.path.join(current_dir, "subastaBids.json")