import json, os

with open('ContactBinds.json', 'r') as file:
    data = json.load(file)
    file.close()

for x in data:
    os.system("cls")
    while True:
        print(f"Set binding for: {x}")
        choice = input("0: None\n1: PS4 Controller\n2: Xbox 1 S Controller\n3: Left Joycon\n4: Right Joycon\n5: Joycon Pair\n>")
        os.system("cls")
        if choice == '0':
            data[x] = None
            break
        elif choice == '1':
            data[x] = "PS4 Controller"
            break
        elif choice == '2':
            data[x] = "Xbox One S Controller"
            break
        elif choice == '3':
            data[x] = "Nintendo Switch Joy-Con (L)"
            break
        elif choice == '4':
            data[x] = "Nintendo Switch Joy-Con (R)"
            break
        elif choice == '5':
            data[x] = "Nintendo Switch Joy-Con (L/R)"
            break
        else:
            print("Invalid Input")

with open('ContactBinds.json', 'w') as file:
    json.dump(data, file, ensure_ascii=False, indent=4)
    file.close()
print("updated data")
