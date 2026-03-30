from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Project, Warehouse, Location, Room, GeneralSettings
from .forms import ProjectForm, WarehouseForm, LocationForm, RoomForm, GeneralSettingsForm


@login_required
def project_settings(request):
    projects = Project.objects.all()
    q = request.GET.get('q', '')
    if q:
        projects = projects.filter(name__icontains=q)
    paginator = Paginator(projects, 20)
    page = request.GET.get('page')
    projects = paginator.get_page(page)
    form = ProjectForm()
    return render(request, 'parameters/project_settings.html', {
        'projects': projects, 'form': form, 'q': q
    })


@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proje eklendi.')
    return redirect('project_settings')


@login_required
def project_edit(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proje guncellendi.')
    return redirect('project_settings')


@login_required
def project_delete(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Proje silindi.')
    return redirect('project_settings')


@login_required
def location_settings(request):
    projects = Project.objects.filter(is_active=True)
    warehouses = Warehouse.objects.select_related('project').all()
    locations = Location.objects.select_related('warehouse').all()
    rooms = Room.objects.select_related('location').all()

    wh_form = WarehouseForm()
    loc_form = LocationForm()
    room_form = RoomForm()

    return render(request, 'parameters/location_settings.html', {
        'projects': projects, 'warehouses': warehouses,
        'locations': locations, 'rooms': rooms,
        'wh_form': wh_form, 'loc_form': loc_form, 'room_form': room_form
    })


@login_required
def warehouse_create(request):
    if request.method == 'POST':
        form = WarehouseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Depo/Bina eklendi.')
    return redirect('location_settings')


@login_required
def warehouse_delete(request, pk):
    obj = get_object_or_404(Warehouse, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Depo/Bina silindi.')
    return redirect('location_settings')


@login_required
def location_create(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lokasyon eklendi.')
    return redirect('location_settings')


@login_required
def location_delete(request, pk):
    obj = get_object_or_404(Location, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Lokasyon silindi.')
    return redirect('location_settings')


@login_required
def room_create(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Oda/Alan eklendi.')
    return redirect('location_settings')


@login_required
def room_delete(request, pk):
    obj = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, 'Oda/Alan silindi.')
    return redirect('location_settings')


@login_required
def general_settings(request):
    settings = GeneralSettings.get_settings()
    if request.method == 'POST':
        form = GeneralSettingsForm(request.POST, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, 'Genel ayarlar guncellendi.')
            return redirect('general_settings')
    else:
        form = GeneralSettingsForm(instance=settings)
    return render(request, 'parameters/general_settings.html', {'form': form})


@login_required
def api_locations(request):
    warehouse_id = request.GET.get('warehouse_id')
    locs = Location.objects.filter(warehouse_id=warehouse_id, is_active=True).values('id', 'name')
    return JsonResponse(list(locs), safe=False)


@login_required
def api_rooms(request):
    location_id = request.GET.get('location_id')
    rooms = Room.objects.filter(location_id=location_id, is_active=True).values('id', 'name')
    return JsonResponse(list(rooms), safe=False)
