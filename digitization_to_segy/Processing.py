import numpy as np
from matplotlib.colors import ListedColormap

class Processing:
    @staticmethod
    def get_palette(name):
        """Тут три палетки для RWB, они все дают +- одинаковый результат для первого случая,
        плюс палетка из petrel для второго случая"""
        if name == 'seismic':
            seismic = np.array([[0, 0, i*0.7 + 0.3, 1] for i in np.linspace(0, 1, 256)]
                                 + [[i, i, 1, 1] for i in np.linspace(0, 1, 256)]
                                 + [[1, 1 - i, 1 - i, 1] for i in np.linspace(0, 1, 256)]
                                 + [[1 - i*0.5, 0, 0, 1] for i in np.linspace(0, 1, 256)])
            return seismic, ListedColormap(seismic)
        elif name == 'rwb_like_petrel':
            rwb_like_petrel = np.array([[i, i, i*0.4 + 0.6, 1] for i in np.linspace(0, 1, 512)]
                                        + [[1 - 0.4*i, 1 - i, 1 - i, 1] for i in np.linspace(0, 1, 512)])
            return rwb_like_petrel, ListedColormap(rwb_like_petrel)
        elif name == 'rwb_petrel':
            with open('../palettes/RWB.alut', 'r') as file:
                lines = file.readlines()
                rwb_petrel = np.array([[int(i) for i in line.strip().split(',')] for line in lines])[::-1]
            return rwb_petrel/255, ListedColormap(rwb_petrel/255)
        elif name == 'basic_petrel':
            with open('../palettes/pallete.alut', 'r') as file:  # палетка петрель
                lines = file.readlines()
                petrel = np.array([[int(i) for i in line.strip().split(',')] for line in lines])[::-1]
            return petrel/255, ListedColormap(petrel/255)
        else:
            try:
                with open(name, 'r') as file:
                    lines = file.readlines()
                    user_palette = np.array([[int(i) for i in line.strip().split(',')] for line in lines])[::-1]
                return user_palette/255, ListedColormap(user_palette/255)
            except:
                raise ValueError("Choose from: 'seismic', 'rwb_like_petrel', 'rwb_petrel', 'basic_petrel' or write correct path")

    @staticmethod
    def __normalized_index(pixel, colors):
        """
        Нормализуем значение амплитуды на промежутке [-1:1]
        :param pixel: np.array([RGBA])
        :param colors: palette
        :return: amplitude value from -1 to 1
        """
        distance = np.linalg.norm(colors[:, :3] - pixel[:3], axis=1) #
        index = np.max(np.where(distance == min(distance)))
        normalized = (index / (len(colors) - 1)) * 2 - 1
        return normalized

    @staticmethod
    def rgb_to_amplitude(img, palette_name):
        image = img
        edited = np.zeros((image.shape[0], image.shape[1]))
        palette, cmap = Processing.get_palette(palette_name)

        for i, row in enumerate(image):
            for j, pixel in enumerate(row):
                edited[i, j] = Processing.__normalized_index(pixel, palette)

        return edited, cmap

    @staticmethod
    def bw_to_amplitude(img):
        edited = np.zeros((img.shape[0], img.shape[1]))

        for i, row in enumerate(img):
            for j, pixel in enumerate(row):
                edited[i, j] = sum(pixel[:3])/3
        return edited