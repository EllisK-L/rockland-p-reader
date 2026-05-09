from PReader.pdecoder import PDecoder


if __name__ == '__main__':
    decoder = PDecoder()
    decoder.debug_level = 1
    decoder.get_level_0("examples/raw/dat_1336.p")
    decoder.display_matrix(9)
    print(decoder.l0_df["U_EM"])

    decoder.get_level_1()
    print(decoder.l1_df["U_EM"])