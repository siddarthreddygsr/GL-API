from boundary import save_output, detect_objects_in_image
from image2url import image2url

image_path = '11.jpg'
def accessories_s3url(image_path):
    detected_objects = detect_objects_in_image(image_path)

    list_of_paths = save_output(image_path,detected_objects)
    list_of_urls = []
    for i in list_of_paths:
        list_of_urls.append(image2url(i))
    return list_of_urls

print(accessories_s3url('11.jpg'))