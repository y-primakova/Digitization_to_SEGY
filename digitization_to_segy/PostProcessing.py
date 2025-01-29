import cv2 as cv


class PostProcessing:
    @staticmethod
    def resize_array(data, trace_count, n_samples):
        data_res = cv.resize(data, dsize=(trace_count, n_samples), interpolation=cv.INTER_CUBIC)
        return data_res