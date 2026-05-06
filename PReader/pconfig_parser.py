class PConfigParser:
    def __init__(self):
        self.channels = {}
        self.matrix = []
        self.channels = {}

    def _try_num_cast(self, val):
        ret = val
        if "." in val:
            try:
                ret = float(val)
            except:
                pass
        else:
            try:
                ret = int(val)
            except:
                pass
        return ret

    def _format_matrix(self, matrix_section: dict):
        ret = []
        for key, row in matrix_section.items():
            processed_row = []
            for row_val in row.split("\t"):
                try:
                    int_val = int(row_val)
                    processed_row.append(int_val)
                except:
                    for val in row_val.split(" "):
                        if val:
                            processed_row.append(int(val))
            ret.append(processed_row)
            print(processed_row)
        return ret

    def get_channel_name_by_matrix(self, row,col):
        return self.channels[self.matrix[row][col]]["name"]

    def read_string(self, config_str: str):
        section = {}
        header_name = ""
        for line in config_str.splitlines():
            print(line)
            if len(line) > 2:
                match line[0]:
                    case ";":
                        pass
                    case "[":
                        # header
                        # Save last section
                        if header_name:
                            if header_name == "channel":
                                self.channels[section["id"]] = section
                            elif header_name == "matrix":
                                self.matrix = self._format_matrix(section)
                            section = {}
                        header_name = line[1:-1]
                    case _:
                        # variable assignment
                        line_split = line.split("=")
                        var = line_split[0].strip()
                        
                        val = line_split[1].strip() 
                        if ";" in val:
                            val = val.split(";")[0].strip()
                        # val = val.split("\t")
                        val = self._try_num_cast(val)
                        section[var] = val

        if header_name == "channel":
            self.channels[section["id"]] = section
    
