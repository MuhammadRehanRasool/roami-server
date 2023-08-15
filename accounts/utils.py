from django.utils.text import slugify


def get_username_unique_slug(id, title, obj):
    slug = slugify(title.replace('ı', 'i'))
    unique_slug = slug
    counter = 1
    while obj.filter(username_slug=unique_slug).exists():
        if obj.filter(username_slug=unique_slug).values('id')[0]['id'] == id:
            break
        unique_slug = '{}-{}'.format(slug, counter)
        counter += 1
    return unique_slug
