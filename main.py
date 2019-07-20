from tools.Visualizador import Visualizador
from tools.Signal import Signal

'''
Muestras de adulto arritmico

filename = "arritmia/100.dat"

Muestras de adulto normales

filename = "normal/aami4b_d.dat"
filename = "normal/aami4b_h.dat"

Muestras de FECG

filename = "fetal/1001.dat"
filename = "fetal/ARR_01.dat"
filename = "fetal/NR_01.dat" # OK
filename = "fetal/ARR_08.dat" # OK
filename = "fetal/ARR_05.dat" # Muchos P
filename = "fetal/ARR_03.dat" # Falta P
filename = "fetal/NR_03.dat" # Maso
filename = "fetal/NR_04.dat"
'''
filename = "arritmia/100.dat"

tiempo_limite = 30

ecg = Signal(filename, tiempo_limite)

visualizador = Visualizador(ecg)
visualizador.imprimir_informacion()