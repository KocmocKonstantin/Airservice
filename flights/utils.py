import re

def extract_passenger_name(text):
    match = re.search(r"Пассажир:\s+([A-ZА-Я ]+)", text)
    return match.group(1).strip() if match else "Unknown"

def extract_flight_number(text):
    match = re.search(r"Рейс:\s+(\w+\d+)", text)
    return match.group(1).strip() if match else "Unknown"

def extract_departure_city(text):
    match = re.search(r"Вылет из:\s+([A-ZА-Я ]+)", text)
    return match.group(1).strip() if match else "Unknown"

def extract_arrival_city(text):
    match = re.search(r"Прилет в:\s+([A-ZА-Я ]+)", text)
    return match.group(1).strip() if match else "Unknown"

def extract_departure_time(text):
    match = re.search(r"Время вылета:\s+(\d{2}:\d{2})", text)
    return match.group(1).strip() if match else "Unknown"

def extract_arrival_time(text):
    match = re.search(r"Время прилета:\s+(\d{2}:\d{2})", text)
    return match.group(1).strip() if match else "Unknown"