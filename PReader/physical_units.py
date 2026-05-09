class BasePhysical:
    def __init__(self, channel_config: dict):
        self.channel_config = channel_config
        try:
            self.set_coefficients()
        except KeyError as e:
            raise KeyError(f"Failed to get coefficients from channel config!\n{e}")

    def get_channel_name(self):
        return self.channel_config["name"]

    def set_coefficients(self):
        print("Setting coefficients Base")
        pass

    def convert(self):
        raise NotImplementedError

class UEMPhysical(BasePhysical):
    def __init__(self, channel_config: dict):
        super().__init__(channel_config)

    def set_coefficients(self):
        print("Setting coefficients UEM")
        self.a = self.channel_config["a"]
        self.b = self.channel_config["b"]

    def convert(self, val):
        return self.a + (self.b * val)