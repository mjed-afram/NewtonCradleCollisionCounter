from factories import Preprocessor



class Pipeline:
    def __init__(self):
        self.preprocessor = Preprocessor.hsv_segmentor("HSV Segmentor")






if __name__ == "__main__":
    pipeline = Pipeline()