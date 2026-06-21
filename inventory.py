import datetime
#This gives the item present in the inventory and also helps to update the stock after a sale or restock.
# FUNCTION: read all medicines from file
# returns a list of lists
# Each inner list = [name, brand, stock, rate-tab, rate-strip, tabs-per]
def read_medicines():
    medicines = []
    
    file = open("medicines.txt", "r")
    lines = file.readlines()
    file.close()
    
    return medicines

    for line in lines:
        line = line.strip()
        if line == "":
            continue  # if is nothing then continue to next line
        data = line.split(",")
        if len(data) == 6: #Splits the line into parts using commas
            medicines.append(data)

    return medicines
# function : Save all medicines back to file
def save_medicines(medicines):
    try:
        file = open("medicines.txt", "w")
        for med in medicines:
            line = med[0] + "," + med[1] + "," + med[2] + "," + med[3] + "," + med[4] + "," + med[5]
            file.write(line + "\n")
        file.close()
    except Exception as e:
        print("\n  ERROR: Could not save medicines.txt -", e)

# function: to show full inventory table.
def show_inventory():
    medicines = read_medicines()
    if len(medicines) == 0:
        print("\n There is no medicines  in inventory.")
        return
    print("\n" + "=" * 100)
    print(" MEDSTORE WHOLESALE SYSTEM-INVENTORY")
    print("=" * 100)
    #for alignment of the table we use f string and specify the width of each column using < and a number.
    print(f"  {'S.N.':<5} {'Medicine Name':<25} {'Brand':<18} {'Stock(Tabs)':<12} {'Rs/Tab':<8} {'Rs/Strip':<10} {'Tabs/Strip'}")
    print("-" * 100)

    count = 0
    for med in medicines:
        count = count + 1
        name      = med[0]
        brand     = med[1]
        stock     = med[2]
        rate_tab  = med[3]
        rate_strip= med[4]
        tabs_per  = med[5]

        print(f"  {count:<5} {name:<25} {brand:<18} {stock:<12} {rate_tab:<8} {rate_strip:<10} {tabs_per}")

    print("=" * 100)
    print(f"  Report Date   : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"  Total Medicines: {count}")
    print("=" * 100)

# function: search medicine by name, returns index or -1
def find_medicine(medicines, name):
    name = name.lower()
    for i in range(len(medicines)):
        if medicines[i][0].lower() == name:
            return i
    return -1

# function: Reduce stock after a sale
def reduce_stock(medicine_name, quantity_in_tabs):
    medicines = read_medicines()
    index = find_medicine(medicines, medicine_name)

    if index == -1:
        return False

    current_stock = int(medicines[index][2])
    if current_stock < quantity_in_tabs:
        return False

    medicines[index][2] = str(current_stock - quantity_in_tabs)
    save_medicines(medicines)
    return True

# function: to increase stock after restock
def increase_stock(medicine_name, quantity_in_tabs):
    medicines = read_medicines()
    index = find_medicine(medicines, medicine_name)

    if index == -1:
        return False

    current_stock = int(medicines[index][2])
    medicines[index][2] = str(current_stock + quantity_in_tabs)
    save_medicines(medicines)
    return True