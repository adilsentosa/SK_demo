import datetime
from django.shortcuts import render, redirect
import pandas as pd
from .models import *

from django.contrib.auth.models import Group, User

from django.http import HttpResponse
import xlwt


# KELAS
def create_Kelas(file_path):
  df = pd.read_excel(file_path)
  list_file = [list(row) for  row in df.values]
  for l in list_file:
    Kelas.objects.create(nama_kelas = l[1],)

def upload_file_Kelas(request):
  if request.method == 'POST':
    file = request.FILES['file']
    obj = Excelfile.objects.create(file = file)    
    create_Kelas(obj.file) 
    return redirect('kelas')
      
  return render(request,'back/kelas/baru.html')

def export_filekelas(request):
  respone = HttpResponse(content_type='application/ms-excel')
  respone['Content-Disposition'] = 'attachment; filename=Kelas' +\
      str(datetime.datetime.now())+'.xls'
  wb = xlwt.Workbook(encoding='utf-8')
  ws = wb.add_sheet('Kelas')
  row_num = 0
  font_style = xlwt.XFStyle()
  font_style.font.bold = True
  columns = ['id','nama_kelas']
  
  for col_num in range(len(columns)):
    ws.write(row_num, col_num, columns[col_num], font_style)
      
  font_style = xlwt.XFStyle()
  
  rows = Kelas.objects.all().values_list('id','nama_kelas')    
  for row in rows :
    row_num+=1        
    for col_num in range(len(row)):
      ws.write(row_num, col_num, str(row[col_num]), font_style)
  wb.save(respone)
  
  return respone

# RUANGAN
def create_Ruangan(file_path):
  df = pd.read_excel(file_path)
  list_file = [list(row) for  row in df.values]
  for l in list_file:
    Ruangan.objects.create(
      nama_ruangan = l[1],
      kelas = Kelas.objects.get(pk=l[2]),
      jenis = l[3],
    )
        
def upload_file_Ruangan(request):
  if request.method == 'POST':
    file = request.FILES['file']
    obj = Excelfile.objects.create(file = file)    
    create_Ruangan(obj.file)
    return redirect('ruangan')
      
  return render(request,'back/ruangan/baru.html')

def export_Ruangan(request):
  respone = HttpResponse(content_type='application/ms-excel')
  respone['Content-Disposition'] = 'attachment; filename=Ruangan' +\
      str(datetime.datetime.now())+'.xls'
  wb = xlwt.Workbook(encoding='utf-8')
  ws = wb.add_sheet('Kelas')
  row_num = 0
  font_style = xlwt.XFStyle()
  font_style.font.bold = True
  columns = ['id', 'nama_ruangan', 'kelas', 'jenis']
  
  for col_num in range(len(columns)):
    ws.write(row_num, col_num, columns[col_num], font_style)
      
  font_style = xlwt.XFStyle()
  
  rows = Ruangan.objects.all().values_list('id', 'nama_ruangan', 'kelas', 'jenis')    
  for row in rows :
    row_num+=1        
    for col_num in range(len(row)):
      ws.write(row_num, col_num, str(row[col_num]), font_style)
  wb.save(respone)
  
  return respone

# JAM
def create_jam(file_path):
  df = pd.read_excel(file_path)
  list_file = [list(row) for  row in df.values]
  for l in list_file:
    Jam.objects.create(waktu_mulai = l[1], waktu_selesai = l[2])
        
def upload_file_jam(request):
  if request.method == 'POST':
    file = request.FILES['file']
    obj = Excelfile.objects.create(file = file)    
    create_jam(obj.file)
    return redirect('jam')
      
  return render(request,'back/jam/baru.html')

def export_jam(request):
  respone = HttpResponse(content_type='application/ms-excel')
  respone['Content-Disposition'] = 'attachment; filename=Jam' +\
      str(datetime.datetime.now())+'.xls'
  wb = xlwt.Workbook(encoding='utf-8')
  ws = wb.add_sheet('Jam')
  row_num = 0
  font_style = xlwt.XFStyle()
  font_style.font.bold = True
  columns = ['id', 'waktu_mulai', 'waktu_selesai']
  
  for col_num in range(len(columns)):
    ws.write(row_num, col_num, columns[col_num], font_style)
      
  font_style = xlwt.XFStyle()
  
  rows = Jam.objects.all().values_list('id', 'waktu_mulai', 'waktu_selesai')    
  for row in rows :
    row_num+=1        
    for col_num in range(len(row)):
      ws.write(row_num, col_num, str(row[col_num]), font_style)
  wb.save(respone)
  
  return respone

# HARI
def create_hari(file_path):
  df = pd.read_excel(file_path)
  list_file = [list(row) for  row in df.values]
  for l in list_file:
    Hari.objects.create(nama_hari=l[1], jam=Jam.objects.get(pk=l[2]))
        
def upload_file_hari(request):
  if request.method == 'POST':
    file = request.FILES['file']
    obj = Excelfile.objects.create(file = file)    
    create_hari(obj.file)
    return redirect('hari')
      
  return render(request,'back/hari/baru.html')

def export_hari(request):
  respone = HttpResponse(content_type='application/ms-excel')
  respone['Content-Disposition'] = 'attachment; filename=Hari' +\
      str(datetime.datetime.now())+'.xls'
  wb = xlwt.Workbook(encoding='utf-8')
  ws = wb.add_sheet('Hari')
  row_num = 0
  font_style = xlwt.XFStyle()
  font_style.font.bold = True
  columns = ['id', 'nama_hari', 'jam']
  
  for col_num in range(len(columns)):
    ws.write(row_num, col_num, columns[col_num], font_style)
      
  font_style = xlwt.XFStyle()
  
  rows = Hari.objects.all().values_list('id', 'nama_hari', 'jam')    
  for row in rows :
    row_num+=1        
    for col_num in range(len(row)):
      ws.write(row_num, col_num, str(row[col_num]), font_style)
  wb.save(respone)
  
  return respone

# MAPEL
def create_mapel(file_path):
  df = pd.read_excel(file_path)
  list_file = [list(row) for  row in df.values]
  for l in list_file:
    Mapel.objects.create(
      nama_mapel = l[1], 
      waktu = l[2],
      kelas = Kelas.objects.get(pk=l[3])
    )
        
def upload_file_mapel(request):
  if request.method == 'POST':
    file = request.FILES['file']
    obj = Excelfile.objects.create(file = file)    
    create_mapel(obj.file)
    return redirect('mapel')
      
  return render(request,'back/mapel/baru.html')

def export_mapel(request):
  respone = HttpResponse(content_type='application/ms-excel')
  respone['Content-Disposition'] = 'attachment; filename=Mapel ' +\
      str(datetime.datetime.now())+'.xls'
  wb = xlwt.Workbook(encoding='utf-8')
  ws = wb.add_sheet('Mapel')
  row_num = 0
  font_style = xlwt.XFStyle()
  font_style.font.bold = True
  columns = ['id', 'nama_mapel', 'kelas', 'waktu']
  
  for col_num in range(len(columns)):
    ws.write(row_num, col_num, columns[col_num], font_style)
      
  font_style = xlwt.XFStyle()
  
  rows = Mapel.objects.all().values_list('id', 'nama_mapel', 'kelas', 'waktu')    
  for row in rows :
    row_num+=1        
    for col_num in range(len(row)):
      ws.write(row_num, col_num, str(row[col_num]), font_style)
  wb.save(respone)
  
  return respone

# GURU
def create_Guru(file_path):
  df = pd.read_excel(file_path)
  list_file = [list(row) for  row in df.values]
  for l in list_file:
    Guru.objects.create(
      gid = l[1],
      nama = l[2],  
    )
        
def upload_file_Guru(request):
  if request.method == 'POST':
    file = request.FILES['file']
    obj = Excelfile.objects.create(file = file)    
    create_Guru(obj.file) 
    return redirect('guru')
      
  return render(request,'back/guru/baru.html')

# TUGAS
def create_tugas(file_path):
  df = pd.read_csv(file_path)
  list_file = [list(row) for  row in df.values]
  for l in list_file:
    Tugas.objects.create(
      guru=Guru.objects.get(pk=l[1]),
      mapel=Mapel.objects.get(pk=l[2]),
    )
        
def upload_file_tugas(request):
  if request.method == 'POST':
    file = request.FILES['file']
    obj = Excelfile.objects.create(file = file)    
    create_tugas(obj.file)
    return redirect('tugas')
      
  return render(request,'back/tugas/baru.html')

def export_tugas(request):
  respone = HttpResponse(content_type='application/ms-excel')
  respone['Content-Disposition'] = 'attachment; filename=Tugas ' +\
      str(datetime.datetime.now())+'.xls'
  wb = xlwt.Workbook(encoding='utf-8')
  ws = wb.add_sheet('Tugas')
  row_num = 0
  font_style = xlwt.XFStyle()
  font_style.font.bold = True
  columns = ['id', 'guru', 'mapel']
  
  for col_num in range(len(columns)):
    ws.write(row_num, col_num, columns[col_num], font_style)
      
  font_style = xlwt.XFStyle()
  
  rows = Tugas.objects.all().values_list('id', 'guru', 'mapel')    
  for row in rows :
    row_num+=1        
    for col_num in range(len(row)):
      ws.write(row_num, col_num, str(row[col_num]), font_style)
  wb.save(respone)
  
  return respone

#JADWAL
def export_jadwal(request):
  respone = HttpResponse(content_type='application/ms-excel')
  respone['Content-Disposition'] = 'attachment; filename=Jadwal ' +\
      str(datetime.datetime.now())+'.xls'
  wb = xlwt.Workbook(encoding='utf-8')
  ws = wb.add_sheet('Jadwal')
  row_num = 0
  font_style = xlwt.XFStyle()
  font_style.font.bold = True
  columns = ['tugas__guru__nama', 'waktu__nama_hari','tugas__mapel__nama_mapel','waktu__jam','waktu__jam__waktu_mulai','waktu__jam__waktu_selesai','tugas__mapel__kelas__nama_kelas']
  
  for col_num in range(len(columns)):
    ws.write(row_num, col_num, columns[col_num], font_style)
      
  font_style = xlwt.XFStyle()
  
  rows = Jadwal.objects.order_by().values_list('tugas__guru__nama', 'waktu__nama_hari','tugas__mapel__nama_mapel','waktu__jam__waktu_mulai','waktu__jam__waktu_selesai','tugas__mapel__kelas__nama_kelas')    
  for row in rows :
    row_num+=1        
    for col_num in range(len(row)):
      ws.write(row_num, col_num, str(row[col_num]), font_style)
  wb.save(respone)
  
  return respone