import os
import uuid

def get_unique_filename(instance, filename):
    model_name = instance.__class__.__name__.lower()
    folder_mapping = {
        'user': 'profile/',
        'product': 'products/',
        'productimage': 'product_images/',
        'default': 'others/',
    }
    try:
        folder = folder_mapping[model_name]
    except:
        folder = folder_mapping['default']

    ext = filename.split('.')[-1]
    unique_filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join(folder, unique_filename)
