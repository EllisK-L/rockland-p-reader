from PReader.pdecoder import PDecoder


if __name__ == '__main__':
    decoder = PDecoder()
    decoder.debug_level = 1
    decoder.raw_to_pandas("data/dat_1336.p")