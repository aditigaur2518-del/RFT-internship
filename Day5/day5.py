
import os


file_name = "students.csv"


if not os.path.exists(file_name):
    print("CSV file not found!")
else:

    students = []
    total_marks = 0
    valid_marks_count = 0

    
    with open(file_name, "r") as file:

        
        lines = file.readlines()

        
        headers = lines[0].strip().split(",")

        
        for line in lines[1:]:

            
            line = line.strip()

            
            if line == "":
                continue

            
            values = line.split(",")

            
            while len(values) < len(headers):
                values.append("N/A")

            
            student = {}

            for i in range(len(headers)):

                key = headers[i].upper()
                value = values[i]

                
                if key in ["AGE", "MARKS"]:

                    if value.strip() == "" or value == "N/A":
                        student[key] = "Missing"

                    else:
                        student[key] = int(value)

                        
                        if key == "MARKS":
                            total_marks += int(value)
                            valid_marks_count += 1

                else:
                    student[key] = value

            
            students.append(student)

    
    print("Student Data:\n")
    print(students)

    
    if valid_marks_count > 0:
        average = total_marks / valid_marks_count
        print("\nAverage Marks:", average)
    else:
        print("\nNo valid marks found.")