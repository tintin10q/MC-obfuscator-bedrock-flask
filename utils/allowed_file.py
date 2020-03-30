def allowed_file(filename):
    if filename.split(".")[-1] in ("zip"):
        return True
    else:
        return False