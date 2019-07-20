import matplotlib.pyplot as plot

class Visualizador:

    def __init__(self, ecg):
        self.ecg = ecg

    def imprimir_informacion(self):
        self.print_arritmia_presence()
        self.print_cardiac_frequency()
        self.print_qualify_cardiac_freq()

        pulsos_tiempo, pulsos = self.ecg.pulsos()

        transformada = self.ecg.get_transform_values()
        frecuencias = self.ecg.get_frequency_values()

        _, subplot = plot.subplots(3, 1)

        n = 0

        subplot[n].plot(self.ecg.time_original(), self.ecg.data_original())
        subplot[n].set_xlabel('Tiempo')
        subplot[n].set_ylabel('Amplitud')
        subplot[n].title.set_text("Señal Original")

        n = n + 1

        subplot[n].plot(self.ecg.time(), self.ecg.data())
        subplot[n].set_xlabel('Tiempo')
        subplot[n].set_ylabel('Amplitud')
        subplot[n].title.set_text("Señal recortada y filtrada")

        subplot[n].plot(pulsos_tiempo, pulsos, "ro")
        n = n + 1

        trans1, freq1 = self.ecg.transform()

        subplot[n].plot(freq1, trans1)
        subplot[n].set_xlabel('Frecuencia')
        subplot[n].set_ylabel('Modulo')
        subplot[n].title.set_text("Transformada de la señal recortada y filtrada")

        [x.grid() for x in subplot]

        plot.tight_layout()
        plot.show()

    def print_arritmia_presence(self):
        has_arritmia = self.ecg.arrhythmia_detector()

        if has_arritmia:
            self.printer("Arritmia por regularidad: Detectada")
        else:
            self.printer("Arritmia por regularidad: No Detectada")

        return has_arritmia

    def print_qualify_cardiac_freq(self):
        if (self.ecg._cardiac_frequency * 60) > 100:
            self.printer("Pulso alto, tiene Taquicardia")
        elif (self.ecg._cardiac_frequency * 60) < 60:
            self.printer("Pulso bajo, tiene Bradicardia")
        else:
            self.printer("Pulso Normal")

    def print_cardiac_frequency(self):
        self.printer("Frecuencia Cardíaca: " + '{:2.2f}'.format(self.ecg._cardiac_frequency * 60) + " ppm")

    def printer(self, text):
        largo = (len(text))
        print("┏" + "━" * largo + "┓")
        print("{:┃^{width}}".format(text, width=largo + 2))
        print("┗"+"━" * largo + "┛")