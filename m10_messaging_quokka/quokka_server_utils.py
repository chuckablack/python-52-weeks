from urllib.parse import urlparse


def fix_target(target):

    # Target could be a URL; if so, use urlparse to extract the network location (hostname)
    if target.startswith("http://") or target.startswith("https://"):
        parsed_target = urlparse(target)
        return parsed_target.netloc

    return target
