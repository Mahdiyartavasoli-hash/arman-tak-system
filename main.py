import factory_managers
import web_tools

num_1 = factory_managers.CementBlockMachine("Arman_Tak_1")
num_2 = factory_managers.AsphaltMachine("Tarnama_2")

while True:
    user = input("please write number 1 - 3 to chose your user : ")
    if user == "1":
        amount_1 = int(input("How many kg CementBlockMachine you need? "))
        amount_2 = int(input("How many kg AsphaltMachine you need? "))
        final_1 = num_1.produce(amount_1)
        final_2 = num_2.produce(amount_2)
        print(final_1)
    elif user == "2":
        try:
            with open("data/production_logs.txt", "r", encoding="utf-8") as file:
                print(file.read())
        except FileNotFoundError:
            print("📭 No reports have been filed yet! Create one first.\n")
    elif user == "3":
        price = web_tools.get_btc_price()
        print(price)
    

