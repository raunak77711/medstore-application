import inventory
import sales
import restock

# function: Display the header
def show_header():
    print("                ┌───┐                    ")
    print("                │ + │                    ")
    print("            ┌───┴───┴───┐                ")
    print("            │           │                ")
    print("            │  MEDSTORE │                ")
    print("            │           │                ")
    print("            └───────────┘                ")

# function: Display the main menu
def show_menu():
    print("\n" + "-" * 50)
    print(" MEDSTORE PVT. LTD.")
    print(" WHOLESALE MANAGEMENT SYSTEM")
    print("-" * 60)
    
    print("")
    print("  1.  View Inventory")
    print("  2.  Make a Sale")
    print("  3.  Restock Medicines")
    print("  4.  Exit")
    print("=" * 60)

def main():
    print("\n  Welcome to MedStore Wholesale System!")
    show_header()   # <-- call header here

    running = True
    while running:
        show_menu()
        choice = input("Please enter your choice (1-4): ").strip()

        if choice == "1":
            inventory.show_inventory()

        elif choice == "2":
            sales.make_sale()

        elif choice == "3":
            restock.do_restock()

        elif choice == "4":
            print("\n Thank you for using MedStore :).\n")
            running = False
        else:
            print("\n  YOU ENTERED AN INVALID CHOICE!, Please enter between 1, 2, 3, or 4.")

# Run the program
main()