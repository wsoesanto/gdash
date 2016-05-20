class GlusterCommand:
    def __init__(self, gluster_path, remote_host):
        self.__cmd_list = [gluster_path, '--xml']

    def get_volume_command(self):
        # create a new list because there is only a single GlusterCommand
        return _VolumeCommand(self.__cmd_list[:])


class _VolumeCommand:
    def __init__(self, cmd_list):
        cmd_list.append(self.__VOLUME_COMMAND)
        self.__cmd_list = cmd_list

    __VOLUME_COMMAND = 'volume'
    __ALL_OPTION = 'all'
    __LIST_COMMAND = 'list'
    __STATUS_COMMAND = 'status'
    __INFO_COMMAND = 'info'

    # TODO: Create volume function

    def get_volume(self, vol_name):
        return _SpecificVolumeCommand(self.__cmd_list, vol_name)

    # TODO: Read about tier

    def get_list(self):
        self.__cmd_list.append(self.__LIST_COMMAND)
        return self.__cmd_list

    def get_status(self, option=None):
        self.__cmd_list.append(self.__STATUS_COMMAND)
        self.__cmd_list.append(self.__ALL_OPTION)
        if option:
            self.__cmd_list.append(option)
        return self.__cmd_list

    def get_info(self):
        self.__cmd_list.append(self.__INFO_COMMAND)
        self.__cmd_list.append(self.__ALL_OPTION)
        return self.__cmd_list


class _SpecificVolumeCommand:
    def __init__(self, cmd_list, vol_name):
        self.__cmd_list = cmd_list
        self.__vol_name = vol_name

    __DELETE_COMMAND = 'delete'
    __START_COMMAND = 'start'
    __STOP_COMMAND = 'stop'
    __FORCE_COMMAND = 'force'
    __INFO_COMMAND = 'info'
    __ADD_BRICK_COMMAND, __REMOVE_BRICK_COMMAND = 'add-brick', 'remove-brick'
    __STATUS_COMMAND = 'status'

    def delete(self):
        self.__cmd_list.extend([self.__DELETE_COMMAND, self.__vol_name])
        return self.__cmd_list

    # TODO: Start command doesn't seem to work by using remote host

    def start(self, is_force=False):
        self.__cmd_list.extend([self.__START_COMMAND, self.__vol_name])
        if is_force:
            self.__cmd_list.append(self.__FORCE_COMMAND)
        return self.__cmd_list

    # TODO: Stop command doesn't seem to work by using remote host

    # TODO: Stop command subprocess seems to halt when requesting for input. Inserting input "y" into communicate()
    # TODO: doesn't work. Find out another way

    def stop(self, is_force=False):
        self.__cmd_list.extend([self.__STOP_COMMAND, self.__vol_name])
        if is_force:
            self.__cmd_list.append(self.__FORCE_COMMAND)
        return self.__cmd_list, "y"

    # TODO: add stripe/replica option

    # def add_brick(self, list_bricks):
    #     self.__cmd_list.extend(list_bricks)

    # def remove_brick(self):

    def get_info(self):
        self.__cmd_list.extend([self.__INFO_COMMAND, self.__vol_name])
        return self.__cmd_list

    def get_status(self, option=None):
        self.__cmd_list.append(self.__STATUS_COMMAND)
        self.__cmd_list.append(self.__vol_name)
        if option:
            self.__cmd_list.append(option)
        return self.__cmd_list
