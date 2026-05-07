
def analyze_logs(logs):

    
    log_count = {
        "ERROR": 0,
        "INFO": 0,
        "WARNING": 0
    }

    
    for log in logs:

        # Ignore case sensitivity
        log = log.upper()

    
        if log.startswith("ERROR"):
            log_count["ERROR"] += 1

        elif log.startswith("INFO"):
            log_count["INFO"] += 1

        elif log.startswith("WARNING"):
            log_count["WARNING"] += 1

    
    print("Log Counts:")
    print("ERROR :", log_count["ERROR"])
    print("INFO :", log_count["INFO"])
    print("WARNING :", log_count["WARNING"])

    
    most_frequent = max(log_count, key=log_count.get)

    print("\nMost Frequent Log Type:", most_frequent)



logs = [
    "ERROR DISK FULL",
    "INFO STARTED",
    "error file missing",
    "Warning memory low",
    "INFO user login",
    "ERROR network failed"
]

# Function call
analyze_logs(logs)