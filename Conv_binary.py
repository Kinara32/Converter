from DefaultSegyHeader import getDefaultSegyHeader, getDefaultSegyTraceHeaders, writeSegyStructure, \
    getDefaultSegyDataBin,getDefaultGPSData

ns = 5000                   # Количество отсчетов в одной трассе # Number of samples per data trace
numsensors = 96             # Количество датчиков
numsensors_nonzero = 8      # Номер датчика для построения разреза с одного канала
delay = 1800*100            # Задержка записи после выстрела пушки в нс * множитель пакета !!!

Job = 1     # Номер работы
Line = 2    # Номер профиля
Reel = 2    # Номер косы
Day = 25    # День !!!

distance = 15625        #1.5625 м Расстояние между датчиками
offset = 160000         # 16 м Отдаление источника от приемника
SourceWaterDepth = 70   # Глубина воды под источником
SourceX = 33010181      # Координаты источника  4 день 33 06.4545  2 день 33 01.0178 5 день 33 01.0181 !!!
SourceY = 69004687      # Координаты источника  4 день 69 03.3662  2 день 69 00.4683 5 день 69 00.4687!!!
GroupX = 0              # Координаты приемника
GroupY = 0              # Координаты приемника

sensorsAll = 1  # Если 1, то строит все датчики
readAll = 0     # Если 1, то читает весь файл
sortFlag = 1    # Флаг сортировки Если 1, то сортирует датчики Если 2, то выбран один датчик для разреза
pack_in = 5     # Если readAll = 1, то игнорирует эту строку # Количество пакетов в записи # Должно быть кратно и не меньше ns, и не больше чем пакетов в файле

dt = 100        # Шаг дискретизации в микросекундах для всего файла
# STH_dt = 200  # Шаг дискретизации в микросекундах для трасс # Лучше не трогать
format = '>f'   # Формат данных
sizep = 408     # Размер пакета данных
sizeCanon = 120 # Размер пакета данных пушки
sizeGPS = 126   # Размер пакета GPS

Time_Length = ns * dt * (10 ** (-3))

textheader = 'Murmansk\n25 October 2019 8:58:23\nFormat GPS: Degrees and decimal minutes      \nSource coordinate X: 33 01.0181\nSource coordinate Y: 69 00.4687\n' \
             'Offset = 16 m  \nDistances between sensors = 1.5625 m\nNumber of samples per data trace = ' + str(ns) + ' ns\nNumber of sensors = ' + str(numsensors) + \
             '\nRecording delay after gun shot = 2000 ns                \nSampling frequency = 10 000 Hz\nWater depth under source = 70 m'

dir_name = 'C:\Matvey\Day_4_(24.10.2019)\ITMO\\'
#filename_gps = 'D:\ITMO\GPS_data_Thu_Oct_24_2019_12_44_36.bin'
filename_cannon = dir_name + 'Cannon_data_Thu_Oct_24_2019_12_04_49.bin'
filename_bin = dir_name + 'Kosa_data_Thu_Oct_24_2019_12_04_49.bin'       # BIN\Day_(21.10.2019)\ITMO\  # 'Kosa_data_Sat_Oct_19_2019_15_58_42.bin' # 'geokosa_data.bin'  # 'kosa_data_13_26_02.bin' #'Kosa_data_Tue_Oct_15_2019_16_41_30.bin'
filename_sgy = 'SEGY\Kosa_data_Thu_Oct_24_2019_12_04_49_final.sgy'  # C:\Matvey\Segy\Data_last\Day_(22.10.2019)SEGY\

#Gps = getDefaultGPSData(filename_gps, readAll, pack_in, sizeGPS)

Data_segy, ntraces = getDefaultSegyDataBin(filename_bin, filename_cannon, numsensors, numsensors_nonzero, ns, pack_in,
                                           sizeCanon,
                                           format, readAll,
                                           sortFlag, delay, sensorsAll)
SH = getDefaultSegyHeader(numsensors,numsensors_nonzero, ntraces, ns, dt, Job, Line, Reel, sensorsAll)
STH = getDefaultSegyTraceHeaders(numsensors,numsensors_nonzero, distance, ntraces, ns, dt, offset, SourceWaterDepth, SourceX,
                                 SourceY,
                                 GroupX,
                                 GroupY, Day, sensorsAll)
writeSegyStructure(filename_sgy, Data_segy, textheader, SH, STH)
