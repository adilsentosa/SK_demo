from core.models import *

import random
import time
import math

class AG:
  def __init__(self, waktu, tugas):
    self.num_crommosom = None  # jumlah kromosom awal yang dibangkitkan
    self.waktu = waktu  # data waktu
    self.tugas = tugas  # data tugas
    self.generation = 0  # generasi ke....
    self.max_generation = 2
    self.crommosom = []  # array kromosom sesuai num_cromosom
    self.success = False  # keadaan jika sudah ada solusi terbaik
    self.debug = False  # menampilkan debug jika diset True
    self.fitness = []  # nilai fitness setiap kromosom
    self.console = ""  # menyimpan proses algoritma
    self.total_fitness = 0  # menyimpan total fitness untuk masing-masing kromosom
    self.probability = []  # menyimpan probabilitas fitness masing-masing kromosom
    self.com_pro = []  # menyimpan fitness komulatif untuk masing-masing kromosom
    self.rand = []  # menyimpan bilangan rand()
    self.parent = []  # menyimpan parent saat crossover
    self.best_fitness = 0  # menyimpan nilai fitness tertinggi
    self.best_cromossom = []  # menyimpan kromosom dengan fitness tertinggi
    self.crossover_rate = 75  # prosentase kromosom yang akan dipindah silang
    self.mutation_rate = 25  # prosentase kromosom yang akan dimutasi
    self.time_start = None  # menyimpan waktu mulai proses algoritma
    self.time_end = None  # menyimpan waktu selesai proses algoritma

  def generate(self):
    self.time_start = time.time()
    self.generate_crommosom()

    while self.generation < self.max_generation and not self.success:
      self.generation += 1
      self.console += f"<h6>Generasi ke-{self.generation}</h6>"
      self.show_crommosom()
      self.calculate_all_fitness()
      self.show_fitness()

      if not self.success:
        self.get_com_pro()
        self.selection()
        self.show_crommosom()
        self.show_fitness()

      if not self.success:
        self.crossover()
        self.show_crommosom()
        self.show_fitness()

      if not self.success:
        self.mutation()
        self.show_crommosom()
        self.show_fitness()

    self.save_result()

    self.time_end = time.time()
    execution_time = self.time_end - self.time_start

    # print(f"FITNESS TERBAIK: {self.best_fitness}")
    # print(f"Execution Time: {execution_time} seconds")
    # print(f"Memory Usage: {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024} kilo bytes")
    # print(f"GENERASI: {self.generation}")
    # print(f"CROMOSSOM TERBAIK: {self.print_cros(self.best_cromossom)}")

    data = {
      'best_fitness': self.best_fitness,
      'execution_time': execution_time,
      'generation': self.generation,
      'best_cromossom': self.print_cros(self.best_cromossom),
      'debug': self.get_debug()
    }
    return data

  def mutation(self):
    mutation = []
    self.console += f"<h6>Mutasi generasi ke-{self.generation}</h6>"
    gen_per_cro = len(self.tugas)
    total_gen = len(self.crommosom) * gen_per_cro
    total_mutation = round(self.mutation_rate / 100 * total_gen)

    for _ in range(total_mutation):
      val = random.randint(1, total_gen)

      cro_index = math.ceil(val / gen_per_cro) - 1
      gen_index = (val - 1) % gen_per_cro

      self.console += f"{val} : [{cro_index}, {gen_index}]\r\n"
      self.crommosom[cro_index][gen_index]['waktu'] = random.randint(0, len(self.waktu) - 1)
      self.fitness[cro_index] = self.calculate_fitness(cro_index)

      if self.success:
        return

    return False
  
  def save_result(self):
    Jadwal.objects.all().delete()

    for val in self.best_cromossom:
      jadwal = Jadwal.objects.create(
        tugas= Tugas.objects.get(pk=self.tugas[val['tugas']]['id_tugas']),
        waktu= Hari.objects.get(pk=self.waktu[val['waktu']]['id_hari'])
      )
      jadwal.save()

  def show_crommosom(self):
    cros = self.crommosom
    a = []
    for key, val in enumerate(cros):
      a.append(self.print_cros(val, key))

    self.console += " \r\n".join(a) + "\r\n"

  def print_cros(self, val=[], key=0):
    arr = []
    for v in val:
      arr.append(f"[{v['tugas']}, {v['waktu']}]")
    return "Kromosom[{}]: ({})".format(key, ",".join(arr))

  def calculate_all_fitness(self):
    for key, val in enumerate(self.crommosom):
      self.calculate_fitness(key)

  def calculate_fitness(self, key):
    cro = self.crommosom[key]
    # guru sama waktu sama
    clash_guru = self.get_clash_guru(cro)
    # kelas sama waktu sama
    clash_kelas = self.get_clash_kelas(cro)

    f = {}
    f['desc'] = f"1/(1+{clash_guru}+{clash_kelas})"
    f['nilai'] = 1 / (1 + clash_guru + clash_kelas)

    if f['nilai'] == 1:  # jika sudah optimal maka berhenti
      self.success = True

    if f['nilai'] > self.best_fitness:
      self.best_fitness = f['nilai']
      self.best_cromossom = self.crommosom[key]

    self.fitness[key] = f
    return f

  def show_fitness(self):
    # print(self.fitness)
    for key, fit in enumerate(self.fitness):
      self.console += f"F[{key}]: {fit['desc']} = {fit['nilai']} \r\n"
    self.get_total_fitness()
    self.console += f"Total F: {self.total_fitness} \r\n"

  def crossover(self):
    self.console += f"<h6>Pindah silang generasi ke-{self.generation}</h6>"
    parent = []

    for key, val in enumerate(self.crommosom):
      rnd = random.random()
      if rnd <= self.crossover_rate / 100:
        parent.append(key)

    for key, val in enumerate(parent):
      self.console += f"Parent[{key}]: {val} \r\n"

    c = len(parent)

    if c > 1:
      new_cro = {}
      for a in range(c - 1):
        new_cro[parent[a]] = self.get_crossover(parent[a], parent[a + 1])
      new_cro[parent[c - 1]] = self.get_crossover(parent[c - 1], parent[0])

      for key, val in new_cro.items():
        self.crommosom[key] = val
        self.calculate_fitness(key)
  
  def get_crossover(self, key1, key2):
    cro1 = self.crommosom[key1]
    cro2 = self.crommosom[key2]

    offspring = random.randint(0, len(cro1) - 2)
    new_cro = []

    for a in range(len(cro1)):
      if a <= offspring:
        new_cro.append(cro1[a])
      else:
        new_cro.append(cro2[a])

    return new_cro
  
  def get_debug(self):
    if self.debug:
      return "<pre class='border border-1 p-2' style='font-size:0.8em'>{}</pre>".format(self.console)
    return False

  def generate_crommosom(self):
    numb = 0
    while numb < self.num_crommosom:
      cro = self.get_rand_crommosom()
      self.crommosom.append(cro)
      self.fitness.append(0)
      numb += 1

  def get_rand_crommosom(self):
    result = []
    tugass = self.tugas
    no = 0

    for key, val in tugass.items():
      for a in range(1):
        result.append({'tugas': val['id_tugas'] - 1, 'waktu': random.randint(0, len(self.waktu) - 1)})
        no += 1

    return result

  def get_total_fitness(self):
    self.total_fitness = 0
    for val in self.fitness:
      self.total_fitness += val['nilai']
    return self.total_fitness
  
  def get_probability(self):
    self.probability = []
    for key, val in enumerate(self.fitness):
      x = val['nilai'] / self.total_fitness
      self.probability.append(x)
    return self.probability

  def get_com_pro(self):
    self.get_probability()

    self.com_pro = []
    x = 0
    for key, val in enumerate(self.probability):
      x += val
      self.com_pro.append(x)

  def selection(self):
    self.console += "<h6>Seleksi generasi ke-{}</h6>".format(self.generation)
    self.get_rand()
    new_cro = []
    for key, val in self.rand.items():
      k = self.choose_selection(val)
      new_cro.append(self.crommosom[k])
      self.fitness[key] = self.fitness[k]
    self.crommosom = new_cro

  def choose_selection(self, rand_numb=0):
    for key, val in enumerate(self.com_pro):
      if rand_numb <= val:
        return key

  def get_rand(self):
    self.rand = {}
    for key, val in enumerate(self.fitness):
      r = random.random()
      self.rand[key] = r

  def get_clash_guru(self, crom):
    clash = 0
    count = len(crom)

    for a in range(count - 1):
      for b in range(a + 1, count):
        tugas1 = self.tugas[crom[a]['tugas']]
        tugas2 = self.tugas[crom[b]['tugas']]
        if tugas1['id_guru'] == tugas2['id_guru']:
          if crom[a]['waktu'] == crom[b]['waktu']:
            clash += 1
    return clash

  def get_clash_kelas(self, crom):
    clash = 0
    count = len(crom)

    for a in range(count - 1):
      for b in range(a + 1, count):
        tugas1 = self.tugas[crom[a]['tugas']]
        tugas2 = self.tugas[crom[b]['tugas']]
        if tugas1['id_kelas'] == tugas2['id_kelas']:
          if crom[a]['waktu'] == crom[b]['waktu']:
              clash += 1
    return clash



# TIMETABEL
# variabel yang digunakan sebagai parameter dalam proses penjadwalan
POPULATION_SIZE = 9 #menetukan jumlah individu dalam populasi
NUMB_OF_ELITE_SCHEDULES = 1 #menentukan jumlah jadwal yang di ambil dari setiap populasi
TOURNAMENT_SELECTION_SIZE = 3 #menentukan jumlah individu dalam seleksi turnamen
MUTATION_RATE = 0.05 #menentukan tingkat mutasi dalam proses evolusi

# Fungsi menyimpan semua data yang digunakan untuk membuat jadwal pelajaran
# class Data:
#     def __init__(self):
#         self._ruangans = Ruangan.objects.all()
#         self._waktu_belajars = WaktuBelajar.objects.all()
#         self._pengajar = Guru.objects.all()
#         self._matapelajarans = MataPelajaran.objects.all()
#         self._kelass= Kelasbeta.objects.all()

#     def get_ruangans(self): return self._ruangans

#     def get_pengajar(self): return self._pengajar

#     def get_matapelajarans(self): return self._matapelajarans

#     def get_kelass(self): return self._kelass

#     def get_waktu_belajars(self): return self._waktu_belajars
    
# # fungsi menyimpan informasi tentang sesi pembelajaran yang memuat informasi berupa nama kelas,mata pelajaran, guru, watu belajar dan ruangan. 
# class Class:
#     def __init__(self, id, kelas, section, matapelajaran):
#         self.section_id = id
#         self.kelasbeta = kelas
#         self.matapelajaran = matapelajaran
#         self.guru = None
#         self.waktubelajar = None
#         self.ruangan = None
#         self.section = section

#     def get_id(self): return self.section_id

#     def get_kelas(self): return self.kelasbeta

#     def get_matapelajaran(self): return self.matapelajaran

#     def get_guru(self): return self.guru

#     def get_waktu_belajar(self): return self.waktubelajar

#     def get_ruangan(self): return self.ruangan

#     def set_guru(self, guru): self.guru = guru

#     def set_waktu_belajar(self, waktu_belajar): self.waktubelajar = waktu_belajar 

#     def set_ruangan(self, ruangan): self.ruangan = ruangan


# data = Data()

# class Jadwal:
#     def __init__(self):
#         self._data = data #atribut menyimpan data
#         self._classes = [] # menyimpan data kelas
#         self._numberOfConflicts = 0 # menyimpan  jumlah konflik
#         self._fitness = -1 # menyimpan nilai fitnes
#         self._classNumb = 0 #menyimpan jumlah kelas
#         self._isFitnessChanged = True #menentukan apakah nilai fitnes sudah dipebaruhi atau belum
        
#     # method yang mengembalikan daftar kelas
#     def get_classes(self):
#         self._isFitnessChanged = True
#         return self._classes
    
#     #method yang mengembalikan jumlah konflik jadwal
#     def get_numbOfConflicts(self): return self._numberOfConflicts
    
#     #method yang mengembalikan nilai fitness
#     def get_fitness(self):
#         if self._isFitnessChanged:
#             self._fitness = self.calculate_fitness()
#             self._isFitnessChanged = False
#         return self._fitness
    
#     #method yang menginisialisasi data jadwal sekolah, membuat daftar kelas, dan menentukan waktu, ruangan, dan guru untuk setiap kelas
#     def initialize(self):
#         sections = Section.objects.all()
#         for section in sections:
#             kelas = section.kelasbeta
#             n = section.num_class_in_week
#             if n <= len(WaktuBelajar.objects.all()):
#                 matapelajarans = kelas.matapelajarans.all()
#                 for matapelajaran in matapelajarans:
#                     for i in range(n // len(matapelajarans)):
#                         mat_gur = matapelajaran.pengajar.all()
#                         kelasbaru = Class(self._classNumb, kelas, section.section_id, matapelajaran)
#                         self._classNumb += 1
#                         kelasbaru.set_waktu_belajar(data.get_waktu_belajars()[rnd.randrange(0, len(WaktuBelajar.objects.all()))])
#                         kelasbaru.set_ruangan(data.get_ruangans()[rnd.randrange(0, len(data.get_ruangans()))])
#                         kelasbaru.set_guru(mat_gur[rnd.randrange(0, len(mat_gur))])
#                         self._classes.append(kelasbaru)
#             else:
#                 n = len(WaktuBelajar.objects.all())
#                 matapelajarans = kelas.matapelajarans.all()
#                 for matapelajaran in matapelajarans:
#                     for i in range(n // len(matapelajarans)):
#                         mat_gur = matapelajaran.pengajar.all()
#                         kelasbaru = Class(self._classNumb, kelas, section.section_id, matapelajaran)
#                         self._classNumb += 1
#                         kelasbaru.set_waktu_belajar(data.get_waktu_belajars()[rnd.randrange(0, len(WaktuBelajar.objects.all()))])
#                         kelasbaru.set_ruangan(data.get_ruangans()[rnd.randrange(0, len(data.get_ruangans()))])
#                         kelasbaru.set_guru(mat_gur[rnd.randrange(0, len(mat_gur))])
#                         self._classes.append(kelasbaru)

#         return self
    
#     #method yang menghitung nilai fitness dari jadwal sekolah
#     def calculate_fitness(self):
#         self._numberOfConflicts = 0
#         classes = self.get_classes()
#         for i in range(len(classes)):
#             if classes[i].ruangan.r_kapasistas < int(classes[i].matapelajaran.max_jumlah_siswa):
#                 self._numberOfConflicts += 1
#             for j in range(len(classes)):
#                 if j >= i:
#                     if (classes[i].waktubelajar == classes[j].waktubelajar) and \
#                             (classes[i].section_id != classes[j].section_id) and (classes[i].section == classes[j].section):
#                         if classes[i].ruangan == classes[j].ruangan:
#                             self._numberOfConflicts += 1
#                         if classes[i].guru == classes[j].guru:
#                             self._numberOfConflicts += 1
#         return 1 / (1.0 * self._numberOfConflicts + 1)
    
# # Nilai fitness dihitung berdasarkan jumlah konflik jadwal, semakin sedikit konflik maka 
# # nilai fitness akan semakin baik. Konflik dapat terjadi antara waktu belajar, ruangan, atau guru yang sama pada saat yang bersamaan.

# # class population merepresentasikan populasi jadwal pelajaran
# class Population: 
#     def __init__(self, size): #membuat objek populasi jadwal
#         self._size = size
#         self._data = data
#         self._jadwals = [Jadwal().initialize() for i in range(size)]

#     def get_jadwals(self): #untuk mengambil data jadwal dalam populasi
#         return self._jadwals


# #class utama yang memproses evolusi penjadwalan
# class Genetika:
#     def evolve(self, population): #untuk mengambil populasi sebagai input dan mengembalikan populasi
#                                   # yang lebih baik melalui proses mutasi crosover
#         return self._mutate_population(self._crossover_population(population))

#     def _crossover_population(self, pop): #menggabungkan dua jadwal menjadi satu dengan mengambil bagian dari kedua jadwal dan membentuk
#                                           #jadwal baru yang lebih baik
#         crossover_pop = Population(0)
#         for i in range(NUMB_OF_ELITE_SCHEDULES):
#             crossover_pop.get_jadwals().append(pop.get_jadwals()[i])
#         i = NUMB_OF_ELITE_SCHEDULES
#         while i < POPULATION_SIZE:
#             jadwal1 = self._select_tournament_population(pop).get_jadwals()[0]
#             jadwal2 = self._select_tournament_population(pop).get_jadwals()[0]
#             crossover_pop.get_jadwals().append(self._crossover_jadwal(jadwal1, jadwal2))
#             i += 1
#         return crossover_pop

#     def _mutate_population(self, population): #mengubah jadwal-jadwal dalam populasi melalui proses mutasi.
#         for i in range(NUMB_OF_ELITE_SCHEDULES, POPULATION_SIZE):
#             self._mutate_jadwal(population.get_jadwals()[i])
#         return population

#     def _crossover_jadwal(self, jadwal1, jadwal2): #melakukan crossover antara dua jadwal dan mengembalikan jadwal baru yang dibuat dari 
#                                                    #bagian-bagian dari jadwal-jadwal tersebut
#         crossoverJadwal = Jadwal().initialize()
#         for i in range(0, len(crossoverJadwal.get_classes())):
#             if rnd.random() > 0.5:
#                 crossoverJadwal.get_classes()[i] = jadwal1.get_classes()[i]
#             else:
#                 crossoverJadwal.get_classes()[i] = jadwal2.get_classes()[i]
#         return crossoverJadwal    

#     def _mutate_jadwal(self, mutateJadwal): #mengubah jadwal menjadi jadwal baru dengan mengubah satu atau beberapa kelas matapelajaran.
#         jadwal = Jadwal().initialize()
#         for i in range(len(mutateJadwal.get_classes())):
#             if MUTATION_RATE > rnd.random():
#                 mutateJadwal.get_classes()[i] = jadwal.get_classes()[i]
#         return mutateJadwal

#     def _select_tournament_population(self, pop): # memilih jadwal-jadwal dari populasi dengan membandingkan fitness-nya dan memilih
#                                                     #jadwal dengan fitness terbaik.
#         tournament_pop = Population(0)
#         i = 0
#         while i < TOURNAMENT_SELECTION_SIZE:
#             tournament_pop.get_jadwals().append(pop.get_jadwals()[rnd.randrange(0, POPULATION_SIZE)])
#             i += 1
#         tournament_pop.get_jadwals().sort(key=lambda x: x.get_fitness(), reverse=True)
#         return tournament_pop

# def context_manager(jadwal):
#     classes = jadwal.get_classes()
#     context = []
#     cls = {}
#     for i in range(len(classes)):
#         cls["section"] = classes[i].section_id
#         cls['kelas'] = classes[i].kelasbeta.nama_kelas
#         cls['matapelajaran'] = f'{classes[i].matapelajaran.nama_pelajaran} ({classes[i].matapelajaran.no_pelajaran}, ' \
#                             f'{classes[i].matapelajaran.max_jumalah_siswa}'
#         cls['ruangan'] = f'{classes[i].ruangan.r_number} ({classes[i].ruangan.r_kapasistas})'
#         cls['guru'] = f'{classes[i].guru.nama} ({classes[i].guru.gid})'
#         cls['waktubelajar'] = [classes[i].waktubelajar.wid, classes[i].waktubelajar.hari, classes[i].waktubelajar.jam]
#         context.append(cls)
#     return context


# def timetabel(request):
#     jadwal = []
#     population = Population(POPULATION_SIZE)
#     generation_num = 0
#     population.get_jadwals().sort(key=lambda x: x.get_fitness(), reverse=True)
#     genetikaAlgo = Genetika()
#     while population.get_jadwals()[0].get_fitness() != 1.0:
#         generation_num += 1
#         print('\n> Generasi #' + str(generation_num))
#         population = genetikaAlgo.evolve(population)
#         population.get_jadwals().sort(key=lambda x: x.get_fitness(), reverse=True)
#         jadwal = population.get_jadwals()[0].get_classes()

#     return render(request, 'penjadwalan/algoritma/timetabel.html', {'jadwal': jadwal, 'sections': Section.objects.all(),
#                                               'waktu': WaktuBelajar.objects.all()})