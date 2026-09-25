def blocking_keys(name_norm: str, addr_norm: str, pincode: str | None) -> set:
    keys = set()
    name_tokens = sorted(set(name_norm.split()))
    if name_tokens:
        keys.add(f"name:{name_tokens[0][:6]}")
        for token in name_tokens[1:3]:
            if len(token) >= 4:
                keys.add(f"name:{token[:6]}")
        if len(name_tokens) >= 2:
            keys.add(f"namepair:{name_tokens[0][:4]}:{name_tokens[1][:4]}")
    if pincode:
        keys.add(f"pin:{pincode}")
    addr_tokens = addr_norm.split()
    for t in addr_tokens:
        if len(t) > 3 and not t.isdigit():
            keys.add(f"addr:{t[:8]}")
    return keys