from PIL import Image


def make_and_save_thumbnail(thumbnail_path, archive_thumbnails_path, size=(192, 108), item_id="no_id"):
    if not thumbnail_path:
        return ""
    thumbnail = Image.open(thumbnail_path)
    thumbnail = thumbnail.resize(size)
    if thumbnail.mode != "RGB":
        thumbnail = thumbnail.convert("RGB")
    item_thumbnail_path = archive_thumbnails_path + f"{item_id}_thumbnail.jpeg"
    thumbnail.save(item_thumbnail_path)
    return item_thumbnail_path
