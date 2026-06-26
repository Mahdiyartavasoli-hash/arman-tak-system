import factory_managers
import web_tools
import sqlite3

num_1 = factory_managers.CementBlockMachine("Arman_Tak_1")
num_2 = factory_managers.AsphaltMachine("Tarnama_2")

while True:
    print("\n--- Arman Tak Factory Management System ---")
    print("1. Register New Production")
    print("2. View Production Reports (Database)")
    print("3. Check Bitcoin Live Price")
    print("4. Exit")
    
    user = input("Please select an option (1-4): ")
    
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
        price = web_tools.get_btc_price()
        print(price)
        
    elif user == "4":
        print("Exiting system. Have a great day! 👋")
        break



# import sqlite3

# def get_machine_history(target_machine):
#     connection = sqlite3.connect("factory.db")
#     cursor = connection.cursor()
#     cursor.execute("SELECT * FROM production WHERE machine_name = ?", (target_machine,))
#     rows = cursor.fetchall()
#     if not rows:
#                 print("📭 No production reports found in database!")
#     else:
#         print("\n📋 --- Database Production Logs ---")
#         for row in rows:
#             print(f"ID: {row[0]} | Machine: {row[1]} | Amount: {row[2]} kg | Date: {row[3]}")
#     connection.close()

# get_machine_history("Arman_Tak_1")