
from features.models import *


# @login_required
# def download_qr_code(request, event_credentials, secret_token):
#     event = get_object_or_404(Event, event_credentials=urlsafe_base64_decode(event_credentials).decode(),
#                                secret_token=urlsafe_base64_decode(secret_token).decode())
    
#     company = Company.objects.all().order_by('-created').first()
#     # here is the company logo iwant in the center of qr code 
#     logo = company.logo

#     qr = qrcode.QRCode(
#         version=1,
#         error_correction=qrcode.constants.ERROR_CORRECT_L,
#         box_size=10,
#         border=4,
#     )
#     event_url = f"{request.scheme}://{request.get_host()}{reverse('event', args=[event.event_credentials, event.secret_token])}"

#     qr.add_data(event_url)
#     qr.make(fit=True)

#     buffer = BytesIO()
#     qr_img = qr.make_image(fill_color="black", back_color="white")
#     qr_img.save(buffer, format="PNG")
#     image_data = buffer.getvalue()

#     response = HttpResponse(image_data, content_type='image/png')
#     response['Content-Disposition'] = f'attachment; filename="{event.event_name}_qr_code.png"'

#     return response


from io import BytesIO
from PIL import Image, ImageDraw
import qrcode
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.utils.http import urlsafe_base64_decode
from .models import Event
from django.contrib.auth.decorators import login_required

@login_required
def download_qr_code(request, event_credentials, secret_token):
    event = get_object_or_404(Event, event_credentials=urlsafe_base64_decode(event_credentials).decode(),
                               secret_token=urlsafe_base64_decode(secret_token).decode())
    
    company = Company.objects.all().order_by('-created').first()
    logo_path = company.qr_logo.path  # Assuming 'qr_logo' is an ImageField in your Company model

    # Generate QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    event_url = f"{request.scheme}://{request.get_host()}{reverse('event', args=[event.event_credentials, event.secret_token])}"
    qr.add_data(event_url)
    qr.make(fit=True)

    # Create a new image with white background
    image_size = 300
    new_image = Image.new("RGB", (image_size, image_size), (255, 255, 255))
    
    # Initialize the drawing context
    draw = ImageDraw.Draw(new_image)

    # Draw the QR code on the image
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_img = qr_img.resize((image_size, image_size))
    new_image.paste(qr_img, (0, 0))

    # Open the logo image
    logo = Image.open(logo_path)

    # Resize the logo
    logo = logo.resize((100, 100), Image.ANTIALIAS)

    # Calculate the position to center the logo on the image
    logo_pos = ((new_image.size[0] - logo.size[0]) // 2, (new_image.size[1] - logo.size[1]) // 2)

    # Paste the logo on the image with transparency
    new_image.paste(logo, logo_pos, logo)

    # Save the image to a BytesIO buffer
    buffer = BytesIO()
    new_image.save(buffer, format="PNG")
    image_data = buffer.getvalue()

    # Create a response with the image data
    response = HttpResponse(image_data, content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename="{event.event_name}_qr_code.png"'

    return response


