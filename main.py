import os
from moodjournal import entry, view, plot, pie

def password():
    passwordfile = "password.txt"

    if not os.path.exists(passwordfile):
        newpass = input("\nCreate a new password: ")
        confirmpass = input("Re-enter your password to confirm: ")
        if newpass == confirmpass:
            with open (passwordfile,'w')as file:
                file.write(newpass)
            print("\nNew password created succesfully!! \n")
        else:
            print ("Password didn't match. Restrart the program")
            return false
    with open(passwordfile,'r') as file:
        savedpass=file.read()

        for attempt in range(3):
            entered = input("\nEnter your password to access your mood journal:")
            if entered == savedpass:
                print(" Access granted!")
                return True
            else:
                print(f" \nINcorrect password. Attempts left: {2- attempt}")

        print ("ACCESS DENIED. Exiting program")
        return False
    
    
def menu():
    while True:
        
        print ("\n~ W E L C O M E ~")
        print (" \n1. Write a new entry")
        print ("2. View past entries")
        print ("3. Show my mood graph!")
        print ("4. Show my mood pie!")
        print ("5. Exit")
        choice = input ("\nChoose an option (1-5): ")

        if choice == '1':
            entry()
        elif choice == '2':
            view()
        elif choice == '3':
            plot()
        elif choice == '4':
            pie()
        elif choice == '5':
            print ("Take care! See you again!")
            break
        else:
            print (" Invalid option Please choose 1 or 2.")

  
if __name__ == "__main__":
    if password():
        menu()
