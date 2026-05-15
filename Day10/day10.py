

logs = [
    "ERROR DISK FULL",
    "INFO STARTED",
    "ERROR FILE MISSING",
    "WARNING MEMORY LOW"
]

log_count = {
    "ERROR": 0,
    "INFO": 0,
    "WARNING": 0
}


for log in logs:
    log = log.upper()   

    if "ERROR" in log:
        log_count["ERROR"] += 1

    elif "INFO" in log:
        log_count["INFO"] += 1

    elif "WARNING" in log:
        log_count["WARNING"] += 1


print("Log Counts:")
for key, value in log_count.items():
    print(key, "=", value)


most_frequent = max(log_count, key=log_count.get)

print("\nMost Frequent Log Type:", most_frequent)