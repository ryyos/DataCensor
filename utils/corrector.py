def vname(name: str, separator: str = '_') -> str:
    invalid_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|', '+', '=', '&', '%', '@', '#', '$', '^', '[', ']', '{', '}', '`', '~', '\n']
    falid = ''.join(char if char not in invalid_chars else '' for char in name)
    
    return falid.replace(" ", separator)

def vtext(text: str) -> str:
    return text.replace('\n', '')
    ...