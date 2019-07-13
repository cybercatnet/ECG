import matplotlib.pyplot as plot
import numpy

from tools.FileHandler import FileHandler
from tools.utils import rect_window, window_in_db

filename = "arritmia/100.dat"
# filename = "ruido\\aami3d.dat"
# filename = "picos_abajo\\aami3a.dat"
# filename = "ilegible/f0005.wav"
# filename = "normal/aami4b_d.dat"
# filename = "normal/aami4b_h.dat"
# filename = "fetal/1001.dat"
# filename1 = "fetal/ARR_01.dat"
filename1 = "fetal/NR_01.dat"

lector = FileHandler()
pulsos_por_tajada = 10
ecg = lector.read_signal_file(filename, pulsos_por_tajada)
ecg2 = lector.read_signal_file(filename1, pulsos_por_tajada)


ecg.detect_arritmia()
ecg.print_cardiac_frequency()
ecg.qualify_cardiac_freq()

ecg2.detect_arritmia()
ecg2.print_cardiac_frequency()
ecg2.qualify_cardiac_freq()

pulsos_tiempo, pulsos = ecg.pulsos()
pulsos_tiempo2, pulsos2 = ecg2.pulsos()

transformada_original, frecuencias_original = ecg.transform_original()

transformada = ecg.get_transform_values()
frecuencias = ecg.get_frequency_values()

transformada_ventaneada = rect_window(transformada, 5)
transformada_ventaneada2 = rect_window(ecg2.get_transform_values(), 5)

ventana_en_tiempo = numpy.fft.fft(transformada_ventaneada)

_, subplot = plot.subplots(3, 1)

n = 0

subplot[n].plot(ecg.original_time(), ecg.original_data())
subplot[n].plot(ecg2.original_time(), ecg2.original_data())
subplot[n].set_xlabel('Tiempo')
subplot[n].set_ylabel('Amplitud')
subplot[n].title.set_text("Señal Original")

subplot[n].plot(pulsos_tiempo, pulsos, "ro")
subplot[n].plot(pulsos_tiempo2, pulsos2, "go")

n = n + 1

subplot[n].plot(ecg.time(), ecg.data())
subplot[n].plot(ecg2.time(), ecg2.data())
subplot[n].set_xlabel('Tiempo')
subplot[n].set_ylabel('Amplitud')
subplot[n].title.set_text("Señal Recortada")

subplot[n].plot(pulsos_tiempo, pulsos, "ro")
subplot[n].plot(pulsos_tiempo2, pulsos2, "go")
n = n + 1

subplot[n].plot(frecuencias, transformada_ventaneada)
subplot[n].plot(ecg2.get_frequency_values(), transformada_ventaneada2)
subplot[n].set_xlabel('Frecuencia')
subplot[n].set_ylabel('Modulo')
subplot[n].title.set_text("Transformada Ventaneada de la Señal Recortada")
'''
n = n + 1

subplot[n].plot(ecg.time(), ventana_en_tiempo)
subplot[n].set_xlabel('Tiempo')
subplot[n].set_ylabel('Amplitud')
subplot[n].title.set_text("Transformada Inversa de la Ventana Recortada")
'''
[x.grid() for x in subplot]

# plot.tight_layout()
plot.show()
