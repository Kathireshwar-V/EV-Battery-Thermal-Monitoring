# External IoT-Based Predictive Thermal Stress Monitoring System for EV Batteries

## Overview

This project is an IoT-based predictive thermal monitoring system designed to improve EV battery safety using external temperature sensing and Thermal Stress Index (TSI) prediction.  
The system continuously monitors battery surface temperature and predicts overheating risk using rate-of-temperature-rise analysis, then triggers local and cloud-based alerts.

## Features

- Real-time battery temperature monitoring  
- Thermal Stress Index (TSI) calculation  
- Predictive overheating detection (Safe / Warning / Danger states)  
- LED and buzzer alerts  
- LCD display showing live status  
- Cloud monitoring and data logging using ThingSpeak  
- Offline-first safety operation (local alerts work even without internet)

## Technologies Used

- Python (Raspberry Pi OS)  
- Raspberry Pi 4  
- DS18B20 temperature sensor  
- ThingSpeak (cloud dashboard)  
- MQTT / HTTP for data upload  
- Basic IoT and embedded systems concepts

## Hardware Components

- Raspberry Pi 4  
- DS18B20 temperature sensor (for battery surface temperature)  
- LEDs (status indication)  
- Buzzer (audio alerts)  
- 16x2 LCD display (system status)  
- Connecting wires, resistors, EV battery pack (test setup)

## System Workflow

1. Read temperature from the DS18B20 sensor attached to the EV battery surface.  
2. Calculate the rate of temperature rise over time.  
3. Compute the Thermal Stress Index (TSI) based on temperature behavior.  
4. Classify battery status as Safe / Warning / Danger and trigger LED, buzzer, and LCD alerts.  
5. Upload temperature and TSI data to ThingSpeak for remote monitoring and visualization.

## Performance Metrics

- Response time: 180 ms  
- Processing speed: 1.2 Hz (updates per second)  
- Low false-positive rate for overheating detection  
- Reliable real-time alerts in both local and cloud modes

## Repository Structure

- `Ev-code.py` – Main Python script running on Raspberry Pi  
- `Sample Data.csv` – Example dataset of temperature and TSI values  
- `Implementation_details.pdf` – Detailed implementation document  
- `Invention_overview.pdf` – High-level project and innovation overview  
- `Technical_description.pdf` – Technical explanation of system design and TSI logic  
- `Safe Mode.png`, `Warning Mode.png`, `Danger Mode (1).png` – Output screenshots  
- `Raspberry Pi setup.png`, `Running Circuit.png`, `LCD Display.png`, `ThingSpeak Dashboard.png` – Hardware and dashboard images

## How to Run

1. **Clone the repository**

```bash
git clone https://github.com/Kathireshwar-V/EV-Battery-Thermal-Monitoring.git
cd EV-Battery-Thermal-Monitoring
```

2. **Install required Python libraries**

Install the libraries used in `Ev-code.py` (for example):

```bash
pip install RPi.GPIO requests
```

(Add any other libraries you have used, such as `paho-mqtt`, `numpy`, etc.)

3. **Hardware setup**

- Connect DS18B20 sensor to Raspberry Pi GPIO pins as per your circuit diagram.  
- Connect LEDs, buzzer, and LCD to the appropriate GPIO pins.  
- Configure ThingSpeak channel and update the API key and channel ID in `Ev-code.py`.

4. **Run the code**

```bash
python Ev-code.py
```

The script will start reading temperature, computing TSI, updating the LCD, activating alerts, and sending data to ThingSpeak.

## Project Documentation

Detailed reports and explanations are available in the PDF files in this repository:

- `Implementation_details.pdf`  
- `Invention_overview.pdf`  
- `Technical_description.pdf`

## Demo

Add your demo video link here (Google Drive / YouTube):

`[Demo Video Link]`

## Future Enhancements

- AI-based battery health and lifetime prediction  
- Mobile app integration for user notifications  
- GPS-based emergency tracking in case of thermal runaway  
- Custom PCB design for compact deployment

## Team Members

- Kathireshwar V (Myself)
- Shakeer Ahmed K  
- M Gunal  
- Giridharan M G
