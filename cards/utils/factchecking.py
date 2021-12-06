from ..settings import FACTCHECKING_TAGS, FACTCHECKING_LABELS_MAP


def get_factchecking_meter_tag(post: dict) -> str:
    tag = None

    for post_tag in post.get('tags', []):
        if post_tag['slug'] in FACTCHECKING_TAGS:
            return post_tag['slug']

    if not tag:
        raise ValueError(f'Tag was not found in factchecking post\n{post["tags"]}')


def get_factchecking_tag_label(tag: str) -> str:
    if tag not in FACTCHECKING_TAGS:
        raise ValueError('Invalid tag name')

    return FACTCHECKING_LABELS_MAP[tag]
