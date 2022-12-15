import hashlib


def hash_code(s, salt='Qn'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()
