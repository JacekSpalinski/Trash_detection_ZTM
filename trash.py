# -*- coding: utf-8 -*-
"""Trash.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1W4wgi1cCL2vLSUAimKeDpNj5N-Vi5u6_
"""

#pip install google-cloud-vision
#pip install Pillow
#pip install piexif
#pip install selenium
#pip install folium
#pip install matplotlib

from google.cloud import vision

import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS']='C:/Users/Patryk/Desktop/deft-station-375717-6847447a0df3.json'

def detect_labels_uri(uri):
    """Detects labels in the file located in Google Cloud Storage or on the
    Web."""
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = uri

    response = client.label_detection(image=image)
    labels = response.label_annotations
    #print(labels)
    print('Labels:')

    for label in labels:
        print(label.description + " "+ str(label.score))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
                
def detect_labels(path):
    """Detects labels in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')

    for label in labels:
        print(label.description)

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

detect_labels_uri('https://www.ladysmithchronicle.com/wp-content/uploads/2019/07/17648894_web1_190711-LCH-Garbage-Forests1-640x427.jpg')
#detect_labels(path)

def localize_objects_uri(uri):
    """Localize objects in the image on Google Cloud Storage

    Args:
    uri: The path to the file in Google Cloud Storage (gs://...)
    """
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    image = vision.Image()
    image.source.image_uri = uri

    objects = client.object_localization(
        image=image).localized_object_annotations

    print('Number of objects found: {}'.format(len(objects)))
    for object_ in objects:
        print('\n{} (confidence: {})'.format(object_.name, object_.score))
        print('Normalized bounding polygon vertices: ')
        for vertex in object_.bounding_poly.normalized_vertices:
            print(' - ({}, {})'.format(vertex.x, vertex.y))
            
def localize_objects(path):
    """Localize objects in the local image.

    Args:
    path: The path to the local file.
    """
    from google.cloud import vision
    client = vision.ImageAnnotatorClient()

    with open(path, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    objects = client.object_localization(
        image=image).localized_object_annotations

    print('Number of objects found: {}'.format(len(objects)))
    for object_ in objects:
        print('\n{} (confidence: {})'.format(object_.name, object_.score))
        print('Normalized bounding polygon vertices: ')
        for vertex in object_.bounding_poly.normalized_vertices:
            print(' - ({}, {})'.format(vertex.x, vertex.y))

localize_objects_uri('https://www.ladysmithchronicle.com/wp-content/uploads/2019/07/17648894_web1_190711-LCH-Garbage-Forests1-640x427.jpg')
#localize_objects(path)

from PIL import Image
from PIL.ExifTags import TAGS

imagename = "C:/Users/Patryk/Desktop/17648894_web1_190711-LCH-Garbage-Forests1.jpg"
#https://drive.google.com/file/d/1i0hYkcI7nN4fPDAuEhJolDFU7mfm7kBB/view?usp=share_link zdj z lokalizacją gps w metadanych

# read the image data using PIL
image = Image.open(imagename)

import piexif

codec = 'ISO-8859-1'

def exif_to_tag(exif_dict):
    exif_tag_dict = {}
    thumbnail = exif_dict.pop('thumbnail')
    exif_tag_dict['thumbnail'] = thumbnail.decode(codec)

    for ifd in exif_dict:
        exif_tag_dict[ifd] = {}
        for tag in exif_dict[ifd]:
            try:
                element = exif_dict[ifd][tag].decode(codec)

            except AttributeError:
                element = exif_dict[ifd][tag]

            exif_tag_dict[ifd][piexif.TAGS[ifd][tag]["name"]] = element

    return exif_tag_dict

exif_dict = piexif.load(image.info.get('exif'))
exif_dict = exif_to_tag(exif_dict)
print(exif_dict['GPS'])

#Wysokosc i szerokosc geograficzna pobrana z metadanych zdj
lat = float(str(exif_dict['GPS'].get('GPSLatitude')[0][0])+"."+str(exif_dict['GPS'].get('GPSLatitude')[1][0]))
long = float(str(exif_dict['GPS'].get('GPSLongitude')[0][0])+"."+str(exif_dict['GPS'].get('GPSLongitude')[1][0]))
print(lat)
print(long)

# import the library
import folium

# Make an empty map
m = folium.Map(location=[20,0], tiles="OpenStreetMap", zoom_start=2)

# Show the map
m

folium.Marker(location=[lat, long],).add_to(m)

import io
from PIL import Image

img_data = m._to_png(5)
img = Image.open(io.BytesIO(img_data))
img.save('image.png')

from matplotlib import pyplot as plt
from matplotlib import image as mpimg
 
plt.title("Mapa")
plt.xlabel("X pixel scaling")
plt.ylabel("Y pixels scaling")

plt.imshow(img)
plt.show()