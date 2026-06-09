import cv2

image = cv2.imread("test_images/elephant.jpg")

cv2.rectangle(
    image,
    (500, 500),
    (2000, 2000),
    (0, 255, 0),
    5
)

cv2.putText(
    image,
    "Elephant 0.92",
    (500, 450),
    cv2.FONT_HERSHEY_SIMPLEX,
    2,
    (0, 255, 0),
    4
)

cv2.imwrite("captures/visualized_elephant.jpg",image)

print("Image saved successfully")
