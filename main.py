import sqlite3
import factory_managers  
import web_tools
# Assuming num_1 and num_2 are instantiated somewhere here, for example:
num_1 = factory_managers.CementBlockMachine("Arman_Tak_1")
num_2 = factory_managers.AsphaltMachine("Arman_Tak_2")

while True:
    print("""
        --- 🏗️ ARMAN TAK Factory Management System ---
        1. Log Production for Machines
        2. View All Production Logs
        3. Update Production Record
        4. Delete Production Record
        5. Report: High Production Records
        6. Report: Production Sorted by Highest Amount
        7. Report: Machine Production Analytics (Total & Average)
        8. Report: Max & Min Production Records
        9. Report: Total Production Count
        10. Live Bitcoin Price
        0. Exit
        """)
    
    user = input("Please select an option (0-9): ")
    

    if user == "1":
        try:
            amount_1 = int(input("How many kg CementBlockMachine you need? "))
            amount_2 = int(input("How many kg AsphaltMachine you need? "))
            
            final_1 = num_1.produce(amount_1)
            final_2 = num_2.produce(amount_2)
            
            print(final_1)
            print(final_2)
        except ValueError:
            print("❌ Invalid amount! Please enter a valid number.")
        

    elif user == "2":
        try:
            connection = sqlite3.connect("factory.db")
            cursor = connection.cursor()
            
            cursor.execute("SELECT * FROM production")
            rows = cursor.fetchall()
            
            if not rows:
                print("🚨 No production reports found in database!")
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
        print("\n📊 --- Delete Production Record ---")
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
        print("\n📊 --- High Production Report ---")
        machine_name = input("Enter machine name (e.g., Arman_Tak_1): ")
        try:
            min_amount = int(input("Enter minimum production amount (kg): "))
        except ValueError:
            print("❌ Invalid amount! Please enter a number.")
            continue
            
        records = factory_managers.get_high_production(machine_name, min_amount)
        
        if not records:
            print("🚨 No records found matching the criteria!")
        else:
            print(f"\n📊 Records above {min_amount} kg for {machine_name}:")
            for row in records:
                print(f"ID: {row[0]} | Machine: {row[1]} | Amount: {row[2]} kg | Date: {row[3]}")


    elif user == "6":
        print("\n📊 --- Production Sorted by Highest Amount ---")
        machine_name = input("Enter machine name (e.g., Arman_Tak_1): ")
        
        records = factory_managers.get_ordered_production(machine_name)
        
        if not records:
            print("🚨 No records found for this machine!")
        else:
            print(f"\n🔝 {machine_name} records from highest to lowest production:")
            for row in records:
                print(f"ID: {row[0]} | Machine: {row[1]} | Amount: {row[2]} kg | Date: {row[3]}")


    elif user == "7":
        print("\n📊 --- Machine Production Analytics ---")
        machine_name = input("Enter machine name (e.g., Arman_Tak_1): ")
            
        analytics = factory_managers.get_machine_analytics(machine_name)
            
        total_prod = analytics[0]
        avg_prod = analytics[1]
            
        print(f"\n📊 Performance Metrics for {machine_name}:")
        print(f"💰 Total Production: {total_prod:,} kg") 
        print(f"🧮 Average Production: {avg_prod:,.2f} kg") 


    elif user == "8":
        print("\n📊 --- Machine MAX & MIN Analytics ---")
    
        machine_name = input("Enter machine name (e.g., Arman_Tak_1): ")
            
        extremes = factory_managers.get_machine_extremes(machine_name)
            
        max_prod = extremes[0]
        min_prod = extremes[1]
            
        print(f"\n📊 Performance Metrics for {machine_name}:")
        print(f" MAX Production: {max_prod:,} kg") 
        print(f" MIN Production: {min_prod:,} kg")


    elif user == "9":
            print("\n📊 --- Total Production Count ---")
        
            machine_name = input("Enter machine name (e.g., Arman_Tak_1): ")
                        
            total_runs = factory_managers.get_machine_production_count(machine_name)
                
            print(f"\n📊 Total Production for {machine_name}:")
            print(f"🔢 Total Production Log Count: {total_runs:,} times")

    elif user == "10":
        print("\n🪙 --- Fetching Live Bitcoin Price ---")
        price = web_tools.get_btc_price()
        print(f"Current BTC Price: {price}")           
        

    elif user == "0":
        print("Exiting system. Have a great day! 👋")
        break
        
    else:
        print("❌ Invalid option! Please select between 0 and 10.")
