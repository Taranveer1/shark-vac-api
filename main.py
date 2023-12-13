from sharkiq import get_ayla_api, OperatingModes, Properties, PowerModes

USERNAME = 'example@email.com'
PASSWORD = 'password$'

ayla_api = get_ayla_api(USERNAME, PASSWORD)
ayla_api.sign_in()

shark_vacs = ayla_api.get_devices()
shark = shark_vacs[0]
print(shark)

rooms = shark.get_room_list()

selected_rooms = []

while True:
    print('Selected rooms: ' + (", ".join(selected_rooms) if len(selected_rooms) > 0 else "<None>" ))
    print('Available rooms: ' + (", ".join(rooms)))
    print('Enter the room number you would like to add to the cleaning list: ')
    print("\n".join([f'\t{idx}: {val}' for idx, val in enumerate(rooms)]))
    print('\tc: Start Cleaning\n\nEnter your Selection: ')
    selection = input()
    if selection == 'c':
        shark.clean_rooms(selected_rooms)
        break
    else:
        try:
            selected_rooms.append(rooms[int(selection)])
            print('\n\n')
        except:
            print('\n🚨🚨 Oops, i didn\'t get that. Make sure you input a valid room index or the character "c" 🚨🚨')