import numpy as np
import cv2 as cv


class Preparer:
    @staticmethod
    def summed_delta_along(img_array, a):  # img_array - np массив исходного изображения, a (0 or 1) = axis - ось, вдодль которой исследуется цветовой градиент
        shifted_arr = np.roll(img_array, 1, axis=a)  # сдвинутый по оси 0 исходный массив
        delta_arr = abs(
            img_array.astype(int) - shifted_arr.astype(int))  # массив из разностей соседних вдоль оси 0 элементов
        summed = np.sum(delta_arr, axis=(a, 2))  # массив из сумм отклонений по оси сдвига, по 3 цветам
        return summed

    @staticmethod
    def summed_delta_across(img_array, a):  # img_array - np массив исходного изображения, a (0 or 1) = axis - ось, вдодль которой исследуется цветовой градиент
        shifted_arr = np.roll(img_array, 1, axis=a)  # сдвинутый по оси 0 исходный массив
        delta_arr = abs(
            img_array.astype(int) - shifted_arr.astype(int))  # массив из разностей соседних вдоль оси 0 элементов
        summed = np.sum(delta_arr,
                        axis=((1 - a), 2))  # массив из сумм отклонений по оси, перпендикулярной a, по 3 цветам
        return summed

    @staticmethod
    def find_borders(img_array, a, method):
        if method == 0:
            summed = Preparer.summed_delta_across(img_array, a)
        elif method == 1:
            summed = Preparer.summed_delta_along(img_array, (1 - a))
        sr = int(np.mean(summed))  # среднее значение интенсивности отклонения линий, параллельных оси суммирования
        xleft = 0
        xright = 0  # координаты границ участка повышенной интенсивности линий
        first = 0
        for i in range(len(summed)):
            if summed[i] > sr:
                if first == 0:
                    xleft = i
                    first = 1
                else:
                    xright = i
        indsr = int((xleft + xright) / 2)  # считаем, середина между границами этого участка попадает внутрь изображения с данными
        borders = [0, 0]  # будущие границы по оси 1
        right = 0
        left = 0  # логические переменные для нахождения точных границ изображиния. Нахождение границ происходит по ближайшему минимуму на
        # графике сумм разниц интенсивностей соседних линий
        for i in range(max(len(summed) - sr, sr)):
            if indsr + i + 1 < len(summed):
                if summed[indsr + i + 1] < 0.2 * sr and right == 0:
                    borders[1] = indsr + i
                    right = 1
            if indsr - i - 1 > 0:
                if summed[indsr - i - 1] < 0.2 * sr and left == 0:
                    borders[0] = indsr - i
                    left = 1
            if right == 1 and left == 1:
                break
        if borders[1] == 0:
            borders[1] = len(summed) - 1
        return borders

    @staticmethod
    def getSeismicRGB(img_array, method_ax0, method_ax1):
        # method_ax0 - нахождение границ по вертикальной оси, method_ax1 - по горизонтальной
        # если у данных есть резкие границы по оси Z, лучше использовать method_axZ=0. Если граница картинки с данными не четкая, то method_axZ=1
        img = img_array * 255
        borders0 = Preparer.find_borders(img, 0, method_ax0)
        borders1 = Preparer.find_borders(img, 1, method_ax1)
        return img[borders0[0]:borders0[1], borders1[0]:borders1[1]]/255

    @staticmethod
    def getSeismicRGB_cv(img_array, numb_of_iterations, binary_method):
        # если фон сейсм. данных не белый, можно примменять более одной итеррации (2 или 3), binary_method=1 (cv.THRESH_OTSU + cv.THRESH_BINARY_INV)
        # если фон данных белый, следует применять только одну итеррацию и использование binary_method=0 (240, 255, cv.THRESH_BINARY_INV)
        img = img_array * 255
        image = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        kernel = np.ones((3, 3), np.uint8)  # ядро матрицы для функции dilate
        image = cv.dilate(image, kernel, iterations=numb_of_iterations)  # если фон статьи белый, то уйдут оси и текст

        # бинаризация с инверсией (работает, если фон скриншота светлее, чем фон данных)
        if binary_method == 0:
            ret, image = cv.threshold(image, 245, 255, cv.THRESH_OTSU + cv.THRESH_BINARY_INV)
        else:
            ret, image = cv.threshold(image, 245, 255, cv.THRESH_BINARY_INV)
        contours, hierarchy = cv.findContours(image, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)

        # нахождение контура наибольшего размера
        num = 0
        maxlen = 0
        len_0 = len(contours[0])
        for i in range(0, len(contours), 1):
            if len(contours[i]) >= len_0 / 2:
                if len(contours[i]) > maxlen:
                    num = i
                    maxlen = len(contours[i])
        contour = np.array(contours[num])
        xmin = np.min(contour[:, :, 0])
        ymin = np.min(contour[:, :, 1])
        xmax = np.max(contour[:, :, 0])
        ymax = np.max(contour[:, :, 1])
        crop_img = img_array[ymin:ymax, xmin:xmax]
        return crop_img
