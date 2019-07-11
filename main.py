from scipy.io import wavfile
import numpy
import wfdb
import matplotlib.pyplot as plot
from scipy.signal import find_peaks


def printer(text):
    largo = (len(text))
    print("┏" + "━" * largo + "┓")
    print("{:┃^{width}}".format(text, width=largo + 2))
    print("┗"+"━" * largo + "┛")


class Signal:
    def __init__(self, fs, data, pulsos_por_tajada):
        self._time_cut = 20
        self._original_data = data
        self._fs = fs
        self._pulsos_por_tajada = pulsos_por_tajada

        # recortar hasta tener n pulsos
        while(True):
            pulsos_peaks = self.find_pulse_peaks(self.data())
            if(len(pulsos_peaks[0]) <= self._pulsos_por_tajada):
                break
            self._time_cut = self._time_cut - 0.25

        pulsos_tiempo = pulsos_peaks[0] / self.fs()
        pulsos = pulsos_peaks[1]["peak_heights"]
        self._pulsos = (pulsos_tiempo, pulsos)

    def fs(self):
        return self._fs

    def original_data(self):
        return self._original_data

    def data(self):
        return self.original_data()[:int(self._time_cut * self.fs())]

    def n_original_samples(self):
        return len(self.original_data())

    def n_samples(self):
        return len(self.data())

    def duration(self):
        return self.n_samples() / self.fs()

    def original_time(self):
        return numpy.arange(0, self.n_original_samples())/self.fs()

    def time(self):
        return numpy.arange(0, self.n_samples())/self.fs()

    def arrhythmia_detector(self):
        segundos_tajada = 20
        inicio = self.fs()*0
        fin = int(self.fs()*segundos_tajada)
        ecg = self.original_data()[inicio:fin]
        time = time_original[inicio:fin]
        pulsos_peaks = self.find_pulse_peaks(self.original_data())[0]
        intervalos = []
        for i in range(len(pulsos_peaks)-1, 0, -1):
            intervalos.append(pulsos_peaks[i]-pulsos_peaks[i-1])
        margen = 0.30  # porcentaje
        for i in range(len(intervalos)-1, 0, -1):
            if(abs(intervalos[i] - intervalos[i-1]) >= margen * max(intervalos[i], intervalos[i-1])):
                return True
        return False

    def pulsos(self, n):
        return self._pulsos

    def transform_original(self):
        freq_axis = numpy.fft.fftfreq(ecg.n_original_samples()) * ecg.fs()
        transform = numpy.fft.fft(ecg.original_data()) / \
            ecg.n_original_samples()
        return (transform, freq_axis)

    def transform(self):
        freq_axis = numpy.fft.fftfreq(ecg.n_samples()) * ecg.fs()
        transform = numpy.fft.fft(ecg.data()) / ecg.n_samples()
        return (transform, freq_axis)

    def cardiac_frequency(self):
        maximo = find_first_maximum(transformada)
        frecuencia_cardiaca = frecuencias[maximo]
        return frecuencia_cardiaca

    def find_pulse_peaks(self, data):
        height = max(data)*0.8
        return find_peaks(data, height=height)


class File_Handler:
    def __init__(self):
        def read_wav_file(wav_file_name):
            fs, data = wavfile.read(wav_file_name, mmap=False)
            return (fs, data)

        def read_dat_file(dat_file_name):
            dat_file_name = dat_file_name[:dat_file_name.find(".")]
            record = wfdb.rdrecord(dat_file_name)
            return (record.fs, [x[0] for x in record.p_signal])

        self.readers = {"wav": read_wav_file,
                        "dat": read_dat_file}

    def read_signal_file(self, filename, pulsos_por_tajada):
        def file_extension(filename):
            return filename[filename.find(".")+1:]

        ext = file_extension(filename)
        if(ext not in self.readers):
            raise "Invalid file extension:" + ext
        fs, data = self.readers[ext](filename)
        signal = Signal(fs, data, pulsos_por_tajada)
        return signal


def find_first_maximum(tf):
    first_max = None
    for i in range(3, len(tf)):
        if tf[i] > 0.005 and tf[i] > tf[i-1] and tf[i] > tf[i+1]:
            first_max = i
            break

    return first_max


def rect_window(ft, delta):
    ventana = numpy.zeros(len(ft))
    largo = len(ventana)

    ventana[0:delta] = ft[0:delta]
    ventana[largo-delta:largo] = ft[largo-delta:largo]

    return ventana


filename = "arritmia\\100.dat"
#filename = "ruido\\aami3d.dat"
#filename = "picos_abajo\\aami3a.dat"
#filename = "ilegible\\f0005.wav"
#filename = "normal\\aami4b_d.dat"
#filename = "normal\\aami4b_h.dat"

lector = File_Handler()
pulsos_por_tajada = 3
ecg = lector.read_signal_file(filename, pulsos_por_tajada)

time_original = ecg.original_time()

(pulsos_tiempo, pulsos) = ecg.pulsos(pulsos_por_tajada)

if(ecg.arrhythmia_detector()):
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

if(frecuencia_cardiaca > 1.6):
    printer("Taquicardia")
elif(frecuencia_cardiaca < 1):
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
