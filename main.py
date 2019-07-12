import matplotlib.pyplot as plot
import numpy

from tools.FileHandler import FileHandler
from tools.utils import printer, rect_window

filename = "arritmia/100.dat"
# filename = "ruido\\aami3d.dat"
# filename = "picos_abajo\\aami3a.dat"
# filename = "ilegible\\f0005.wav"
# filename = "normal\\aami4b_d.dat"
# filename = "normal\\aami4b_h.dat"

lector = FileHandler()
pulsos_por_tajada = 3
ecg = lector.read_signal_file(filename, pulsos_por_tajada)

time_original = ecg.original_time()

(pulsos_tiempo, pulsos) = ecg.pulsos(pulsos_por_tajada)

if ecg.arrhythmia_detector():
    printer("Arritmia Detectada")
else:
    printer("Arritmia No Detectada")

'''
Teniendo en cuenta que el latido normal
1 latido por segundo
a
1,66 latido por segundo
Hay que tomar al menos 10 segundos de muestras
'''

transformada_original, frecuencias_original = ecg.transform_original()

transformada, frecuencias = ecg.transform()

transformada_ventaneada = rect_window(transformada, 5)

frecuencia_cardiaca = ecg.cardiac_frequency()

printer("Frecuencia Cardíaca: " + str(frecuencia_cardiaca * 60) + " ppm")

if frecuencia_cardiaca > 1.6:
    printer("Taquicardia")
elif frecuencia_cardiaca < 1:
    printer("Bradicardia")
else:
    printer("Normal")

ventana_en_tiempo = numpy.fft.fft(transformada_ventaneada)

_, subplot = plot.subplots(4, 1)

n = 0

subplot[n].plot(ecg.original_time(), ecg.original_data())
subplot[n].set_xlabel('Tiempo')
subplot[n].set_ylabel('Amplitud')
subplot[n].title.set_text("Señal Original")

subplot[n].plot(pulsos_tiempo, pulsos, "ro")

n = n + 1

subplot[n].plot(ecg.time(), ecg.data())
subplot[n].set_xlabel('Tiempo')
subplot[n].set_ylabel('Amplitud')
subplot[n].title.set_text("Señal Recortada")

subplot[n].plot(pulsos_tiempo, pulsos, "ro")

n = n + 1

subplot[n].plot(frecuencias, abs(transformada))
subplot[n].set_xlabel('Frecuencia')
subplot[n].set_ylabel('Modulo')
subplot[n].title.set_text("Transformada Ventaneada de la Señal Recortada")

n = n + 1

subplot[n].plot(ecg.time(), ventana_en_tiempo)
subplot[n].set_xlabel('Tiempo')
subplot[n].set_ylabel('Amplitud')
subplot[n].title.set_text("Transformada Inversa de la Ventana Recortada")

[x.grid() for x in subplot]

plot.tight_layout()
plot.show()
