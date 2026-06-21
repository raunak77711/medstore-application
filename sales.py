import datetime
import inventory
import random
# function: generation of a unique invoice filename
def get_invoice_filename():
    now = datetime.datetime.now()
    filename = "invoice_" + now.strftime("%Y%m%d_%H%M%S%p") + ".txt"
    return filename

# function: Process a sale
# Asks customer name, then loops to add medicines
# generates a .txt invoice at the end

def make_sale():
    print("\n" + "=" * 60)
    print("MEDSTORE - NEW SALE")
    print("=" * 60)

    # Get customer name
    customer_name = input("Enter customer name: ").strip()
    if customer_name == "":
        print("  ERROR: Customer name cannot be empty.")
        return

    # list to hold sale items
    item_names      = []
    item_brands     = []
    item_unit_types = []   # "tablet" or "strip"
    item_quantities = []   # quantity in the unit chosen (strips or tablets)
    item_tabs_total = []   # quantity converted to tablets (for stock)
    item_unit_rates = []   # rate per chosen unit (before discount)
    item_discounts  = []   # discount amount per item
    item_totals     = []   # final total per item

    # keep adding medicines until user says done
    adding = True
    while adding:
        print("\n  Add a medicine to this sale")
        inventory.show_inventory()

        medicines = inventory.read_medicines()

        id_input = input("\n  Enter medicine ID: ").strip()
        if id_input.isdigit() == False or int(id_input) < 1 or int(id_input) > len(medicines):
            print(f"  ERROR: Enter a valid ID between 1 and {len(medicines)}.")
            continue

        index = int(id_input) - 1
        med        = medicines[index]
        name       = med[0]
        brand      = med[1]
        stock      = int(med[2])
        rate_tab   = float(med[3])
        rate_strip = float(med[4])
        tabs_per   = int(med[5])

        print(f"\n  Medicine : {name}")
        print(f"  Brand    : {brand}")
        print(f"  In Stock : {stock} tablets")
        print(f"  Rate     : Rs {rate_tab} / tablet   |   Rs {rate_strip} / strip ({tabs_per} tabs per strip)")

        # ask unit type
        unit_choice = input("\n  Sell by (1) Tablet  or  (2) Strip? Press 1 or 2: ").strip()
        if unit_choice != "1" and unit_choice != "2":
            print("  ERROR: Enter 1 for tablet or 2 for strip.")
            continue

        # ask quantity
        qty_input = input("  Enter quantity: ").strip()
        if qty_input.isdigit() == False or int(qty_input) <= 0:
            print("  ERROR: Quantity must be a positive number.")
            continue
        qty = int(qty_input)

        # calculate tablets needed and check stock
        if unit_choice == "1":
            unit_type    = "Tablet"
            tabs_needed  = qty
            unit_rate    = rate_tab
        else:
            unit_type    = "Strip"
            tabs_needed  = qty * tabs_per
            unit_rate    = rate_strip

        if tabs_needed > stock:
            print(f"  ERROR: Not enough stock! Available: {stock} tablets.")
            continue

        # Calculate discount (5% if buying 2 or more strips)
        discount_amount = 0.0
        if unit_choice == "2" and qty >= 2:
            subtotal        = unit_rate * qty
            discount_amount = subtotal * 0.05
            total           = subtotal - discount_amount
            print(f"  5% strip discount applied! Discount: Rs {discount_amount:.2f}")
        else:
            total = unit_rate * qty

        print(f"  Item Total: Rs {total:.2f}")

        # Confirm adding this item
        confirm = input("  Add this item to bill? [y/n]: ").strip().lower()
        if confirm != "y":
            print("  Item not added.")
            continue

        # Add to sale lists
        item_names.append(name)
        item_brands.append(brand)
        item_unit_types.append(unit_type)
        item_quantities.append(qty)
        item_tabs_total.append(tabs_needed)
        item_unit_rates.append(unit_rate)
        item_discounts.append(discount_amount)
        item_totals.append(total)

        print(f"  '{name}' added to bill.")

        more = input("\n  Add another medicine? [y/n]: ").strip().lower()
        if more != "y":
            adding = False

    # Check if any items were added
    if len(item_names) == 0:
        print("\n  No items in bill. Sale cancelled.")
        return

    # Calculate grand total
    grand_total       = 0.0
    total_discount    = 0.0
    for i in range(len(item_totals)):
        grand_total    = grand_total + item_totals[i]
        total_discount = total_discount + item_discounts[i]

    # Print bill on screen
    print("\n" + "=" * 65)
    print("                  MEDSTORE PVT. LTD.")
    print("                 SALES INVOICE")
    print("=" * 65)
    # print(f"  Bill No  : {random.randint(100000, 999999)}")
    print(f"  Customer : {customer_name}")
    print(f"  Date     : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S%p')}")
    print("-" * 65)
    print(f"  {'Medicine':<22} {'Brand':<15} {'Unit':<7} {'Qty':<5} {'Rate':<8} {'Disc':<8} {'Total'}")
    print("-" * 65)

    for i in range(len(item_names)):
        print(f"  {item_names[i]:<22} {item_brands[i]:<15} {item_unit_types[i]:<7} {item_quantities[i]:<5} {item_unit_rates[i]:<8.2f} {item_discounts[i]:<8.2f} {item_totals[i]:.2f}")

    print("-" * 65)
    print(f"  Total Discount  : Rs {total_discount:.2f}")
    print(f"  GRAND TOTAL     : Rs {grand_total:.2f}")
    print("=" * 65)

    # Confirm and save
    save_confirm = input("\n  Confirm sale and generate invoice? [y/n]: ").strip().lower()
    if save_confirm != "y":
        print("  Sale cancelled.")
        return

    # Update stock for each item
    for i in range(len(item_names)):
        inventory.reduce_stock(item_names[i], item_tabs_total[i])

    # Write invoice to file
    invoice_file = get_invoice_filename()
    try:
        f = open(invoice_file, "w")
        f.write("=" * 65 + "\n")
        f.write("           MEDSTORE PVT. LTD. - SALES INVOICE\n")
        f.write("=" * 65 + "\n")
        f.write(f"Bill No  : {random.randint(100000, 999999)}\n")
        f.write(f"Customer : {customer_name}\n")
        f.write(f"Date     : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("-" * 65 + "\n")
        f.write(f"{'Medicine':<22} {'Brand':<15} {'Unit':<7} {'Qty':<5} {'Rate':<8} {'Disc':<8} {'Total'}\n")
        f.write("-" * 65 + "\n")

        for i in range(len(item_names)):
            f.write(f"{item_names[i]:<22} {item_brands[i]:<15} {item_unit_types[i]:<7} {item_quantities[i]:<5} {item_unit_rates[i]:<8.2f} {item_discounts[i]:<8.2f} {item_totals[i]:.2f}\n")

        f.write("-" * 65 + "\n")
        f.write(f"Total Discount  : Rs {total_discount:.2f}\n")
        f.write(f"GRAND TOTAL     : Rs {grand_total:.2f}\n")
        f.write("=" * 65 + "\n")
        f.write("   Thank you for purchasing from MedStore!\n")
        f.write("=" * 65 + "\n")
        f.close()
        print(f"\n  Invoice saved as: {invoice_file}")
    except Exception as e:
        print(f"\n  ERROR: Could not save invoice - {e}")

    print("\n  Sale completed successfully!")