import numpy


def printer(text):
    largo = (len(text))
    print("┏" + "━" * largo + "┓")
    print("{:┃^{width}}".format(text, width=largo + 2))
    print("┗"+"━" * largo + "┛")


def find_first_maximum(tf):
    first_max = None
    for i in range(3, len(tf)):
        print(tf[i])
        if tf[i] > tf[i-1] and tf[i] > tf[i+1]:
            first_max = i
            break

    return first_max


def rect_window(ft, delta):
    ventana = numpy.zeros(len(ft), dtype=complex)
    largo = len(ventana)

    ventana[0:delta] = ft[0:delta]
    ventana[largo-delta:largo] = ft[largo-delta:largo]

    return ventana

def bass_filter(ft, frecuency_axis, freq):
    ventana = numpy.zeros(len(ft), dtype=complex)
    largo = len(ventana)
    #encontrar la frecuencia mas cercana si el elemento no esta en el eje de la frecuencia, busqueda secuencial por ahora
    if freq not in frecuency_axis:
        for f in frecuency_axis:
            if f > freq:
                freq = f
                print(freq)
                break
    delta = frecuency_axis.tolist().index(freq)
    ventana[delta:-delta] = ft[delta:-delta]
    return ventana

def window_in_db(fft):

    fft_norm = abs(fft) / max(abs(fft))

    return 20 * numpy.log10(fft_norm)