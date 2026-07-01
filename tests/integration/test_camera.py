from detection.camera_manager import (CameraManager)

camera = CameraManager()

image = camera.load_image("test_images/elephant.jpg")

print(image.shape)

print(type(image))
