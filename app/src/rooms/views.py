import csv
from io import TextIOWrapper
import json

from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.template import Context, loader
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_http_methods
from django.views.decorators.vary import vary_on_cookie

from conferences.models import UserPreferences, Zosia
from rooms.forms import UploadFileForm
from rooms.models import Room
from rooms.serializers import room_to_dict, user_to_dict


# Cache hard (15mins)
@cache_page(60 * 15)
@vary_on_cookie
@login_required
@require_http_methods(['GET'])
def index(request):
    # Return HTML w/ rooms layout
    try:
        zosia = Zosia.objects.get(active=True)
    except Zosia.DoesNotExist:
        messages.error(request, _('There is no active conference'))
        return redirect(reverse('index'))

    try:
        preferences = UserPreferences.objects.get(zosia=zosia, user=request.user)
    except UserPreferences.DoesNotExist:
        messages.error(request, _('Please register first'))
        return redirect(reverse('user_zosia_register', kwargs={'zosia_id': zosia.pk}))

    paid = preferences.payment_accepted
    if not paid:
        messages.error(request, _('Your payment must be accepted first'))
        return redirect(reverse('accounts_profile'))

    if not zosia.is_rooming_open:
        messages.error(request, _('Room registration is not active yet'))
        return redirect(reverse('accounts_profile'))

    rooms = Room.objects.all_visible().prefetch_related('members').all()
    rooms = sorted(rooms, key=lambda x: x.pk)
    rooms_json = json.dumps(list(map(room_to_dict, rooms)))
    context = {
        'rooms': rooms,
        'rooms_json': rooms_json,
    }
    return render(request, 'rooms/index.html', context)


# GET
@vary_on_cookie
@login_required
@require_http_methods(['GET'])
def status(request):
    # Ajax
    # Return JSON view of rooms
    zosia = get_object_or_404(Zosia, active=True)
    user_prefs = get_object_or_404(UserPreferences, zosia=zosia, user=request.user)
    can_start_rooming = zosia.can_user_choose_room(user_prefs)
    rooms = Room.objects.all_visible().select_related('lock').prefetch_related('members').all()
    rooms_view = []

    for room in rooms:
        dic = room_to_dict(room)
        dic['is_owned_by'] = room.is_locked and room.lock.is_owned_by(
            request.user) and room.lock.password
        dic['people'] = list(map(user_to_dict, room.members.all()))
        dic['inside'] = request.user.pk in map(lambda x: x.pk, room.members.all())
        rooms_view.append(dic)

    view = {
        'can_start_rooming': can_start_rooming,
        'rooms': rooms_view,
    }
    return JsonResponse(view)


# https://docs.djangoproject.com/en/1.11/howto/outputting-csv/
# NOTE: Might not be the best approach - consider using csv module instead
def csv_response(data, template, filename='file'):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}.csv"'.format(filename)
    t = loader.get_template(template)
    c = Context({
        'data': data,
    })
    response.write(t.render(c))
    return response


@staff_member_required
@require_http_methods(['GET'])
def report(request):
    zosia = get_object_or_404(Zosia, active=True)
    rooms = Room.objects.all_visible().prefetch_related('members').all()
    rooms = sorted(rooms, key=lambda x: str(x))
    users = UserPreferences.objects.for_zosia(zosia).prefetch_related('user').all()
    users = sorted(users, key=lambda x: str(x))
    ctx = {
        'zosia': zosia,
        'rooms': rooms,
        'user_preferences': users
    }

    download = request.GET.get('download', False)
    if download == 'users':
        return csv_response(users, template='rooms/users.txt', filename='users')
    if download == 'rooms':
        return csv_response(rooms, template='rooms/rooms.txt', filename='rooms')

    return render(request, 'rooms/report.html', ctx)


def handle_uploaded_file(csvfile):
    rooms = []
    for row in csv.reader(csvfile, delimiter=','):
        name, desc, cap, hidden = row
        if name != "Name":
            rooms.append(
                Room(name=name, description=desc, capacity=cap, hidden=hidden))
    Room.objects.bulk_create(rooms)


@staff_member_required
@require_http_methods(['GET', 'POST'])
def import_room(request):
    zosia = get_object_or_404(Zosia, active=True)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(TextIOWrapper(request.FILES['file'].file,
                                               encoding=request.encoding))
            return HttpResponseRedirect(reverse('rooms_report'))
    else:
        form = UploadFileForm()
    return render(request, 'rooms/import.html', {'form': form})
