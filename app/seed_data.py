"""
seed_data.py

Contains mock data for seeding the sensor database.
"""

from datetime import datetime, timedelta
import random
from typing import List
from .models import SensorReading

def generate_seed_data() -> List[SensorReading]:
    """Generates 50 mock sensor readings."""
    data = []
    base_time = datetime.now()
    
    # Define some virtual sensors
    sensors = [
        {'id': 'S1', 'type': 'temperature', 'unit': 'C', 'base_val': 34.0, 'variance': 2.0},
        {'id': 'S2', 'type': 'humidity', 'unit': '%', 'base_val': 60.0, 'variance': 5.0},
        {'id': 'S3', 'type': 'weight', 'unit': 'kg', 'base_val': 45.0, 'variance': 0.5},
        {'id': 'S4', 'type': 'acoustics', 'unit': 'dB', 'base_val': 50.0, 'variance': 10.0},
        {'id': 'S5', 'type': 'co2', 'unit': 'ppm', 'base_val': 400.0, 'variance': 50.0}
    ]

    # Generate 10 readings for each of the 5 sensors (total 50)
    # Spaced 15 minutes apart
    for i in range(10):
        timestamp = base_time - timedelta(minutes=15 * (9 - i)) # Past to present
        
        for sensor in sensors:
            # Randomize value slightly
            val = sensor['base_val'] + random.uniform(-sensor['variance'], sensor['variance'])
            val = round(val, 2)
            
            reading = SensorReading(
                sensor_id=sensor['id'],
                insert_timestamp=timestamp,
                type=sensor['type'],
                value=val,
                unit=sensor['unit'],
                upload_freq='15min'
            )
            data.append(reading)
            
    return data

SEED_DATA: List[SensorReading] = generate_seed_data()
