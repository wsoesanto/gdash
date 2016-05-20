class Brick:
    def __init__(self, xml_model):
        self.name = xml_model.find("name").text
        self.host_uuid = xml_model.find("hostUuid").text
        self.is_arbiter = (int(xml_model.find("isArbiter").text) == 1)

    @staticmethod
    def to_json(brick):
        return brick.__dict__
