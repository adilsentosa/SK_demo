from django.shortcuts import render,get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from core.algoritma import AG

from .decorators import unauthenticated_user
from .forms import *
from .decorators import allowed_users
from django.contrib.auth.models import Group

@unauthenticated_user
def loginPage(request):
  if request.method == 'POST':
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)

    if user is not None:
      login(request, user)
      return redirect('index')
    else:
      messages.info(request, 'Username OR password is incorrect')

  context = {}
  return render(request, 'registration/login.html', context)

def logoutUser(request):
  logout(request)
  return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Staff'])
# @admin_only
def index(request):
  guru = Guru.objects.all()
  kelas = Kelas.objects.all()
  mapel = Mapel.objects.all()
  hari = Hari.objects.all()
  
  total_guru = guru.count()
  total_kelas = kelas.count()
  total_mapel = mapel.count()
  total_hari = hari.count()

  context = {'total_guru': total_guru, 'total_kelas': total_kelas, 'total_mapel': total_mapel, 'total_hari': total_hari,}
  return render(request, 'index.html', context)

# KELAS
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Staff'])
def form_Kelas(request):
  kelas = Kelas.objects.all()
  
  context = {'kelas': kelas}
  return render(request,'back/kelas/form.html', context )

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Staff'])
def create_Kelas(request):
  form = KelasForm()
  if request.method == 'POST' :
    form = KelasForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, "Data Berhasil Ditambahkan")
      return redirect('kelas')
    
  context = {'form': form}
  return render(request,'back/kelas/create.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Staff'])
def update_Kelas(request, pk):
  k = Kelas.objects.get(id=pk)
  form = KelasForm(instance=k)
  if request.method == 'POST' :
    form = KelasForm(request.POST, instance=k)
    if form.is_valid():
      form.save()
      messages.success(request, "Data Berhasil Diperbaharui")
      return redirect('kelas')
  context = {'form_Kelas': form_Kelas, 'form':form}
  return render(request,'back/kelas/create.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Staff'])
def delete_Kelas(request, pk):
  k = get_object_or_404(Kelas, id=pk)
  k.delete()
  messages.success(request, "Data Berhasil Dihapus")
  return redirect('kelas')

# RUANGAN
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Staff'])
def form_Ruangan(request):
  context = {'ruang_form': Ruangan.objects.all()}
  return render(request, 'back/ruangan/form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Staff'])
def create_Ruangan(request):
  form = RuanganForm(request.POST or None)
  if request.method == 'POST':
    if form.is_valid():
      form.save()
      messages.success(request, "Data Berhasil Ditambahkan")
      return redirect('ruangan')
    else:
      print('Invalid')
  context = {'form':form}
  return render(request, 'back/ruangan/create.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Staff'])
def update_Ruangan(request, pk):
  rg = Ruangan.objects.get(id=pk)
  form = RuanganForm(instance=rg)
  if request.method == 'POST':
    form = RuanganForm(request.POST, instance=rg)
    if form.is_valid():
      form.save()
      messages.success(request, "Data Berhasil Diperbaharui")
      return redirect('ruangan')
    else:
      print('Invalid')
  context = {'form':form}
  return render(request, 'back/ruangan/create.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Staff'])
def delete_Ruangan(request, pk):
  rg = Ruangan.objects.get(pk=pk)
  if request.method == 'POST':
    rg.delete()
    messages.success(request, "Data Berhasil Dihapus")
    return redirect('ruangan')

# JAM
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Staff'])
def form_jam(request):
  context = {'jam': Jam.objects.all()}
  return render(request, 'back/jam/form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Staff'])
def create_jam(request):
    form = JamForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, "Data Berhasil Ditambahkan")
            return redirect('jam')
        else:
            print('Invalid')
    context = {'form':form}
    return render(request, 'back/jam/create.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Staff'])
def update_jam(request, pk):
  jam = Jam.objects.get(id=pk)
  form = JamForm(instance=jam)
  if request.method == 'POST':
    form = JamForm(request.POST, instance=jam)
    if form.is_valid():
      form.save()
      messages.success(request, "Data Berhasil Diperbaharui")
      return redirect('jam')
    else:
      print('Invalid')
  context = {'form':form}
  return render(request, 'back/jam/create.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Staff'])
def delete_jam(request, pk):
  rg = Jam.objects.get(pk=pk)
  if request.method == 'POST':
    rg.delete()
    messages.success(request, "Data Berhasil Dihapus")
    return redirect('jam')

# HARI
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Staff'])
def form_hari(request):
  context = {'hari': Hari.objects.all()}
  return render(request, 'back/hari/form.html', context)

@login_required(login_url='login')
def create_hari(request):
  form = HariForm(request.POST or None)
  if request.method == 'POST':
    if form.is_valid():
      form.save()
      messages.success(request, "Data Berhasil Ditambahkan")
      return redirect('hari')
    else:
      print('Invalid')
  context = {'form':form}
  return render(request, 'back/hari/create.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Staff'])
def update_hari(request, pk):
  hari = Hari.objects.get(id=pk)
  form = HariForm(instance=hari)
  if request.method == 'POST':
    form = HariForm(request.POST, instance=hari)
    if form.is_valid():
      form.save()
      messages.success(request, "Data Berhasil Diperbaharui")
      return redirect('hari')
    else:
      print('Invalid')
  context = {'form':form}
  return render(request, 'back/hari/create.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Staff'])
def delete_hari(request, pk):
  rg = Hari.objects.get(pk=pk)
  if request.method == 'POST':
    rg.delete()
    messages.success(request, "Data Berhasil Dihapus")
    return redirect('hari')

# MAPEL
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Staff'])
def form_mapel(request):
  context = {'mapel': Mapel.objects.all()}
  return render(request, 'back/mapel/form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Staff'])
def create_mapel(request):
  form = MapelForm(request.POST or None)
  if request.method == 'POST':
    if form.is_valid():
      form.save()
      messages.success(request, "Data Berhasil Ditambahkan")
      return redirect('mapel')
    else:
      print('Invalid')
  context = {'form':form}
  return render(request, 'back/mapel/create.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Staff'])
def update_mapel(request, pk):
  mapel = Mapel.objects.get(id=pk)
  form = MapelForm(instance=mapel)
  if request.method == 'POST':
    form = MapelForm(request.POST, instance=mapel)
    if form.is_valid():
      form.save()
      messages.success(request, "Data Berhasil Diperbaharui")
      return redirect('mapel')
    else:
      print('Invalid')
  context = {'form':form}
  return render(request, 'back/mapel/create.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Staff'])
def delete_mapel(request, pk):
  rg = Mapel.objects.get(pk=pk)
  if request.method == 'POST':
    rg.delete()
    messages.success(request, "Data Berhasil Dihapus")
    return redirect('mapel')

# GURU
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Staff'])
def form_Guru(request):
  context = {'guru': Guru.objects.all()}
  return render(request, 'back/guru/form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Staff'])
def create_Guru(request):
  form = GuruForm(request.POST or None)
  if request.method == 'POST':
    if form.is_valid():
      user =form.save()
      username = form.cleared_data.get(username)
      group = Group.objects.get(name='Guru')
      user.groups.add(group)
      messages.success(request, "Data Berhasil Ditambahkan")
      return redirect('guru')
    else:
      print('Invalid')
  context = {'form': form}
  return render(request, 'back/guru/create.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Staff'])
def update_Guru(request, pk):
  gr = Guru.objects.get(id=pk)
  form = GuruForm(instance=gr)
  if request.method =='POST':
    form =GuruForm(request.POST, instance=gr)
    if form.is_valid():
      form.save()
      messages.success(request, "Data Berhasil Diperbaharui")
      return redirect('guru')
    else:
      print('Invalid')
  context ={'form':form}
  return render(request, 'back/guru/create.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Staff'])
def delete_Guru(request, pk):
    gr = Guru.objects.get(pk=pk)
    if request.method == 'POST':
        gr.delete()
        messages.success(request, "Data Berhasil Dihapus")
        return redirect('guru')
    context = {'item':gr}
    return render(request, 'penjadwalan/guru/guru_delete.html', context)
  
  # Staff
@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Staff'])
def form_Staff(request):
  context = {'staff': Staff.objects.all()}
  return render(request, 'back/staff/form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin'])
def create_Staff(request):
  form = StafForm(request.POST or None)
  if request.method == 'POST':
    if form.is_valid():
      
      user= form.save()
      usermame =form.cleared_data.get('username')
      group= Group.objects.get(name ='Staff')
      user.groups.add(group)
      
      messages.success(request, "Data Berhasil Ditambahkan")
      return redirect('staff')
    else:
      print('Invalid')
  context = {'form': form}
  return render(request, 'back/staff/create.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Staff'])
def update_Staff(request, pk):
  sf = Staff.objects.get(id=pk)
  form = StafForm(instance=sf)
  if request.method =='POST':
    form =StafForm(request.POST, instance=sf)
    if form.is_valid():
      form.save()
      messages.success(request, "Data Berhasil Diperbaharui")
      return redirect('staff')
    else:
      print('Invalid')
  context ={'form':form}
  return render(request, 'back/staff/create.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Staff'])
def delete_Staff(request, pk):
    sf = Staff.objects.get(pk=pk)
    if request.method == 'POST':
        sf.delete()
        messages.success(request, "Data Berhasil Dihapus")
        return redirect('staff')
    context = {'item':sf}
    return render(request, 'penjadwalan/guru/guru_delete.html', context)
  

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Staff'])
def form_tugas(request):
  context = {'tugas': Tugas.objects.all()}
  return render(request, 'back/tugas/form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Staff'])
def create_tugas(request):
  form = TugasForm(request.POST or None)
  if request.method == 'POST':
    if form.is_valid():
      form.save()
      messages.success(request, "Data Berhasil Ditambahkan")
      return redirect('tugas')
    else:
      print('Invalid')
  context = {'form':form}
  return render(request, 'back/tugas/create.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Staff'])
def update_tugas(request, pk):
  tugas = Tugas.objects.get(id=pk)
  form = TugasForm(instance=tugas)
  if request.method == 'POST':
    form = TugasForm(request.POST, instance=tugas)
    if form.is_valid():
      form.save()
      messages.success(request, "Data Berhasil Diperbaharui")
      return redirect('tugas')
    else:
      print('Invalid')
  context = {'form':form}
  return render(request, 'back/tugas/create.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['Admin','Staff'])
def delete_tugas(request, pk):
  rg = Tugas.objects.get(pk=pk)
  if request.method == 'POST':
    rg.delete()
    messages.success(request, "Data Berhasil Dihapus")
    return redirect('tugas')

@login_required
@allowed_users(allowed_roles=['Admin','Staff'])
def generate(request):
  context = {}
  context['total_tugas'] =  Tugas.objects.all().count()
  context['total_waktu'] = Hari.objects.all().count()

  if request.method == 'POST':
    num_kromosom = int(request.POST['num_kromosom'])
    max_generation = int(request.POST['max_generation'])
    crossover_rate = int(request.POST['crossover_rate'])
    mutation_rate = int(request.POST['mutation_rate'])
    
    if num_kromosom < 10 or num_kromosom > 500:
      messages.success(request, "Masukkan jumlah kromosom dari 10 sampai 500")
      return render(request, 'back/penjadwalan/form.html', context)
    
    if max_generation < 25 or max_generation > 500:
      messages.success(request, "Masukkan maksimal generasi dari 25 sampai 500")
      return render(request, 'back/penjadwalan/form.html', context)
    
    if crossover_rate < 1 or crossover_rate > 100 or mutation_rate < 1 or mutation_rate > 100:
      messages.success(request, "Masukkan dari 1 sampai 100")
      return render(request, 'back/penjadwalan/form.html', context)

    tugas_queryset = Tugas.objects.all()
    tugas_dict = {}
    for tugas in tugas_queryset:
      tugas_dict[tugas.id-1] = {
        'id_tugas': tugas.id,
        'id_guru': tugas.guru.id,
        'id_mapel': tugas.mapel.id,
        'nama_mapel': tugas.mapel.nama_mapel,
        'waktu': tugas.mapel.waktu,
        'id_kelas': tugas.mapel.kelas.id
      }

    hari_queryset = Hari.objects.all()
    hari_dict = {}
    for hari in hari_queryset:
      hari_dict[hari.id-1] = {
        'id_hari': hari.id,
        'nama_hari': hari.nama_hari,
        'id_jam': hari.jam.id,
        'waktu_mulai': hari.jam.waktu_mulai,
        'waktu_selesai': hari.jam.waktu_selesai,
      }

    ag = AG(hari_dict, tugas_dict)
    ag.num_crommosom = num_kromosom
    ag.max_generation = max_generation
    ag.debug = True if request.POST.get('debug') else False
    ag.crossover_rate = crossover_rate
    ag.mutation_rate = mutation_rate
    data = ag.generate()
    context.update(data)

  return render(request, 'back/penjadwalan/form.html', context)

@login_required
def jadwal_views(request):
  context = {'jadwal': Jadwal.objects.order_by('tugas__guru__nama', 'waktu__nama_hari').all()}
  return render(request, 'back/jadwal/index.html', context)

def error_404(request, exception):
  return render(request, '404.htm')