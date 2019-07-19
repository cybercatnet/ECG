import matplotlib.pyplot as plot
import numpy
from biosppy.signals import ecg as ecg_biosppy

from tools.FileHandler import FileHandler
from tools.utils import rect_window, window_in_db

# filename = "arritmia/100.dat"
# filename = "ruido/aami3d.dat"
# filename = "picos_abajo/aami3a.dat"
# filename = "normal/aami4b_d.dat"
# filename = "normal/aami4b_h.dat"
# filename = "fetal/1001.dat"
# filename1 = "fetal/ARR_01.dat"
# filename1 = "fetal/NR_01.dat" # OK
# filename = "fetal/ARR_08.dat" # OK
# filename = "fetal/ARR_05.dat" # Muchos P
# filename = "fetal/ARR_03.dat" # Falta P
# filename = "fetal/NR_03.dat" # Maso
filename = "fetal/NR_04.dat"

lector = FileHandler()
tiempo_limite = 30
ecg, fs, data_original = lector.read_signal_file(filename, tiempo_limite)
# ecg2, fs2, data_original2 = lector.read_signal_file(filename1, tiempo_limite)


ecg.detect_arritmia()
ecg.print_cardiac_frequency()
ecg.qualify_cardiac_freq()

#ecg2.detect_arritmia()
#ecg2.print_cardiac_frequency()
#ecg2.qualify_cardiac_freq()

pulsos_tiempo, pulsos = ecg.pulsos()
#pulsos_tiempo2, pulsos2 = ecg2.pulsos()

transformada = ecg.get_transform_values()
frecuencias = ecg.get_frequency_values()

_, subplot = plot.subplots(3, 1)

n = 0

subplot[n].plot(numpy.arange(0, len(data_original)) / fs, data_original)
#subplot[n].plot(numpy.arange(0, len(data_original2)) / fs2, data_original2)
subplot[n].set_xlabel('Tiempo')
subplot[n].set_ylabel('Amplitud')
subplot[n].title.set_text("Señal Original")

n = n + 1

subplot[n].plot(ecg.time(), ecg.data())
#subplot[n].plot(ecg2.time(), ecg2.data())
subplot[n].set_xlabel('Tiempo')
subplot[n].set_ylabel('Amplitud')
subplot[n].title.set_text("Señal Recortada")

subplot[n].plot(pulsos_tiempo, pulsos, "ro")
#subplot[n].plot(pulsos_tiempo2, pulsos2, "go")
n = n + 1

trans1, freq1 = ecg.transform()
#trans2, freq2 = ecg2.transform()

subplot[n].plot(freq1, trans1)
#subplot[n].plot(freq2, trans2)
subplot[n].set_xlabel('Frecuencia')
subplot[n].set_ylabel('Modulo')
subplot[n].title.set_text("Transformada Ventaneada de la Señal Recortada")
'''

n = n + 1

subplot[n].plot(ecg2.time(), ventana_en_tiempo2)
subplot[n].set_xlabel('Tiempo')
subplot[n].set_ylabel('Amplitud')
subplot[n].title.set_text("Transformada Inversa de la Ventana Recortada")
'''
[x.grid() for x in subplot]

# plot.tight_layout()
plot.show()
