from django.db import models

class Flight(models.Model):
    flight_number = models.CharField(max_length=10)
    departure = models.CharField(max_length=100)
    arrival = models.CharField(max_length=100)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.flight_number} from {self.departure} to {self.arrival}"


class Ticket(models.Model):
    passenger_name = models.CharField(max_length=100)
    flight_number = models.CharField(max_length=20)
    departure_city = models.CharField(max_length=100)
    arrival_city = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    pdf_file = models.FileField(upload_to='tickets/')
    
    def __str__(self):
        return f"{self.passenger_name} - {self.flight_number}"