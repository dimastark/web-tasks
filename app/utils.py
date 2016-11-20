from collections import namedtuple


Image = namedtuple('Image', ['src', 'id'])


def create_image(name, image_id):
    return Image('app/gallery/' + name, 'image' + str(image_id))
