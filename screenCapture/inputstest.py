from inputs import devices, get_gamepad
for device in devices:
    print(device)
while True:
    events = get_gamepad()

    for event in events:
        print(event.code, event.state)
