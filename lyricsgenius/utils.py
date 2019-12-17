def sanitize_filename(f):
    keepchars = (" ", ".", "_")
    return "".join(c for c in f if c.isalnum() or c in keepchars).rstrip()
