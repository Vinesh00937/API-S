import secrets

# Create 3 different keys for 3 different testers
key1 = secrets.token_hex(16)
key2 = secrets.token_hex(16)
key3 = secrets.token_hex(16)

# Save the keys only in the .env file on your own computer
# This file must not go into a public repo
f = open(".env", "w")
f.write("API_KEYS=" + key1 + "," + key2 + "," + key3)
f.close()

print("consumer_1:", key1)
print("consumer_2:", key2)
print("consumer_3:", key3)
print("Keys have been saved in .env. Share them with testers privately only.")
