from pwdlib import PasswordHash

# from main import create_access_token

# token = create_access_token({'sub': 1})
# print(token)

password_hash = PasswordHash.recommended()

def hash_password(password):

    return password_hash.hash(password)


def verify_password(password, hashed_password)-> bool:
    
    return password_hash.verify(password, hashed_password)

print(hash_password('psword1234'))

if verify_password("psword1234", '$argon2id$v=19$m=65536,t=3,p=4$Isirwj6hHmnDkflkk1MlBQ$vIrbNpAnAMlR7BeGwkX4qVTw2hHpqHBWRwfmzpJTIqU'):
    print('password match')
    
