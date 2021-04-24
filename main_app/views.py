from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Dodger, Equipment, Photo
from .forms import TrainingForm

# Add the following import
from django.http import HttpResponse

import uuid
import boto3


S3_BASE_URL = 'https://s3-us-west-1.amazonaws.com/'
BUCKET = 'dodgercollector'


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


@login_required
def dodgers_index(request):
    dodgers = Dodger.objects.filter(user=request.user)
    return render(request, 'dodgers/index.html', {'dodgers': dodgers})


@login_required
def dodgers_detail(request, dodger_id):
    dodger = Dodger.objects.get(id=dodger_id)
    equipments_dodger_doesnt_have = Equipment.objects.exclude(
        id__in=dodger.equipments.all().values_list('id'))
    training_form = TrainingForm()
    return render(request, 'dodgers/detail.html', {
        'dodger': dodger, 'training_form': training_form,
        'equipments': equipments_dodger_doesnt_have
    })


@login_required
def add_training(request, dodger_id):
    form = TrainingForm(request.POST)
    if form.is_valid():
        new_training = form.save(commit=False)
        new_training.dodger_id = dodger_id
        new_training.save()
    return redirect('detail', dodger_id=dodger_id)


class DodgerCreate(LoginRequiredMixin, CreateView):
    model = Dodger
    fields = ['name', 'position', 'description', 'salary']
    success_url = '/dodgers/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class DodgerUpdate(UpdateView):
    model = Dodger
    fields = ['position', 'description', 'salary']


class DodgerDelete(DeleteView):
    model = Dodger
    success_url = '/dodgers/'

# Equipments views


def equipments_index(request):
    equipments = Equipment.objects.all()
    context = {'equipments': equipments}

    return render(request, 'equipment/index.html', context)


def equipment_detail(request, equipment_id):
    equipment = Equipment.objects.get(id=equipment_id)
    context = {
        'equipment': equipment
    }
    return render(request, 'equipment/detail.html', context)


@login_required
def assoc_equipment(request, dodger_id, equipment_id):
    # Note that you can pass a equipment's id instead of the whole object
    Dodger.objects.get(id=dodger_id).equipments.add(equipment_id)
    return redirect('detail', dodger_id=dodger_id)


@login_required
def dissoc_equipment(request, dodger_id, equipment_id):
    # Note that you can pass a equipment's id instead of the whole object
    Dodger.objects.get(id=dodger_id).equipments.remove(equipment_id)
    return redirect('detail', dodger_id=dodger_id)


class Create_Equipment(CreateView):
    model = Equipment
    fields = '__all__'


class Update_equipment(UpdateView):
    model = Equipment
    fields = ['color']


class Delete_equipment(DeleteView):
    model = Equipment
    success_url = '/equipments/'


@login_required
def add_photo(request, dodger_id):
    # photo-file will be the "name" attribute on the <input type="file">
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + \
            photo_file.name[photo_file.name.rfind('.'):]
        # just in case something goes wrong
        try:
            s3.upload_fileobj(photo_file, BUCKET, key)
            # build the full url string
            url = f"{S3_BASE_URL}{BUCKET}/{key}"
            # we can assign to dodger_id or dodger (if you have a dodger object)
            photo = Photo(url=url, dodger_id=dodger_id)
            photo.save()
        except:
            print('An error occurred uploading file to S3')
    return redirect('detail', dodger_id=dodger_id)


def signup(request):
    error_message = ''
    if request.method == 'POST':
        # This is how to create a 'user' form object
        # that includes the data from the browser
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # This will add the user to the database
            user = form.save()
            # This is how we log a user in via code
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    # A bad POST or a GET request, so render signup.html with an empty form
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)
