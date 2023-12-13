from sharkiq import get_ayla_api, OperatingModes, Properties, PowerModes


#get user sign in information 
#print('Enter Shark email address: ')
USERNAME = 'apsflora@gmail.com'
#print('Enter password: ')000
PASSWORD = 'Ryan1215$'

#sign in  using the ayla api
ayla_api = get_ayla_api(USERNAME, PASSWORD)
ayla_api.sign_in()

#message user saying sign-in successful
print('\nSign-in Succesful!')

#Choose which robot you would like create a schedule for
shark_vacs = ayla_api.get_devices()

device_names = [device.name for device in shark_vacs]

formatted_names = [f'\t{idx}: {name}' for idx, name in enumerate(device_names)]

print('Which robot would you like to schedule specific rooms to clean?\n' + '\n'.join(formatted_names))
robot_selection = input()
try:
    selected_idx = int(robot_selection)
    if 0 <= selected_idx < len(shark_vacs):
        shark = shark_vacs[selected_idx]
        print(f'You selected: {shark.name} (ID: {selected_idx})')
    else:
        print("Invalid selection. Please enter a valid number.")
except ValueError:
    print("Invalid input. Please enter a valid number.")

#reference for the robot name
shark_name = shark.name

#get all the rooms under the robot 
rooms = shark.get_room_list()


# create a schedule to clean specific rooms 
print('\nWhich rooms would you like to schedule ' + shark_name + ' to clean?')
print("\n".join([f'\t{idx}: {val}' for idx, val in enumerate(rooms)]))

selected_rooms = set()  # Initialize an empty set to store selected rooms

while True:
    selection = input("Enter the room number to select or 'done' to finish: ")
    if selection.lower() == 'done':
        break
    try:
        selection = int(selection)
        if 0 <= selection < len(rooms):
            if rooms[selection] not in selected_rooms:
                selected_rooms.add(rooms[selection])
                print(f"{rooms[selection]} has been selected.")
            else:
                print("You've already selected this room. Choose another room. Or enter 'done' to finish. ")
        else:
            print("Invalid room number. Please enter a valid room number.")
    except ValueError:
        print("Invalid input. Please enter a valid room number or 'done' to finish.")

#show user the slected rooms
print("You have selected the following rooms:")
for room in selected_rooms:
    print(room)

#ask user if they would like to start cleaning the slected rooms
print('Would like to have ' + shark_name + ' start cleaning? (Y/N)' )
reponse = input ()
if reponse == "y":
 shark.clean_rooms(selected_rooms)
else:
    exit()