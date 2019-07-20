from tools.Visualizador import Visualizador
from tools.Signal import Signal

'''
Muestras de adulto arritmico

filename = "arritmia/105.dat"
filename = "arritmia/108.dat"
filename = "arritmia/119.dat"
filename = "arritmia/200.dat"
filename = "arritmia/201.dat"
filename = "arritmia/203.dat"

Muestras de adulto con bradicardia
filename = "arritmia/123.dat"
filename = "arritmia/124.dat"
filename = "arritmia/202.dat"

Muestras de adulto normales

filename = "normal/aami4b_d.dat"
filename = "normal/aami4b_h.dat"

Muestras de FECG

filename = "fetal/NR_01.dat" # OK
filename = "fetal/ARR_08.dat" # OK
filename = "fetal/ARR_05.dat" # Muchos P
filename = "fetal/ARR_03.dat" # Falta P
filename = "fetal/NR_04.dat"
'''
filename = "fetal/NR_04.dat"

tiempo_limite = 30

ecg = Signal(filename, tiempo_limite)

visualizador = Visualizador(ecg)
visualizador.imprimir_informacion()