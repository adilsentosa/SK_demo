from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms 
        
from .models import *

class KelasForm(ModelForm):
  class Meta:
    model = Kelas
    fields = '__all__'

class RuanganForm(ModelForm):
  class Meta:
    model = Ruangan
    fields = '__all__'

class JamForm(ModelForm):
  class Meta:
    model = Jam
    fields = '__all__'
    widgets = {
      'waktu_mulai': forms.TimeInput(attrs={'type': 'time'}),
      'waktu_selesai': forms.TimeInput(attrs={'type': 'time'}),
    }

class HariForm(ModelForm):
  class Meta:
    model = Hari
    fields = '__all__'

class MapelForm(ModelForm):
  class Meta:
    model = Mapel
    fields = '__all__'

class GuruForm(ModelForm):
  username = forms.CharField(max_length=150)
  email = forms.EmailField(required=True)
  password = forms.CharField(widget=forms.PasswordInput)

  class Meta:
    model = Guru
    fields = ['nama', 'telepon', 'mapel', 'alamat', 'jenis_kelamin', 'status']

  def save(self, commit=True):
    user = User.objects.create_user(
      username=self.cleaned_data['username'],
      email=self.cleaned_data['email'],
      password=self.cleaned_data['password']
    )
    guru = super().save(commit=False)
    guru.user = user
    if commit:
      user.save()
      guru.save()
    return guru

class TugasForm(ModelForm):
  class Meta:
    model = Tugas
    fields = '__all__'