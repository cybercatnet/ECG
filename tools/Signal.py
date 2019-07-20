import numpy
from scipy.signal import find_peaks
import scipy.signal as signal


class Signal:
    def __init__(self, fs, data, time_cut_seg):

        self._bass_filter = 2
        self._treble_filter = 45
        self._porcentaje_desde_maximo_peaks = 0.3
        self._max_freq_taquicardia_lpm = 300

        self._time_cut_seg = time_cut_seg
        self._fs = fs
        self._cardiac_frequency = None
        self._pulsos = None
        self._has_arritmia = None
        self._data = None

        self.normalize_signal(data)
        self.find_pulses()

        self._transform, self._frequency = self.transform()
        self.cardiac_frequency()

    def printer(self, text):
        largo = (len(text))
        print("┏" + "━" * largo + "┓")
        print("{:┃^{width}}".format(text, width=largo + 2))
        print("┗"+"━" * largo + "┛")

    def bass_filter(self):
        if self._bass_filter <= 0:
            return
        ft, frecuency_axis = self.transform()
        ft_filtered = numpy.zeros(len(ft), dtype=complex)
        largo = len(ft_filtered)
        # encontrar la frecuencia mas cercana si el elemento no esta en el eje de la frecuencia, busqueda secuencial por ahora
        if self._bass_filter not in frecuency_axis:
            for f in frecuency_axis:
                if f > self._bass_filter:
                    self._bass_filter = f
                    break
        if self._bass_filter not in frecuency_axis:
            self._bass_filter = 0
        delta = frecuency_axis.tolist().index(self._bass_filter)
        ft_filtered[delta + 1:-delta] = ft[delta + 1:-delta]
        self._data = self.antitransform(ft_filtered)

    def treble_filter(self):
        ft, frecuency_axis = self.transform()
        ft_filtered = numpy.zeros(len(ft), dtype=complex)
        largo = len(ft_filtered)
        # encontrar la frecuencia mas cercana si el elemento no esta en el eje de la frecuencia, busqueda secuencial por ahora
        if self._treble_filter not in frecuency_axis:
            for f in frecuency_axis:
                if f > self._treble_filter:
                    self._treble_filter = f
                    break
        if self._treble_filter not in frecuency_axis:
            self._treble_filter = max(frecuency_axis)
        delta = frecuency_axis.tolist().index(self._treble_filter)
        ft_filtered[:delta] = ft[:delta]
        ft_filtered[-delta + 1:] = ft[-delta + 1:]
        self._data = self.antitransform(ft_filtered)

    def passband_filter(self, data, low_cut_hz, high_cut_hz):
        low_cut = low_cut_hz / (self._fs / 2)
        high_cut = high_cut_hz / (self._fs / 2)
        b, a = signal.butter(4, [low_cut, high_cut], 'bandpass')

        return signal.filtfilt(b, a, data)

    def normalize_signal(self, original_data):
        self._data = original_data[:int(self._time_cut_seg * self.fs())]
        self._data = self.passband_filter(self._data, self._bass_filter, self._treble_filter)

    def find_pulses(self):
        pulsos_peaks = self.find_pulse_peaks(self.data())

        pulsos_tiempo = pulsos_peaks[0] / self.fs()
        pulsos = pulsos_peaks[1]["peak_heights"]

        self._pulsos = (pulsos_tiempo, pulsos)

    def fs(self):
        return self._fs

    def data(self):
        return self._data

    def n_samples(self):
        return len(self.data())

    def duration(self):
        return self.n_samples() / self.fs()

    def time(self):
        return numpy.arange(0, self.n_samples()) / self.fs()

    def arrhythmia_detector(self):
        pulsos_peaks = self.pulsos()[0]
        intervalos = []

        for i in range(len(pulsos_peaks) - 1, 0, -1):
            intervalos.append(pulsos_peaks[i] - pulsos_peaks[i - 1])

        margen = 0.20  # porcentaje

        arritmias = 0

        for i in range(len(intervalos) - 1, 0, -1):
            if abs(intervalos[i] - intervalos[i - 1]) >= margen * max(intervalos[i], intervalos[i - 1]):
                arritmias = arritmias + 1

        return arritmias > len(pulsos_peaks) * 0.10

    def pulsos(self):
        return self._pulsos

    def transform(self):
        freq_axis = numpy.fft.fftfreq(self.n_samples()) * self.fs()
        transform = numpy.fft.fft(self.data()) / self.n_samples()

        return transform, freq_axis

    def antitransform(self, data):
        return numpy.fft.ifft(data) * self.n_samples()

    def cardiac_frequency(self):
        pulsos = self.pulsos()[0]
        tiempo = pulsos[-1] - pulsos[0]

        self._cardiac_frequency = len(pulsos) / tiempo

        return self._cardiac_frequency

    def find_pulse_peaks(self, data):
        height = max(data) - (max(data) - min(data)) * self._porcentaje_desde_maximo_peaks
        distance = 1/(self._max_freq_taquicardia_lpm/60) * self.fs()

        return find_peaks(data, height=height, distance=distance)

    def detect_arritmia(self):
        self._has_arritmia = self.arrhythmia_detector()

        if self._has_arritmia:
            self.printer("Arritmia Detectada")
        else:
            self.printer("Arritmia No Detectada")

        return self._has_arritmia

    def qualify_cardiac_freq(self):
        if (self._cardiac_frequency * 60) > 100:
            self.printer("Taquicardia")
        elif (self._cardiac_frequency * 60) < 60:
            self.printer("Bradicardia")
        else:
            self.printer("Normal")

    def print_cardiac_frequency(self):
        self.printer("Frecuencia Cardíaca: " +
                str(self._cardiac_frequency * 60) + " ppm")

    def get_transform_values(self):
        return self._transform

    def get_frequency_values(self):
        return self._frequency
