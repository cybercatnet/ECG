from tools.FileHandler import FileHandler
from tools.Visualizador import Visualizador

# filename = "arritmia/100.dat"
# filename = "ruido/aami3d.dat"
# filename = "picos_abajo/aami3a.dat"
# filename = "normal/aami4b_d.dat"
# filename = "normal/aami4b_h.dat"
# filename = "fetal/1001.dat"
# filename1 = "fetal/ARR_01.dat"
# filename1 = "fetal/NR_01.dat" # OK
# filename = "fetal/ARR_08.dat" # OK
# filename = "fetal/ARR_05.dat" # Muchos P
# filename = "fetal/ARR_03.dat" # Falta P
# filename = "fetal/NR_03.dat" # Maso
filename = "fetal/NR_04.dat"

lector = FileHandler()
tiempo_limite = 30
ecg, fs, data_original = lector.read_signal_file(filename, tiempo_limite)

visualizador = Visualizador()
visualizador.imprimir_informacion(ecg, fs, data_original)