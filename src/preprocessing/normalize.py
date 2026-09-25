import re

LEGAL_SUFFIXES = {"inc","incorporated","corp","corporation","ltd","limited",
                   "llc","pvt","private","co","company","plc"}
ADDR_ABBR = {"rd":"road","st":"street","ave":"avenue","blvd":"boulevard",
             "dr":"drive","ln":"lane","apt":"apartment","fl":"floor",
             "nr":"near","opp":"opposite"}

def normalize_name(name: str) -> str:
    if not isinstance(name, str):
        return ""
    name = name.lower().strip()
    name = name.replace("&", " and ")
    name = re.sub(r"[^\w\s]", " ", name)
    tokens = [t for t in name.split() if t not in LEGAL_SUFFIXES]
    return " ".join(tokens)

def normalize_address(addr: str) -> str:
    if not isinstance(addr, str):
        return ""
    addr = addr.lower().strip()
    addr = re.sub(r"[^\w\s,]", " ", addr)
    tokens = [ADDR_ABBR.get(t, t) for t in addr.split()]
    return " ".join(tokens)

def extract_pincode(addr_norm: str):
    tokens = addr_norm.split()
    for t in tokens[::-1]:
        if t.isdigit() and len(t) >= 4:
            return t
    return None

def add_normalized_columns(df):
    df = df.copy()
    df["name_norm"] = df["business_name"].apply(normalize_name)
    df["addr_norm"] = df["business_address"].apply(normalize_address)
    df["pincode"] = df["addr_norm"].apply(extract_pincode)
    return df