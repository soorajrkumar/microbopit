# MicroBopIt

An interactive multiplayer game built for Microbit microcontrollers. Uses radio communication to send real-time challenges, track scores and declare a winner after 20 points. 

This project was designed to demonstrate microcontroller programming, usage of multiple sensors and output devices and real-time data processing.

## How It Works:

- **Server** assigns player IDs, sends challenges and tracks scores
- **Users** respond with physical inputs and receive immediate feedback
- The first player who reaches 20 points triggers a winner name entry
- The winner chooses initials of their choice and sends them via UART for logging and further analysis

## Requirements:

The following libraries must be installed:

- microbit
- radio
- music
- time
- OLED

## Future Improvements:

- Timeout for infinite loops
- Error handling for lost messages
- Restart option for faster gameplay resets

## Team:

- Abdullah Al Jebreen
- Ahmed Mohamed
- Igbunuoghene Omare
- Joshua Temple
- Leon Ghebre
- Millie Cartmail
- Sooraj Rajive Kumar