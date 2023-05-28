with open('user_data.chnk', 'r') as f:
    lines = f.readlines()

for line in lines:
    if line.startswith('login'):
        login = line.split(': ')[1].strip()
    elif line.startswith('password'):
        password = line.split(': ')[1].strip()
    elif line.startswith('api'):
        api_key = line.split(': ')[1].strip()
    elif line.startswith('user'):
        user = line.split(': ')[1].strip()
    elif line.startswith('bot'):
        bot = line.split(': ')[1].strip()

print(login)
print(password)
print(api_key)
print(user)
print(bot)