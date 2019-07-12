import wfdb
from scipy.io import wavfile

from tools.Signal import Signal


class FileHandler:
    def __init__(self):
        def read_wav_file(wav_file_name):
            fs, data = wavfile.read(wav_file_name, mmap=False)
            return fs, data

        def read_dat_file(dat_file_name):
            dat_file_name = dat_file_name[:dat_file_name.find(".")]
            record = wfdb.rdrecord(dat_file_name)
            return record.fs, [x[0] for x in record.p_signal]

        self.readers = {"wav": read_wav_file,
                        "dat": read_dat_file}

    def read_signal_file(self, filename, pulsos_por_tajada):
        def file_extension(filename):
            return filename[filename.find(".")+1:]

        ext = file_extension(filename)
        if ext not in self.readers:
            raise "Invalid file extension:" + ext
        fs, data = self.readers[ext](filename)
        signal = Signal(fs, data, pulsos_por_tajada)
        return signal