import matplotlib.pyplot as plot
import numpy

class Visualizador:

    def imprimir_informacion(self, ecg, fs, data_original):
        ecg.detect_arritmia()
        ecg.print_cardiac_frequency()
        ecg.qualify_cardiac_freq()

        pulsos_tiempo, pulsos = ecg.pulsos()

        transformada = ecg.get_transform_values()
        frecuencias = ecg.get_frequency_values()

        _, subplot = plot.subplots(3, 1)

        n = 0

        subplot[n].plot(numpy.arange(0, len(data_original)) / fs, data_original)
        subplot[n].set_xlabel('Tiempo')
        subplot[n].set_ylabel('Amplitud')
        subplot[n].title.set_text("Señal Original")

        n = n + 1

        subplot[n].plot(ecg.time(), ecg.data())
        subplot[n].set_xlabel('Tiempo')
        subplot[n].set_ylabel('Amplitud')
        subplot[n].title.set_text("Señal recortada y filtrada")

        subplot[n].plot(pulsos_tiempo, pulsos, "ro")
        n = n + 1

        trans1, freq1 = ecg.transform()

        subplot[n].plot(freq1, trans1)
        subplot[n].set_xlabel('Frecuencia')
        subplot[n].set_ylabel('Modulo')
        subplot[n].title.set_text("Transformada de la señal recortada y filtrada")

        [x.grid() for x in subplot]

        plot.tight_layout()
        plot.show()