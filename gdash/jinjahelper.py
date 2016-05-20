from flask import render_template


class JinjaHelper:
    @staticmethod
    def file_tree_list(par_dir_path, name, mergeddirlayout):
        dir_path = par_dir_path + name + "/"
        return render_template("dir-tree.html", dir_path=dir_path, name=name, dir=mergeddirlayout)
