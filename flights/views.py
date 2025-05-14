import io
import os

import fitz
import pytesseract
import requests
from PIL import Image
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

from .forms import TicketUploadForm
from .constants import (
    WEATHER_API_URL,
    SCOPES,
    REDIRECT_URI,
    CLIENT_SECRET_FILENAME,
)
from .models import Flight, Ticket
from .utils import (
    extract_arrival_city,
    extract_arrival_time,
    extract_departure_city,
    extract_departure_time,
    extract_passenger_name,
    extract_flight_number,
)

GOOGLE_CLIENT_SECRET_FILE = os.path.join(settings.BASE_DIR, 'flights', CLIENT_SECRET_FILENAME)


def flight_list(request):
    """
    View to display a list of all flights.

    Args:
        request: The HTTP request object.
    
    Returns:
        HttpResponse: Renders the list of flights on the flight_list template.
    """
    flights = Flight.objects.all()
    return render(request, 'flights/flight_list.html', {'flights': flights})


def parse_pdf(file_path):
    """
    Parses a PDF file and extracts both text and images using OCR.

    Args:
        file_path (str): The path to the PDF file to be parsed.
    
    Returns:
        str: The extracted text content from the PDF and images.
    """
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            text += pytesseract.image_to_string(image)
    return text


def ticket_upload(request):
    """
    Handles the ticket upload process.

    Args:
        request: The HTTP request object containing the uploaded file.
    
    Returns:
        HttpResponse: Redirects to the ticket detail page after successful upload.
    """
    if request.method == 'POST':
        form = TicketUploadForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            file_path = ticket.pdf_file.path

            text = parse_pdf(file_path)
            ticket.passenger_name = extract_passenger_name(text)
            ticket.flight_number = extract_flight_number(text)
            ticket.departure_city = extract_departure_city(text)
            ticket.arrival_city = extract_arrival_city(text)
            ticket.departure_time = extract_departure_time(text)
            ticket.arrival_time = extract_arrival_time(text)

            ticket.save()
            return redirect('ticket_detail', pk=ticket.pk)
    else:
        form = TicketUploadForm()
    return render(request, 'flights/upload_ticket.html', {'form': form})


def ticket_detail(request, pk):
    """
    Displays the details of a specific ticket.

    Args:
        request: The HTTP request object.
        pk (int): The primary key of the ticket to be displayed.
    
    Returns:
        HttpResponse: Renders the ticket details page with weather information.
    """
    ticket = get_object_or_404(Ticket, pk=pk)
    weather = get_weather(ticket.arrival_city)
    context = {
        'ticket': ticket,
        'flight_duration': ticket.arrival_time - ticket.departure_time,
        'weather': weather,
    }
    return render(request, 'flights/ticket_detail.html', context)


def get_weather(city):
    """
    Fetches weather information for a given city using the OpenWeather API.

    Args:
        city (str): The city name to fetch weather information for.
    
    Returns:
        dict: A dictionary containing the weather data (temperature and description).
    """
    api_key = settings.OPENWEATHER_API_KEY
    url = f"{WEATHER_API_URL}?q={city}&appid={api_key}&units=metric&lang=ru"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        temp = data['main']['temp']
        description = data['weather'][0]['description']
        return {'temperature': temp, 'description': description}
    else:
        return {'error': 'Failed to retrieve weather data'}


def calendar_auth(request):
    """
    Initiates the Google OAuth2 flow to authenticate the user.

    Args:
        request: The HTTP request object.
    
    Returns:
        HttpResponse: Redirects the user to Google's OAuth2 consent screen.
    """
    flow = Flow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRET_FILE,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    request.session['state'] = state
    return redirect(authorization_url)


def oauth2callback(request):
    """
    Handles the callback after user authorization during the OAuth2 flow.

    Args:
        request: The HTTP request object containing the authorization response.
    
    Returns:
        HttpResponse: Renders a success page with the created event details.
    """
    state = request.session['state']
    flow = Flow.from_client_secrets_file(
        GOOGLE_CLIENT_SECRET_FILE,
        scopes=SCOPES,
        state=state,
        redirect_uri=REDIRECT_URI
    )
    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)

    credentials = flow.credentials

    service = build('calendar', 'v3', credentials=credentials)

    event = {
        'summary': 'My Ticket',
        'location': 'Airport',
        'description': 'Details about my flight ticket.',
        'start': {
            'dateTime': '2025-05-02T10:00:00',
            'timeZone': 'Europe/Moscow',
        },
        'end': {
            'dateTime': '2025-05-02T12:00:00',
            'timeZone': 'Europe/Moscow',
        },
    }

    event_result = service.events().insert(calendarId='primary', body=event).execute()

    return render(request, 'flights/calendar_success.html', {'event': event_result})
# TEST COMMENT
