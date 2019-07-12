import numpy
from scipy.signal import find_peaks

from tools.utils import find_first_maximum


class Signal:
    def __init__(self, fs, data, pulsos_por_tajada):
        self._time_cut = 20
        self._original_data = data
        self._fs = fs
        self._pulsos_por_tajada = pulsos_por_tajada

        # recortar hasta tener n pulsos
        while True:
            pulsos_peaks = self.find_pulse_peaks(self.data())
            if len(pulsos_peaks[0]) <= self._pulsos_por_tajada:
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
        time = self.original_time()[inicio:fin]
        pulsos_peaks = self.find_pulse_peaks(self.original_data())[0]
        intervalos = []

        for i in range(len(pulsos_peaks)-1, 0, -1):
            intervalos.append(pulsos_peaks[i]-pulsos_peaks[i-1])

        margen = 0.30  # porcentaje

        for i in range(len(intervalos)-1, 0, -1):
            if abs(intervalos[i] - intervalos[i - 1]) >= margen * max(intervalos[i], intervalos[i - 1]):
                return True
        return False

    def pulsos(self, n):
        return self._pulsos

    def transform_original(self):
        freq_axis = numpy.fft.fftfreq(self.n_original_samples()) * self.fs()
        transform = numpy.fft.fft(self.original_data()) / \
            self.n_original_samples()

        return transform, freq_axis

    def transform(self):
        freq_axis = numpy.fft.fftfreq(self.n_samples()) * self.fs()
        transform = numpy.fft.fft(self.data()) / self.n_samples()

        return transform, freq_axis

    def cardiac_frequency(self):
        transformada, frecuencias = self.transform()

        maximo = find_first_maximum(transformada)
        frecuencia_cardiaca = frecuencias[maximo]

        return frecuencia_cardiaca

    def find_pulse_peaks(self, data):
        height = max(data)*0.8

        return find_peaks(data, height=height)
