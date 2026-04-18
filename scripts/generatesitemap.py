from urllib.parse import urlparse

def get_url_priority(url, base_priority=1.0, decay=0.2, min_priority=0.1):
    """
    Calculates priority based on URL depth.
    - depth 0 (home): 1.0
    - depth 1: 0.8
    - depth 2: 0.6, etc.
    """
    # Parse the URL and strip leading/trailing slashes from the path
    path = urlparse(url).path.strip('/')
    
    # If the path is empty, it's the homepage
    if not path:
        return base_priority
    
    # Count segments (subdirectories)
    depth = len(path.split('/'))
    
    # Calculate decaying priority
    # priority = max(min_priority, base_priority - (depth * decay))
    priority = min(base_priority, max(min_priority, base_priority * 1.8 / ( 1 + depth)))
    return round(priority, 2)

# # --- Test Cases ---
# urls = [
#     "https://example.com/",
#     "https://example.com/blog",
#     "https://example.com/blog/a",
#     "https://example.com/blog/a/b",
#     "https://example.com/blog/a/b/c",
#     "https://example.com/blog/a/b/c/d",
#     "https://example.com/blog/a/b/c/d/e",
#     "https://example.com/blog/a/b/c/d/e/f",
#     "https://example.com/blog/a/b/c/d/e/f/g",
#     "https://example.com/blog/a/b/c/d/e/f/g/h",
# ]

# for link in urls:
#     print(f"Priority for {link}: {get_url_priority(link)}")
