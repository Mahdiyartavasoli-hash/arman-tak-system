import factory_managers
import web_tools
import sqlite3

num_1 = factory_managers.CementBlockMachine("Arman_Tak_1")
num_2 = factory_managers.AsphaltMachine("Tarnama_2")

while True:
    print("\n--- Arman Tak Factory Management System ---")
    print("1. Register New Production")
    print("2. View Production Reports (Database)")
    print("3. Update Production")
    print("4. Delete Production Record 🗑️")  
    print("5. Check Bitcoin Live Price")
    print("6. Exit")
    
    user = input("Please select an option (1-6): ")
    
    if user == "1":
        amount_1 = int(input("How many kg CementBlockMachine you need? "))
        amount_2 = int(input("How many kg AsphaltMachine you need? "))
        final_1 = num_1.produce(amount_1)
        final_2 = num_2.produce(amount_2)
        print(final_1)
        print(final_2)
        
    elif user == "2":
        try:
            connection = sqlite3.connect("factory.db")
            cursor = connection.cursor()
            
            cursor.execute("SELECT * FROM production")
            rows = cursor.fetchall()
            
            if not rows:
                print("📭 No production reports found in database!")
            else:
                print("\n📋 --- Database Production Logs ---")
                for row in rows:
                    print(f"ID: {row[0]} | Machine: {row[1]} | Amount: {row[2]} kg | Date: {row[3]}")
            
            connection.close()
        except sqlite3.Error as error:
            print("❌ Database Error:", error)

    elif user == "3":
            print("\n🔧 --- Edit Production Record ---")
            m_name = input("Enter machine name (Arman_Tak_1 or Tarnama_2): ")
            try:
                new_amt = float(input("Enter correct production amount (kg): "))
            except ValueError:
                print("❌ Invalid amount! Please enter a number.")
                continue
            t_date = input("Enter production date (YYYY-MM-DD): ")
            
            success = factory_managers.update_machine_production(m_name, new_amt, t_date)
            if success:
                print("\n✅ Production database updated successfully!")
            else:
                print("\n❌ Failed to update record. Check details.")

    elif user == "4":
        print("\n🗑️ --- Delete Production Record ---")
        try:
            rec_id = int(input("Enter the ID of the record you want to delete: "))
        except ValueError:
            print("❌ Invalid ID! Please enter a number.")
            continue
            
        confirm = input(f"Are you sure you want to delete record ID {rec_id}? (yes/no): ")
        if confirm.lower() == "yes":
            success = factory_managers.delete_production_record(rec_id)
            if success:
                print(f"✅ Record ID {rec_id} has been deleted from database.")
            else:
                print("❌ Failed to delete record.")
        else:
            print("Deletion canceled.")
            

    elif user == "5":
        price = web_tools.get_btc_price()
        print(price)
        
    elif user == "6":
        print("Exiting system. Have a great day! 👋")
        break



