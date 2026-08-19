def is_prime(number):
    if number < 2:
        return false
    for i in range (2,int (number**0.5)+1):
        if number % i==0:
            return False
    return True

num = int(input("Enter the number to check prime or not:"))
if is_prime(num):
    print(num,"is a prime number.")
else:
    print(num,"is not a prime number.")

print("\n----------------------------------------------------")

def find_largest(*args):
    return max(args)

largest = find_largest(10,34,65,24,6,35,60,54)
print("Largest number:",largest)
print("\n----------------------------------------------------")

def student_info(**kwargs):
    print("Student Information:")
    for key ,value in kwargs.items():
        print (key,":",value)

student_info(
    Name="Aditi",
    Age=20,
    Course="Btech (AI-ML)",
    College="University",
    
) 
print("\n----------------------------------------------------")

def calculate_numbers(numbers):
    maximum = max(numbers)
    minimum = min(numbers)
    total = sum (numbers)
    average = total/len(numbers)

    return maximum, minimum , average, total 

numbers = [10,20,30,40,50]
maximum, minimum , average, total = calculate_numbers(numbers)

print("List:",numbers)
print("Maximum:",maximum)
print("Minimum",minimum)
print("Average",average)
print("Sum:",total)


