from security import hash_password , verify_password

my_pass = "secret123"

hashed = hash_password(my_pass)

is_correct = verify_password("secret123", hashed)
print("Is correct pass valid?", is_correct)


is_wrong = verify_password("wrong_pass", hashed)
print("Is wrong pass valid?", is_wrong)
