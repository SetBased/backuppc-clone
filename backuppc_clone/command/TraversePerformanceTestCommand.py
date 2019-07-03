"""
BackupPC Clone
"""
import os
import time

from cleo import Command, Input, Output

from backuppc_clone.style.BackupPcCloneStyle import BackupPcCloneStyle


class TraversePerformanceTestCommand(Command):
    """
    Traversing recursively a directory performance test

    traverse-performance-test
        {--stat : Get status of each file}
        {dir    : The start directory}
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object constructor.
        """
        Command.__init__(self)

        self.__stat = False
        """
        If True stat must be called for each file.

        :type: bool
        """

        self._io = None
        """
        The output style.

        :type: backuppc_clone.style.BackupPcCloneStyle.BackupPcCloneStyleG57G
        """

        self.__dir_count = 0
        """
        The number of directories counted.

        :type: int
        """

        self.__file_count = 0
        """
        The number of file counted.

        :type: int
        """

        self.__start_time = 0
        """
        The timestamp of the start of the performance test.

        :type: float
        """

    # ------------------------------------------------------------------------------------------------------------------
    def __traverse(self, path: str) -> None:
        """
        Traverse recursively a directory.

        :param str path: The path to the directory.
        """
        dirs = []
        for entry in os.scandir(path):
            if self.__stat and not entry.is_symlink():
                entry.stat()

            if entry.is_file():
                self.__file_count += 1

            elif entry.is_dir():
                dirs.append(entry.name)
                self.__dir_count += 1

        for name in dirs:
            self.__traverse(os.path.join(path, name))

    # ------------------------------------------------------------------------------------------------------------------
    def __report(self, end_time: float) -> None:
        """
        Prints the performance report.

        :param float end_time: The timestamp of the end of the performance test.
        """
        self._io.writeln('')
        self._io.writeln('number of directories: {}'.format(self.__dir_count))
        self._io.writeln('number of files      : {}'.format(self.__file_count))
        self._io.writeln('get status           : {}'.format('yes' if self.__stat else 'no'))
        self._io.writeln('duration             : {0:.1f}s'.format(end_time - self.__start_time))

    # ------------------------------------------------------------------------------------------------------------------
    def execute(self, input_object: Input, output_object: Output) -> None:
        """
        Executes the command.

        :param Input input_object: The input.
        :param Output output_object: The output.
        """
        self.input = input_object
        self.output = output_object

        self.handle()

    # ------------------------------------------------------------------------------------------------------------------
    def handle(self) -> None:
        """
        Executes the command.
        """
        self._io = BackupPcCloneStyle(self.input, self.output)

        self.__stat = self.option('stat')
        self.__dir_count = 0
        self.__file_count = 0
        self.__start_time = time.time()

        dir_name = self.argument('dir')

        self._io.writeln('Traversing <fso>{}</fso>'.format(dir_name))
        self.__traverse(dir_name)
        self.__report(time.time())

# ----------------------------------------------------------------------------------------------------------------------
