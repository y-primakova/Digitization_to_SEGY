import segyio


class Saver:
    @staticmethod
    def save_segy(path, data):
        """
        Parameters:
        path:str
            Путь до файла.
        data: nd.array
            массив размером (N, M), где N - количество трасс, M - длина трассы.
        """

        segyio.tools.from_array2D(path, data)
