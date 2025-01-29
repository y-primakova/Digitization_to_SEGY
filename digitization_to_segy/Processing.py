import numpy as np


class Processing:
    @staticmethod
    def rgb_to_amplitude1(data):
        k = 0
        new_array = np.zeros((data.shape[0], data.shape[1]))
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                if data[i][j][0] == 0 and data[i][j][1] == 0:
                    new_array[i, j] = 5 / 7 * data[i][j][2] - 3 / 14 - 1
                elif data[i][j][0] == data[i][j][1] and data[i][j][0] < data[i][j][2]:
                    new_array[i, j] = 0.5 * data[i][j][0] - 0.5
                elif data[i][j][0] == data[i][j][1] and data[i][j][0] == data[i][j][2] and data[i][j][0] >= 240 / 255:
                    new_array[i, j] = 0
                elif data[i][j][2] == 0 and data[i][j][1] == 0:
                    new_array[i, j] = 1.5 - data[i][j][0]
                elif data[i][j][1] == data[i][j][2] and data[i][j][1] < data[i][j][0]:
                    new_array[i, j] = 0.5 - 0.5 * data[i][j][2]
                else:
                    new_array[i, j] = np.nan
                    print(k, data[i][j] * 255, data[i][j])
                    k += 1
        return new_array

    @staticmethod
    def __normalized_index(pixel, colors):
        distance = np.linalg.norm(colors[:, :3] - pixel[:3], axis=1)
        index = np.argmin(distance) / len(colors)
        normalized = index * 2 - 1
        return normalized

    @staticmethod
    def rgb_to_amplitude(img):
        image = img * 255
        edited = np.zeros((image.shape[0], image.shape[1]))

        mycolors = np.array([[0, 0, i * 0.4 + 0.6, 1] for i in np.linspace(0, 1, 256)]
                            + [[i, i, 1, 1] for i in np.linspace(0, 1, 256)]
                            + [[1, 1 - i, 1 - i, 1] for i in np.linspace(0, 1, 256)]
                            + [[1 - i * 0.4, 0, 0, 1] for i in np.linspace(0, 1, 256)]) * 255
        # mycolors = np.array([[i, i, i * 0.4 + 0.6, 1] for i in np.linspace(0, 1, 256)] + [[1 - 0.4 * i, 1 - i, 1 - i, 1] for i in
        #                                                                        np.linspace(0, 1, 256)]) * 255

        for i, row in enumerate(image):
            for j, pixel in enumerate(row):
                edited[i, j] = Processing.__normalized_index(pixel, mycolors)
        return edited
