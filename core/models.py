from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission, User

# class User(AbstractUser):
#   ROLE_CHOICES = (
#     ('admin', 'Admin'),
#     ('guru', 'Guru'),
#   )
#   role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='guru')
#   # groups = models.ManyToManyField(Group, verbose_name='groups', blank=True, related_name='user_set')
#   # permissions = models.ManyToManyField(Permission, verbose_name='user permissions', blank=True, related_name='user_set')

class Kelas(models.Model):
  nama_kelas = models.CharField(max_length=50)
  
  def __str__(self):
    return self.nama_kelas

class Ruangan(models.Model):
  nama_ruangan = models.CharField(max_length=50)
  kelas = models.ForeignKey(Kelas, on_delete=models.SET_NULL, null=True)
  jenis = models.CharField(max_length=50, null=True)
  
  def __str__(self):
    return self.nama_ruangan

class Jam(models.Model):
  waktu_mulai = models.TimeField()
  waktu_selesai = models.TimeField()
  
  def __str__(self):
    return '{} - {}'.format(self.waktu_mulai, self.waktu_selesai)

class Hari(models.Model):
  nama_hari = models.CharField(max_length=50)
  jam = models.ForeignKey(Jam, on_delete=models.SET_NULL, null=True)
  
  def __str__(self):
    return self.nama_hari

class Mapel(models.Model):
  nama_mapel = models.CharField(max_length=50)
  kelas = models.ForeignKey(Kelas, on_delete=models.SET_NULL, null=True)
  waktu = models.IntegerField()
  
  def __str__(self):
    return '{} - {}'.format(self.nama_mapel, self.kelas)

JENIS_KELAMIN = (
  ('L', 'Laki-Laki'),
  ('P', 'Perempuan')
)
STATUS = (
  (1, 'Aktif'),
  (2, 'Nonaktif')
)

class Guru(models.Model):
  nama = models.CharField(max_length=50)
  telepon = models.CharField(max_length=50)
  mapel = models.ForeignKey(Mapel, on_delete=models.SET_NULL, null=True)
  alamat = models.CharField(max_length=200)
  jenis_kelamin = models.CharField(max_length=1, choices=JENIS_KELAMIN)
  status = models.IntegerField(choices=STATUS, default=1)
  user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

  def __str__(self):
    return f'{self.nama}'

class Tugas(models.Model):
  mapel = models.ForeignKey(Mapel, on_delete=models.SET_NULL, null=True)  
  guru = models.ForeignKey(Guru, on_delete=models.SET_NULL, null=True)  

  def __str__(self):
    return f'{self.guru} {self.mapel}'

class Jadwal(models.Model):
  tugas = models.ForeignKey(Tugas, on_delete=models.SET_NULL, null=True)  
  waktu = models.ForeignKey(Hari, on_delete=models.SET_NULL, null=True)  

  def __str__(self):
    return f'{self.tugas} {self.waktu}'

class Excelfile(models.Model):
  file = models.FileField(upload_to='files')