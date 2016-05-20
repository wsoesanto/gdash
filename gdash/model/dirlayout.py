class DirLayout:
    def __init__(self):
        self.layout = None
        self.subfolders = dict()

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False

        # Check whether their list of subfolder are same
        subfolder_name_set = set()
        for subfolder_name in self.subfolders:
            subfolder_name_set.add(subfolder_name)
        other_subfolder_name_set = set()
        for subfolder_name in other.subfolders:
            other_subfolder_name_set.add(subfolder_name)
        if subfolder_name_set != other_subfolder_name_set:
            return False

        # Check if the layout of their subfolder are same
        for subfolder_name in self.subfolders:
            if self.subfolders[subfolder_name] != other.subfolders[subfolder_name]:
                return False
        return True

    def __ne__(self, other):
        return not self == other

    @classmethod
    def with_dir_layout_obj(cls, root_dir_layout_obj):
        self = cls()
        self.layout = root_dir_layout_obj['layout']
        self.subfolders = dict()
        for subfolder_name, dir_layout_obj in root_dir_layout_obj['subfolders'].items():
            self.subfolders[subfolder_name] = DirLayout.with_dir_layout_obj(dir_layout_obj)
        return self

    def add_subfolder(self, name):
        self.subfolders[name] = DirLayout()

    def get_subfolder(self, name):
        return self.subfolders[name]

    def set_layout(self, layout):
        self.layout = layout

    @staticmethod
    def to_json(dir_layout):
        return dir_layout.__dict__
