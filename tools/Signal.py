import numpy
from scipy.signal import find_peaks

from tools.utils import find_first_maximum, printer


class Signal:
    def __init__(self, fs, data, pulsos_por_tajada):
        self._bass_filter = 1
        self._treble_filter = 50
        self._porcentaje_desde_maximo_peaks = 0.05
        self._max_freq_taquicardia_lpm = 300
        self._min_freq_bradicardia_lpm = 30
        self._max_latidos_inicial = 20
        self._time_cut_seg = self._max_latidos_inicial * \
            self._min_freq_bradicardia_lpm / 60
        self._original_data = data
        self._fs = fs
        self._pulsos_por_tajada = pulsos_por_tajada
        self._cardiac_frequency = None
        self._pulsos = None
        self._transform_original = None
        self._frequency_original = None
        self._has_arritmia = None
        self.normalize_signal()
        self.find_pulses()

        self._transform, self._frequency = self.transform()
        self.cardiac_frequency()

    def bass_filter(self):
        ft, frecuency_axis = self.transform()
        ft_filtered = numpy.zeros(len(ft), dtype=complex)
        largo = len(ft_filtered)
        # encontrar la frecuencia mas cercana si el elemento no esta en el eje de la frecuencia, busqueda secuencial por ahora
        if self._bass_filter not in frecuency_axis:
            for f in frecuency_axis:
                if f > self._bass_filter:
                    self._bass_filter = f
                    break
            self._bass_filter = min(frecuency_axis)
        delta = frecuency_axis.tolist().index(self._bass_filter)
        ft_filtered[delta:-delta] = ft[delta:-delta]
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
            self._treble_filter = max(frecuency_axis)
        delta = frecuency_axis.tolist().index(self._treble_filter)
        ft_filtered[:delta] = ft[:delta]
        ft_filtered[-delta:] = ft[-delta:]
        self._data = self.antitransform(ft_filtered)
        

    def normalize_signal(self):
        self._data = self._original_data[:int(self._time_cut_seg * self.fs())]
        self.bass_filter()
        self.treble_filter()

    def find_pulses(self):
        # ajuste de porcentaje desde el maximo
        while True:
            pulsos_peaks = self.find_pulse_peaks(self.data())
            if len(pulsos_peaks[0]) > self._max_latidos_inicial:
                break
            if self._porcentaje_desde_maximo_peaks > 0.2:
                break
            self._porcentaje_desde_maximo_peaks = self._porcentaje_desde_maximo_peaks + 0.05
        # recortar tiempo hasta tener n pulsos
        while True:
            pulsos_peaks = self.find_pulse_peaks(self.data())
            if len(pulsos_peaks[0]) <= self._pulsos_por_tajada:
                break
            self._time_cut_seg = self._time_cut_seg - 0.25
            if self._time_cut_seg < 4:
                break
        pulsos_tiempo = pulsos_peaks[0] / self.fs()
        pulsos = pulsos_peaks[1]["peak_heights"]
        self._pulsos = (pulsos_tiempo, pulsos)

    def fs(self):
        return self._fs

    def original_data(self):
        return self._original_data

    def data(self):
        return self._data

    def n_original_samples(self):
        return len(self.original_data())

    def n_samples(self):
        return len(self.data())

    def duration(self):
        return self.n_samples() / self.fs()

    def original_time(self):
        return numpy.arange(0, self.n_original_samples()) / self.fs()

    def time(self):
        return numpy.arange(0, self.n_samples()) / self.fs()

    def arrhythmia_detector(self):
        pulsos_peaks = self.find_pulse_peaks(self.original_data())[0]
        intervalos = []

        for i in range(len(pulsos_peaks) - 1, 0, -1):
            intervalos.append(pulsos_peaks[i] - pulsos_peaks[i - 1])

        margen = 0.30  # porcentaje

        arritmias = 0

        for i in range(len(intervalos) - 1, 0, -1):
            if abs(intervalos[i] - intervalos[i - 1]) >= margen * max(intervalos[i], intervalos[i - 1]):
                arritmias = arritmias + 1
        
        return arritmias > len(pulsos_peaks) * 0.25

    def pulsos(self):
        return self._pulsos

    def transform_original(self):
        freq_axis = numpy.fft.fftfreq(self.n_original_samples()) * self.fs()
        transform = numpy.fft.fft(self.original_data()) / \
            self.n_original_samples()

        self._transform_original = transform
        self._frequency_original = freq_axis

        return transform, freq_axis

    def transform(self):
        freq_axis = numpy.fft.fftfreq(self.n_samples()) * self.fs()
        transform = numpy.fft.fft(self.data()) / self.n_samples()

        return transform, freq_axis

    def antitransform(self, data):
        return numpy.fft.ifft(data) * self.n_samples()

    def cardiac_frequency(self):
        maximo = find_first_maximum(self._transform)
        print(maximo)
        self._cardiac_frequency = self._frequency[maximo]

        return self._cardiac_frequency

    def find_pulse_peaks(self, data):
        height = max(data) - (max(data) - min(data)) * \
            self._porcentaje_desde_maximo_peaks
        distance = 1/(self._max_freq_taquicardia_lpm/60) * self.fs()
        return find_peaks(data, height=height, distance=distance)

    def detect_arritmia(self):
        self._has_arritmia = self.arrhythmia_detector()

        if self._has_arritmia:
            printer("Arritmia Detectada")
        else:
            printer("Arritmia No Detectada")

        return self._has_arritmia

    def qualify_cardiac_freq(self):
        if self._cardiac_frequency > 1.6:
            printer("Taquicardia")
        elif self._cardiac_frequency < 1:
            printer("Bradicardia")
        else:
            printer("Normal")

    def print_cardiac_frequency(self):
        printer("Frecuencia Cardíaca: " +
                str(self._cardiac_frequency * 60) + " ppm")

    def get_transform_values(self):
        return self._transform

    def get_frequency_values(self):
        return self._frequency