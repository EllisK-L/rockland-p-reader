
import os
import struct
from io import BufferedReader
import json
import pandas as pd
import numpy as np
from PReader.pconfig_parser import PConfigParser
from datetime import datetime, timezone, timedelta

class PDecoder:
    def __init__(self):
        self.f_pointer: BufferedReader = None
        self.header: list[int] = []
        self.all_records: list[list] = []
        self.config_parser = PConfigParser()
        self.debug_level = 0
        self.df: pd.DataFrame = None

    def _get_channel_names(self):
        used_channel_names = []
        for row in range(len(self.config_parser.matrix)):
            for col in range(len(self.config_parser.matrix[row])):
                channel_name = self.config_parser.channels[self.config_parser.matrix[row][col]]["name"]
                if channel_name not in used_channel_names:
                    used_channel_names.append(channel_name)
        used_channel_names.remove("Gnd")
        return used_channel_names

    def raw_to_pandas(self, filename):
        self._decode(filename)
        self.df = pd.DataFrame(data=self.records_dict).set_index("timestamp")
        print(self.df)
        # for key, item in self.records_dict.items():
        #     print(len(item))
        # self.display_matrix(9)
        self.df.to_parquet("./output.parquet")



    def decode_header(self):
        header = []
        # self.header.clear()
        for i in range(64):
            chunk = self.f_pointer.read(2)
            if not chunk:
                return False
            word = struct.unpack(">H", chunk)[0]
            header.append(word)
            if self.debug_level > 0:
                if not self.header:
                    print(f"{i+1}: {word}")
                else:
                    print(f"{i+1}: {word} - {self.header[i]}")
        self.header = header
        print(f"Working on record {self.get_header_val(2)}")
        return True

    def get_header_val(self, location):
        return self.header[location-1]

    def read_config(self):
        config_str = ""
        for i in range(self.get_header_val(12)):
            config_str += self.f_pointer.read(1).decode()
        self.config_parser.read_string(config_str)
        print("done")
        # print(''.join(config_arr))
    
    def get_record_time(self):
        year = self.get_header_val(4)
        month = self.get_header_val(5)
        day = self.get_header_val(6)
        hour = self.get_header_val(7)
        minute = self.get_header_val(8)
        second = self.get_header_val(9)
        milisec = self.get_header_val(10)
        return datetime(year, month, day, hour, minute, second, microsecond=milisec*1000, tzinfo=timezone.utc)

    def decode_record(self):
        data_record_byte_size = self.get_header_val(19)
        records = []
        byte_count = 0
        record_start_time = self.get_record_time()
        sample_rate = 1/float(f"{self.get_header_val(21)}.{self.get_header_val(22)}") * (self.get_header_val(29) + self.get_header_val(30))
        matrix_itr = 0 
        while byte_count < data_record_byte_size-self.get_header_val(18):
            matrix_itr += 1
            matrix = []
            for i_row in range(self.get_header_val(31)):
                channels_in_curr_row = []
                time_offset = timedelta(seconds=sample_rate*matrix_itr*i_row)
                self.records_dict["timestamp"].append(record_start_time + time_offset)
                row = []
                # create new timestamp entry in df
                for j_col in range(self.get_header_val(29) + self.get_header_val(30)):
                    channel_name = self.config_parser.get_channel_name_by_matrix(i_row, j_col)
                    channels_in_curr_row.append(channel_name)
                    chunk = self.f_pointer.read(2)
                    byte_count+= 2
                    word = struct.unpack(">h", chunk)[0]
                    if channel_name != "Gnd":
                        self.records_dict[channel_name].append(word)
                    
                    row.append(word)
                for channel in self._get_channel_names():
                    if channel not in channels_in_curr_row:
                        self.records_dict[channel].append(np.nan)
                matrix.append(row)
            records.append(matrix)
        with open("temp.json", "w") as f:
            json.dump(records, f)
            print(f"Amount of records: {len(records)}")
        self.all_records.append(records)


    def display_matrix(self, record=0):
        space_between = 10
        if record > len(self.all_records):
            raise IndexError("Index more than the amount of records")
        for matrix in self.all_records[record]:
            for row in matrix:
                row_print = ""
                for col in row:
                    # col_calc = f"{(-27.12496 + (0.01148876 * col)):.2f}"
                    col_calc = str(col)
                    row_print += col_calc
                    for space in range(space_between - len(str(col_calc))):
                        row_print += " "
                print(row_print)

            print("\n")



        # data_record_byte_size = self.get_header_val(19)
        # for i in range(data_record_byte_size-self.get_header_val(18)):
        #     chunk = self.f_pointer.read(2)
        #     word = struct.unpack(">H", chunk)[0]
        #     print(f"{i+1}: {word}")
            


    def _decode(self, filename: str):
        if not os.path.exists(filename):
            print("No file found") 
            return
        
        self.f_pointer = open(filename, "rb")
        print("Reading header")
        self.decode_header()
        print("Reading config")
        self.read_config()
        self.df = pd.DataFrame(columns=self._get_channel_names())
        self.records_dict = {channel_name: [] for  channel_name in self._get_channel_names()}
        self.records_dict["timestamp"] = []
        while self.decode_header():
            self.decode_record()
        self.f_pointer.close()
        # print(len(self.all_records))
        # with open("all_records.json", "w") as f:
        #     json.dump(self.all_records, f)




