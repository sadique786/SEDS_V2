import cv2


class CameraManager:

    def load_image( self,image_path):

        image = cv2.imread(image_path)

        return image
