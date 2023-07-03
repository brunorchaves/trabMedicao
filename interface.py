import serial
import matplotlib.pyplot as plt
from collections import deque

# Initialize serial connection
arduino = serial.Serial('COM5', 115200)  # Replace 'COM1' with the appropriate port

# Define the number of data points to plot
max_data_points = 100

# Initialize data buffers
current_data = deque(maxlen=max_data_points)
voltage_data = deque(maxlen=max_data_points)
lux_data = deque(maxlen=max_data_points)
temp_data = deque(maxlen=max_data_points)

# Initialize the plot
plt.ion()  # Enable interactive mode
fig, axs = plt.subplots(4, 1, figsize=(8, 12))

# Set plot labels and titles
axs[0].set_ylabel('Current')
axs[0].set_title('Real-time Signal Plot')
axs[1].set_ylabel('Voltage')
axs[2].set_ylabel('Lux')
axs[3].set_ylabel('Temperature')
axs[3].set_xlabel('Time')

# Start reading and plotting data
while True:
    # Read data from Arduino
    data = arduino.readline().decode('utf-8').strip().split(' ')
    if len(data) != 4:
        continue  # Skip invalid data
    current, voltage, lux, temp = map(int, data)

    # Update data buffers
    current_data.append(current)
    voltage_data.append(voltage)
    lux_data.append(lux)
    temp_data.append(temp)

    # Clear the current axes
    for ax in axs:
        ax.cla()

    # Plot the data
    axs[0].plot(current_data, 'b-', label='Current')
    axs[1].plot(voltage_data, 'g-', label='Voltage')
    axs[2].plot(lux_data, 'r-', label='Lux')
    axs[3].plot(temp_data, 'm-', label='Temperature')

    # Set plot limits
    for ax in axs:
        ax.set_xlim(0, max_data_points)
        ax.legend()

    # Draw the plot
    plt.tight_layout()
    plt.draw()
    plt.pause(0.01)
