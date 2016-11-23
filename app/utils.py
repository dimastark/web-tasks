from collections import namedtuple


Image = namedtuple('Image', ['src', 'thumb', 'id'])


def create_image(name, image_id):
    return Image(
        'app/gallery/' + name + '.png',
        'app/gallery/' + name + '_tn.jpg',
        'image' + str(image_id)
    )
