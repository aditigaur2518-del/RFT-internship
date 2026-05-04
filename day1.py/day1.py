data=[10,None,20,10,"",30,None ,40]
clean_data = []
for item in data:
    if item is None or item =="":
        continue
    if item  not in clean_data:
        clean_data.append(item)
removed_count = len(data)-len(clean_data)
clean_data.sort()
print("Clean data:",clean_data)
print("Removed values:",removed_count)