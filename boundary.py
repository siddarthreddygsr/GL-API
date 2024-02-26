import io
import os
from google.cloud import vision
from PIL import Image
import time

def detect_objects_in_image(image_path):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'secrets.json'
    client = vision.ImageAnnotatorClient()
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)
    objects = client.object_localization(image=image).localized_object_annotations
    object_details = []
    for object_ in objects:
        vertices = [[vertex.x, vertex.y] for vertex in object_.bounding_poly.normalized_vertices]
        object_details.append({
            'name': object_.name,
            'confidence': object_.score,
            'vertices': vertices
        })

    return object_details

def crop_image(image_path, normalized_vertices,output_name):
    with Image.open(image_path) as img:
        # Convert normalized coordinates to absolute pixel coordinates
        width, height = img.size
        absolute_vertices = [
            (
                int(vertex[0] * width), 
                int(vertex[1] * height)
            ) for vertex in normalized_vertices
        ]

        left, upper = absolute_vertices[0]
        right, lower = absolute_vertices[2]

        cropped_img = img.crop((left, upper, right, lower))
        img_name = image_path.split('/')[-1].split('.')[0]
        cropped_img_path = f"results/{img_name}_{output_name}_{int(time.time())}.jpg"
        cropped_img.save(cropped_img_path)

        return cropped_img_path

def save_output(image_path,detected_objects):
    cropped_image_path_list = []
    for obj in detected_objects:
        img_path = crop_image(image_path,obj['vertices'],obj['name'].replace(' ','_'))
        cropped_image_path_list.append(img_path)
    return cropped_image_path_list

"""
# Example usage
image_path = r'11.jpg'
detected_objects = detect_objects_in_image(image_path)

for i in save_output(image_path,detected_objects):
    print(i)
"""