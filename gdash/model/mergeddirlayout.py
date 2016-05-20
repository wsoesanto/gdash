class MergedDirLayout:
    def __init__(self, dirlayout_obj):
        # Take a single dirlayout
        self.layouts = dict()
        for brick_name, dir_layout in dirlayout_obj.iteritems():
            self.layouts[brick_name] = dir_layout.layout

        # Get a single dirlayout object and get the list of subfolders
        subfolders_list = list()
        for brick_name, dir_layout in dirlayout_obj.iteritems():
            for folder_name in dir_layout.subfolders:
                subfolders_list.append(folder_name)
            break

        self.subfolders = dict()
        for subfolder_name in subfolders_list:
            subfolder_dirlayout_obj = dict()
            for brick_name, dir_layout in dirlayout_obj.iteritems():
                subfolder_dirlayout_obj[brick_name] = dir_layout.subfolders[subfolder_name]
            self.subfolders[subfolder_name] = MergedDirLayout(subfolder_dirlayout_obj)

    @staticmethod
    def to_json(mergeddirlayout):
        return mergeddirlayout.__dict__
