import errno
import os

from django.conf import settings


def ensure_dir(filename):
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise


def save_to_filefield(s, model, field_name, file_name):
    fld = model.__class__._meta.get_field(field_name)
    name = fld.upload_to(model, file_name) if callable(fld.upload_to) else os.path.join(fld.upload_to, file_name)
    path = os.path.join(settings.MEDIA_ROOT, name)
    ensure_dir(path)

    with open(path, "wb") as f:
        f.write(s)

    getattr(model, field_name).name = name
    model.save()
