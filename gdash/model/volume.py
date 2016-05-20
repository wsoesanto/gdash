from brick import Brick
from node import Node


class Volume:
    @classmethod
    def with_volume_status(cls, xml_model):
        self = cls()
        self.name = xml_model.find("volName").text
        self.number_of_nodes = xml_model.find("nodeCount").text
        self.nodes = []
        for xml_node in xml_model.findall("node"):
            self.nodes.append(Node(xml_node))
        return self

    @classmethod
    def with_volume_info(cls, xml_model):
        self = cls()
        self.name = xml_model.find("name").text
        self.id = xml_model.find("id").text
        self.status = (int(xml_model.find("status").text) == 1)
        self.brick_count = int(xml_model.find("brickCount").text)
        self.dist_count = int(xml_model.find("distCount").text)
        self.stripe_count = int(xml_model.find("stripeCount").text)
        self.replica_count = int(xml_model.find("replicaCount").text)
        self.arbiter_count = int(xml_model.find("arbiterCount").text)
        self.disperse_count = int(xml_model.find("disperseCount").text)
        self.redundancy_count = int(xml_model.find("redundancyCount").text)
        self.type = xml_model.find("typeStr").text
        self.bricks = list()
        for xml_brick in xml_model.find("bricks").findall("brick"):
            brick = Brick(xml_brick)
            self.bricks.append(brick)
        self.options = dict()
        for xml_option in xml_model.find("options").findall("option"):
            name = xml_option.find("name").text
            value = xml_option.find("value").text
            self.options[name] = value
        return self

    @staticmethod
    def to_json(volume):
        return volume.__dict__

    @classmethod
    def merge(cls, volume_status, volume_info):
        self = cls()
        self.name = volume_status.name
        self.number_of_nodes = volume_status.number_of_nodes
        self.nodes = volume_status.nodes
        self.id = volume_info.id
        self.status = volume_info.status
        self.brick_count = volume_info.brick_count
        self.dist_count = volume_info.dist_count
        self.stripe_count = volume_info.stripe_count
        self.replica_count = volume_info.replica_count
        self.arbiter_count = volume_info.arbiter_count
        self.disperse_count = volume_info.disperse_count
        self.redundancy_count = volume_info.redundancy_count
        self.type = volume_info.type
        self.bricks = volume_info.bricks
        self.options = volume_info.options
        return self
