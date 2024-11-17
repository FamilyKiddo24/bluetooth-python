# simple inquiry example
import bluetooth
import psutil
from pywinusb import hid
from tabulate import tabulate
import cv2
from datetime import datetime

print('''
______ _     _   _ _____ _____ _____ _____  _____ _____ _   _  ________   _______ _   _ _____ _   _ 
| ___ \ |   | | | |  ___|  ___|_   _|  _  ||  _  |_   _| | | | | ___ \ \ / /_   _| | | |  _  | \ | |
| |_/ / |   | | | | |__ | |__   | | | | | || | | | | | | |_| | | |_/ /\ V /  | | | |_| | | | |  \| |
| ___ \ |   | | | |  __||  __|  | | | | | || | | | | | |  _  | |  __/  \ /   | | |  _  | | | | . ` |
| |_/ / |___| |_| | |___| |___  | | \ \_/ /\ \_/ / | | | | | | | |     | |   | | | | | \ \_/ / |\  |
\____/\_____/\___/\____/\____/  \_/  \___/  \___/  \_/ \_| |_/ \_|     \_/   \_/ \_| |_/\___/\_| \_/
                                                                                                    
                                                                                                    
''')

# Discover nearby Bluetooth devices
nearby_devices = bluetooth.discover_devices(lookup_names=True)

# List to store device data
device_list = []

# Add Bluetooth devices to the device list
for idx, (addr, name) in enumerate(nearby_devices, start=1):
    device_list.append([idx, name, 'Bluetooth'])

# List all connected devices (USB storage)
for idx, device in enumerate(psutil.disk_partitions(), start=1):
    if 'usb' in device.opts.lower():
        device_list.append([idx, device.device, 'USB Storage'])

# Use pywinusb to detect USB HID devices (like mice, keyboards)
def hid_device_found(device):
    # Append the HID device name and type
    name = device.product_name if device.product_name else "Unknown HID Device"
    device_list.append([len(device_list) + 1, name, 'USB HID'])

# Scan for HID devices (e.g., USB keyboards, mice)
all_devices = hid.HidDeviceFilter().get_devices()
for device in all_devices:
    hid_device_found(device)

# Display total number of devices found
print(f"\nFound {len(device_list)} Devices:")

# Display the device list in a table format
print(tabulate(device_list, headers=["Number", "Name", "Type"], tablefmt="grid"))

def take_photo():
    try:
        # Initialize camera
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not access camera")
            return

        # Capture frame
        ret, frame = cap.read()
        if ret:
            # Generate timestamp for filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"photo_{timestamp}.jpg"
            
            # Save the photo
            cv2.imwrite(filename, frame)
            print(f"Photo saved as {filename}")
        
        # Release camera
        cap.release()
        cv2.destroyAllWindows()
    except Exception as e:
        print(f"Error taking photo: {e}")

# Ask user to input a number to select a device
try:
    device_number = int(input("Enter the number corresponding to the device you want to see: "))

    # Check if the number is valid
    if 1 <= device_number <= len(device_list):
        selected_device = device_list[device_number - 1]
        print(f"\nSelected Device:\nName: {selected_device[1]}\nType: {selected_device[2]}")
        
        # If it's a Bluetooth device, offer to take a photo
        if selected_device[2] == 'Bluetooth':
            take_photo_input = input("Would you like to take a photo with this device? (y/n): ")
            if take_photo_input.lower() == 'y':
                take_photo()
    else:
        print("Invalid device number. Please enter a valid number from the list.")
except ValueError:
    print("Please enter a valid number.")