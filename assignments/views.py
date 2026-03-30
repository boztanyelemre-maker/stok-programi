from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Assignment
from .forms import AssignmentForm


@login_required
def assignment_list(request):
    assignments = Assignment.objects.select_related('project', 'product', 'asset').all()
    q = request.GET.get('q', '')
    if q:
        assignments = assignments.filter(
            Q(assigned_to_name__icontains=q) | Q(tc_kimlik__icontains=q) |
            Q(product__name__icontains=q)
        )
    status = request.GET.get('status')
    if status:
        assignments = assignments.filter(status=status)
    paginator = Paginator(assignments, 20)
    page = request.GET.get('page')
    assignments = paginator.get_page(page)
    return render(request, 'assignments/assignment_list.html',
                  {'assignments': assignments, 'q': q})


@login_required
def assignment_create(request):
    if request.method == 'POST':
        form = AssignmentForm(request.POST)
        if form.is_valid():
            assignment = form.save(commit=False)
            assignment.created_by = request.user
            assignment.save()
            messages.success(request, 'Zimmet olusturuldu.')
            return redirect('assignment_list')
    else:
        form = AssignmentForm()
    return render(request, 'assignments/assignment_form.html',
                  {'form': form, 'title': 'Yeni Zimmet'})


@login_required
def assignment_edit(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.method == 'POST':
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Zimmet guncellendi.')
            return redirect('assignment_list')
    else:
        form = AssignmentForm(instance=assignment)
    return render(request, 'assignments/assignment_form.html',
                  {'form': form, 'title': 'Zimmet Duzenle'})


@login_required
def assignment_return(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.method == 'POST':
        from django.utils import timezone
        assignment.status = 'returned'
        assignment.return_date = timezone.now().date()
        assignment.save()
        messages.success(request, 'Zimmet iade edildi.')
    return redirect('assignment_list')


@login_required
def assignment_delete(request, pk):
    assignment = get_object_or_404(Assignment, pk=pk)
    if request.method == 'POST':
        assignment.delete()
        messages.success(request, 'Zimmet silindi.')
    return redirect('assignment_list')
