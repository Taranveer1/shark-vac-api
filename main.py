from sharkiq import get_ayla_api, OperatingModes, Properties, PowerModes
import datetime
import time
#get user sign in information 
print('Enter Shark email address: ')
USERNAME = input()
print('Enter password: ')
PASSWORD = input()

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

# Prompt user to enter the scheduled time
while True:
    try:
        scheduled_time = input("Enter the scheduled time in HH:MM format (24-hour clock): ")
        scheduled_time = datetime.datetime.strptime(scheduled_time, "%H:%M")
        break
    except ValueError:
        print("Invalid time format. Please enter the time in HH:MM format.")

# Prompt user to select specific days for the schedule
days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
print("Select the days for the schedule (e.g., 1 3 5 for Monday, Wednesday, Friday):")
for idx, day in enumerate(days_of_week, start=1):
    print(f"{idx}: {day}")
selected_days = []
while True:
    try:
        day_selection = input("Enter the numbers of the days you want to schedule (space-separated): ")
        day_selection = [int(x) for x in day_selection.split()]
        selected_days = [days_of_week[idx - 1] for idx in day_selection if 1 <= idx <= 7]
        if selected_days:
            break
        else:
            print("Invalid day selection. Please select at least one day.")
    except ValueError:
        print("Invalid input. Please enter the numbers of the days you want to schedule.")

# ...

# Now, you can use 'scheduled_time' and 'selected_days' in your scheduling logic
print(f"You have scheduled {shark_name} to clean the selected rooms at {scheduled_time.strftime('%H:%M')} on {', '.join(selected_days)}.")

#send the robot to clean the desired time
while True:
    current_time = datetime.datetime.now()
    current_day = days_of_week[current_time.weekday()]

    if current_time.strftime("%H:%M") == scheduled_time.strftime("%H:%M") and current_day in selected_days:
        # It's time to clean on the selected day
        print(f"Cleaning started at {current_time.strftime('%H:%M')} on {current_day}.")
        shark.clean_rooms(selected_rooms)
    
    # Sleep for a while before checking again (adjust the sleep duration as needed)
    time.sleep(60)  # Sleep for 1 minute before checking again



