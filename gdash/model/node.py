class Node:
    def __init__(self, xml_model):
        self.hostname = xml_model.find("hostname").text
        self.path = xml_model.find("path").text
        self.peerid = xml_model.find("peerid").text
        self.status = (int(xml_model.find("status").text) == 1)
        self.port = xml_model.find("port").text
        # TODO: find out why there is "ports" tag in xml
        self.pid = xml_model.find("pid").text

        if xml_model.find("sizeTotal") is not None:
            self.sizeTotal = xml_model.find("sizeTotal").text
        if xml_model.find("device") is not None:
            self.device = xml_model.find("device").text
        if xml_model.find("blockSize") is not None:
            self.blockSize = xml_model.find("blockSize").text
        if xml_model.find("mntOptions") is not None:
            self.mntOptions = xml_model.find("mntOptions").text
        if xml_model.find("fsName") is not None:
            self.fsName = xml_model.find("fsName").text

    @staticmethod
    def to_json(node):
        return node.__json
