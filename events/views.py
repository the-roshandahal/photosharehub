from features.models import *
from django.http import HttpResponse

from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_str
import base64
from .models import *
from PIL import Image


from io import BytesIO
from PIL import Image
import qrcode
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode
from .models import Event
from django.contrib.auth.decorators import login_required



@login_required
def dashboard(request):
    logged_in_user = User.objects.get(username = request.user)
    events = Event.objects.filter(user=logged_in_user).annotate(num_photos=Count('folder__photo'),num_folders=Count('folder', distinct=True)).all()
    
    # logged_in_user = User.objects.get(username = request.user)
    # print(logged_in_user)
    # events = Event.objects.annotate(num_photos=Count('folder__photo'),num_folders=Count('folder', distinct=True)).all()
    
    current_site = get_current_site(request)

    event_qrcodes = []
    for event_instance in events:
        event_url = f"{request.scheme}://{current_site.domain}{reverse('event', args=[event_instance.event_credentials, event_instance.secret_token])}"

        # Encode the event credentials and secret token for use in the URL
        event_credentials_b64 = urlsafe_base64_encode(force_str(event_instance.event_credentials).encode())
        secret_token_b64 = urlsafe_base64_encode(force_str(event_instance.secret_token).encode())

        # Generate a single QR code for each event
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(event_url)
        qr.make(fit=True)

        buffer = BytesIO()
        qr_img = qr.make_image(fill_color="black", back_color="white")
        qr_img.save(buffer, format="PNG")
        qr_img_data = base64.b64encode(buffer.getvalue()).decode("utf-8")

        event_qrcodes.append({
            'event_instance': event_instance,
            'qr_img_data': qr_img_data,
            'event_url': event_url,
            'event_credentials_b64': event_credentials_b64,
            'secret_token_b64': secret_token_b64,
        })
    context = {
        'event_qrcodes': event_qrcodes,
    }

    return render(request, 'dashboard.html', context)

@login_required
def create_event(request):
    if request.method == 'POST':
        event_name = request.POST['event_name']
        location = request.POST['location']
        remarks = request.POST['remarks']
        event_obj = Event.objects.create(event_name = event_name, location = location, remarks = remarks)
        event_obj.save()
        return redirect('dashboard')
    else:
        return render(request,'create_event.html')
    



def event(request, event_credentials, secret_token):
    event = get_object_or_404(Event, event_credentials=event_credentials, secret_token=secret_token)
    folders = Folder.objects.filter(event=event).annotate(num_photos=Count('photo'))
    
    if SavedEvent.objects.filter(event_id= event.id).exists():
        fav = True
    else:
        fav = False
    for folder in folders:
        # Fetch the first three images inside the folder
        folder.first_three_photos = folder.photo_set.all()[:3]
    
    context = {
        'folders': folders,
        'event': event,
        'fav':fav
    }
    return render(request, 'event.html', context)




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
@login_required
def download_qr_code(request, event_credentials, secret_token):
    event = get_object_or_404(Event, event_credentials=urlsafe_base64_decode(event_credentials).decode(),
                               secret_token=urlsafe_base64_decode(secret_token).decode())
    
    company = Company.objects.all().order_by('-created').first()
    logo_path = company.qr_logo.path  # Assuming 'qr_logo' is an ImageField in your Company model
    event_url = f"{request.scheme}://{request.get_host()}{reverse('event', args=[event.event_credentials, event.secret_token])}"

    basewidth = 100
    
    # Resize the logo
    logo = Image.open(logo_path)
    wpercent = (basewidth / float(logo.size[0]))
    hsize = int((float(logo.size[1]) * float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)

    # Generate QR code
    qr = qrcode.QRCode(
        error_correction=qrcode.constants.ERROR_CORRECT_H
    )
    qr.add_data(event_url)
    qr.make(fit=True)

    # Create an image from the QR code
    qr_img = qr.make_image(fill_color="black", back_color="white").convert('RGB')

    # Calculate the position to center the logo on the QR code
    pos = ((qr_img.size[0] - logo.size[0]) // 2, (qr_img.size[1] - logo.size[1]) // 2)

    # Paste the logo on the QR code
    qr_img.paste(logo, pos)

    buffer = BytesIO()
    qr_img.save(buffer, format="PNG")
    image_data = buffer.getvalue()

    response = HttpResponse(image_data, content_type='image/png')
    response['Content-Disposition'] = f'attachment; filename="{event.event_name}_qr_code.png"'

    return response




@login_required
def delete_event(request, event_credentials):
    event = get_object_or_404(Event, event_credentials=event_credentials)
    event.delete()
    messages.success(request, 'Event and associated images deleted successfully.')
    return redirect('dashboard')

def upload_images(request, event_credentials):
    event = Event.objects.get(event_credentials=event_credentials)
    if request.method == 'POST':
        name = request.POST.get('name')
        folder_name = request.POST.get('folder_name')

        images = request.FILES.getlist('images')
        name = name.title()
        folder_name = folder_name.title()

        event_obj = Event.objects.get(event_credentials=event_credentials)

        folder, created = Folder.objects.get_or_create(event = event_obj, created_by=name, folder_name=folder_name)
        if request.user.is_authenticated:
            user = request.user
        else:
            user = None
        for image in images:
            Photo.objects.create(
                folder=folder,
                image=image,
                guest_name=name,
                uploaded_by = user
            )
        return redirect('folder_detail', folder_credentials=folder.folder_credentials)
    else:
        context = {
            'event': event,
        }
        return render(request, 'upload_images.html', context)


def folder_detail(request, folder_credentials):
    folder = get_object_or_404(Folder, folder_credentials=folder_credentials)
    photos = Photo.objects.filter(folder=folder)
    photo_count = photos.count()
    return render(request, 'folder_detail.html', {'folder': folder, 'photos': photos, 'photo_count':photo_count})



def save_event(request,event_credentials):
    event = Event.objects.get(event_credentials=event_credentials)
    if request.user.is_authenticated:
        user_obj = request.user
        user = User.objects.get(username=user_obj)
        if SavedEvent.objects.filter(event=event,user=user).exists():
            messages.success(request, 'Event already exists in favourites.')
        else:
            SavedEvent.objects.create(event=event,user=user)
            messages.success(request, 'Event saved successfully.')
        return redirect('event', event_credentials=event.event_credentials, secret_token= event.secret_token)
    else:
        messages.success(request, 'You must login to continue.')
        return redirect('event', event_credentials=event.event_credentials, secret_token= event.secret_token)

@login_required
def unsave_event(request,event_credentials):
    event = Event.objects.get(event_credentials=event_credentials)
    user_obj = request.user
    user = User.objects.get(username=user_obj)
    saved_event=SavedEvent.objects.get(event=event,user=user)
    saved_event.delete()
    messages.success(request, 'Event removed successfully.')
    return redirect('event', event_credentials=event.event_credentials, secret_token= event.secret_token)

@login_required
def saved_events(request, id):
    user = get_object_or_404(User, id=id)
    saved_events_data = SavedEvent.objects.filter(user=user)
    events_with_num_images = Event.objects.filter(savedevent__in=saved_events_data).annotate(num_images=Count('folder__photo'))

    context = {
        'saved_events_data': saved_events_data,
        'events_with_num_images': events_with_num_images,
    }
    return render(request, 'saved_events.html', context)

def all_images(request, event_credentials):
    event = Event.objects.get(event_credentials=event_credentials)
    folders = Folder.objects.filter(event=event)
    photos = Photo.objects.filter(folder__in=folders)
    photo_count = photos.count()
    return render(request, 'all_images.html', {'event':event, 'photos': photos, 'photo_count': photo_count})


