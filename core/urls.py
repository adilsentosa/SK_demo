from django.urls import path

from core import excelviews, views

urlpatterns = [
    path('', views.index),
    path('dashboard/', views.index, name='index'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('kelas/', views.form_Kelas, name='kelas'),
    path('kelas/create_kelas/', views.create_Kelas, name='create_kelas'),
    path('kelas/update_kelas/<str:pk>/', views.update_Kelas, name='update_kelas'),
    path('kelas/delete_kelas/<str:pk>/', views.delete_Kelas, name='delete_kelas'),
    path('kelas/kelas-import/', excelviews.upload_file_Kelas, name='importkelas'),
    path('kelas/kelas-export', excelviews.export_filekelas, name='exportkelas'),

    path('ruangan/', views.form_Ruangan, name='ruangan'),
    path('ruangan/create', views.create_Ruangan, name='create_ruangan'),
    path('ruangan/update/<str:pk>/', views.update_Ruangan, name='update_ruangan'),
    path('delete_ruangan/<str:pk>/', views.delete_Ruangan, name='delete_ruangan'),
    path('ruangan/ruangan-import/', excelviews.upload_file_Ruangan, name='importruangan'),
    path('ruangan/ruangan-export/', excelviews.export_Ruangan, name='exportruangan'),

    path('jam/', views.form_jam, name='jam'),
    path('jam/create', views.create_jam, name='create_jam'),
    path('jam/update/<str:pk>/', views.update_jam, name='update_jam'),
    path('delete_jam/<str:pk>/', views.delete_jam, name='delete_jam'),
    path('jam/jam-import/', excelviews.upload_file_jam, name='importjam'),
    path('jam/jam-export/', excelviews.export_jam, name='exportjam'),
    
    path('hari/', views.form_hari, name='hari'),
    path('hari/create', views.create_hari, name='create_hari'),
    path('hari/update/<str:pk>/', views.update_hari, name='update_hari'),
    path('delete_hari/<str:pk>/', views.delete_hari, name='delete_hari'),
    path('hari/hari-import/', excelviews.upload_file_hari, name='importhari'),
    path('hari/hari-export/', excelviews.export_hari, name='exporthari'),
      
    path('mapel/', views.form_mapel, name='mapel'),
    path('mapel/create', views.create_mapel, name='create_mapel'),
    path('mapel/update/<str:pk>/', views.update_mapel, name='update_mapel'),
    path('delete_mapel/<str:pk>/', views.delete_mapel, name='delete_mapel'),
    path('mapel/mapel-import/', excelviews.upload_file_mapel, name='importmapel'),
    path('mapel/mapel-export/', excelviews.export_mapel, name='exportmapel'),
  
    path('guru/', views.form_Guru, name='guru'),
    path('guru/create', views.create_Guru, name='create_guru'),
    path('guru/update/<str:pk>/', views.update_Guru, name='update_guru'),
    path('delete_guru/<str:pk>/', views.delete_Guru, name='delete_guru'),
    path('guru/guru-import/', excelviews.upload_file_Guru, name='importguru'),
    path('guru/guru-export/', excelviews.upload_file_Guru, name='exportguru'),


    path('tugas/', views.form_tugas, name='tugas'),
    path('tugas/create', views.create_tugas, name='create_tugas'),
    path('tugas/update/<str:pk>/', views.update_tugas, name='update_tugas'),
    path('delete_tugas/<str:pk>/', views.delete_tugas, name='delete_tugas'),
    path('tugas/tugas-import/', excelviews.upload_file_tugas, name='importtugas'),
    path('tugas/tugas-export/', excelviews.upload_file_tugas, name='exporttugas'),

    path('generate/', views.generate, name='generate'),
    path('jadwal/', views.jadwal_views, name='jadwal'),
     path('jadwal/jadwal-export/', excelviews.export_jadwal, name='jadwalexport'),
]
handler404 = 'core.views.error_404'



