phonebook = {}   # empty dictionary


def add_contact():
    name = input("Enter name: ").upper()
    number = input("Enter phone number: ")
    
    if name in phonebook:
        print("Contact already exists!")
    else:
        phonebook[name] = number
        print("Contact added successfully!")


def search_contact():
    name = input("Enter name to search: ").upper()
    
    if name in phonebook:
        print(f"{name}: {phonebook[name]}")
    else:
        print("Contact not found!")


def partial_search():
    key = input("Enter partial name: ").upper()
    found = False
    
    for name in phonebook:
        if key in name:
            print(f"{name}: {phonebook[name]}")
            found = True
    
    if not found:
        print("No matching contacts found!")


def delete_contact():
    name = input("Enter name to delete: ").upper()
    
    if name in phonebook:
        del phonebook[name]
        print("Contact deleted!")
    else:
        print("Contact not found!")



n = int(input("How many contacts you want to add initially? "))

for i in range(n):
    print(f"\nEnter contact {i+1}")
    add_contact()



while True:
    print("\nPHONEBOOK MENU")
    print("1. Add Contact")
    print("2. Search Contact")
    print("3. Delete Contact")
    print("4. Partial Search")
    print("5. Show All Contacts")
    print("6. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        add_contact()
    elif choice == '2':
        search_contact()
    elif choice == '3':
        delete_contact()
    elif choice == '4':
        partial_search()
    elif choice == '5':
        print("\nAll Contacts:")
        if phonebook:
            for name, number in phonebook.items():
                print(f"{name}: {number}")
        else:
            print("No contacts available!")
    elif choice == '6':
        print("Exiting Phonebook...")
        break
    else:
        print("Invalid choice,  this contact is  not present, try again!")