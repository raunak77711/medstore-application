import datetime
import inventory
import random
# function: it generates a unique restock note of  filename with a timestamp.

def get_restock_filename():
    now = datetime.datetime.now()
    filename = "restock_" + now.strftime("%Y%m%d_%H%M%S%p") + ".txt"
    return filename
# function: Process a restock order
# Asks supplier name, then loops to add medicines
# Generates a .txt restock note at the end
def do_restock():
    print("\n" + "=" * 60) 
    print("MEDSTORE - RESTOCK ORDER")
    print("=" * 60)

    # get supplier name
    supplier_name = input(" Enter the supplier or vendor name: ").strip()
    if supplier_name == "":
        print("The Supplier name cannot be empty.Pls enter the supplier name.")
        return

    # Lists to hold restock items
    item_names      = []
    item_brands     = []
    item_unit_types = []   # "Tablet" or "Strip"
    item_quantities = []   # quantity in chosen unit
    item_tabs_total = []   # converted to tablets
    item_unit_rates = []   # rate per unit
    item_totals     = []   # total per item

    # a loop that keeps adding the medicines until user says done
    adding = True
    while adding:
        print("\n  Add a medicine to restock order")
        inventory.show_inventory()

        medicines = inventory.read_medicines()

        try:
            id_input = input("\n  Enter medicine ID: ").strip()
            if id_input.isdigit() == False or int(id_input) < 1 or int(id_input) > len(medicines):
                print(f"  ERROR: Enter a valid ID between 1 and {len(medicines)}.")
                continue
        
        except Exception as e:
            print(f"  ERROR: {e}")
            continue

        index = int(id_input) - 1

        med        = medicines[index]
        name       = med[0]
        brand      = med[1]
        rate_tab   = float(med[3])
        rate_strip = float(med[4])
        tabs_per   = int(med[5])

        print(f"\n  Medicine : {name}")
        print(f" Brand : {brand}")
        print(f" Rate : Rs {rate_tab} / tablet   |   Rs {rate_strip} / strip ({tabs_per} tabs per strip)")

        # ask unit type for restock
        unit_choice = input("\n  Restock by (1) Tablet  or  (2) Strip? Press 1 or 2: ").strip()
        if unit_choice != "1" and unit_choice != "2":
            print(" ERROR: Enter 1 for tablet or 2 for strip.Only 1 or 2 allowed.")
            continue

        qty_input = input(" Enter quantity to restock: ").strip()
        if qty_input.isdigit() == False or int(qty_input) <= 0:
            print(" ERROR: Quantity must be a positive number.")
            continue
        qty = int(qty_input)

        if unit_choice == "1":
            unit_type   = "Tablet"
            tabs_total  = qty
            unit_rate   = rate_tab
        else:
            unit_type   = "Strip"
            tabs_total  = qty * tabs_per
            unit_rate   = rate_strip

        total = unit_rate * qty

        print(f"\n  Item Total: Rs {total:.2f}")
        confirm = input("  Add this item to restock order? (y/n): ").strip().lower()
        if confirm != "y":
            print("  Item not added.")
            continue

        # Add to restock lists
        item_names.append(name)
        item_brands.append(brand)
        item_unit_types.append(unit_type)
        item_quantities.append(qty)
        item_tabs_total.append(tabs_total)
        item_unit_rates.append(unit_rate)
        item_totals.append(total)

        print(f"  '{name}' added to restock order.")
        
        '''
     If we want to add more items to the restock order, 
     we can continue the loop. if not, we can proceed 
     to generate the restock note and update the inventory.
    '''
        more = input("\n  Add another medicine? (y/n): ").strip().lower()
        if more != "y":
            adding = False

    # Check if any items added
    if len(item_names) == 0:
        print("\n  No items in restock order. Cancelled!.")
        return

    # Calculate grand total
    grand_total = 0.0
    for t in item_totals:
        grand_total = grand_total + t

    # Print restock note on screen
    print("\n" + "=" * 65)
    print("MEDSTORE PVT. LTD.")
    print("RESTOCK NOTE")
    print("=" * 65)
    
    print(f"  Supplier : {supplier_name}")
    print(f"  Date     : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 65)
    print(f"  {'Medicine':<22} {'Brand':<15} {'Unit':<7} {'Qty':<5} {'Rate':<10} {'Total'}")
    print("-" * 65)

    for i in range(len(item_names)):
        print(f"  {item_names[i]:<22} {item_brands[i]:<15} {item_unit_types[i]:<7} {item_quantities[i]:<5} {item_unit_rates[i]:<10.2f} {item_totals[i]:.2f}")

    print("-" * 65)
    print(f"  GRAND TOTAL : Rs {grand_total:.2f}")
    print("=" * 65)

    # Confirm and save
    save_confirm = input("\n  Confirm restock and update inventory? [y/n]: ").strip().lower()
    if save_confirm != "y":
        #if user does not confirm the restock is cancelled and inventory is not updated.
        print("  Restock cancelled.")
        return

    # update stock
    for i in range(len(item_names)):
        inventory.increase_stock(item_names[i], item_tabs_total[i])

    # write restock note to file
    restock_file = get_restock_filename()
    try:
        f = open(restock_file, "w")
        f.write("=" * 65 + "\n")
        f.write("MEDSTORE- RESTOCK NOTE\n")
        f.write("=" * 65 + "\n")
        f.write(f"Bill No  : {random.randint(100000, 999999)}\n")
        f.write(f"Supplier : {supplier_name}\n")
        f.write(f"Date     : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("-" * 65 + "\n")
        f.write(f"{'Medicine':<22} {'Brand':<15} {'Unit':<7} {'Qty':<5} {'Rate':<10} {'Total'}\n")
        f.write("-" * 65 + "\n")

        for i in range(len(item_names)):
            f.write(f"{item_names[i]:<22} {item_brands[i]:<15} {item_unit_types[i]:<7} {item_quantities[i]:<5} {item_unit_rates[i]:<10.2f} {item_totals[i]:.2f}\n")

        f.write("-" * 65 + "\n")
        f.write(f"GRAND TOTAL : Rs {grand_total:.2f}\n")
        f.write("=" * 65 + "\n")
        f.close()
        print(f"\n  Restock note saved as: {restock_file}")
    except Exception as e:
        print(f"\n  ERROR: Could not save restock note - {e}")

    print("\n  Restock completed successfully! Inventory updated.")