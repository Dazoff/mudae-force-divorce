def getCharacterName(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    if not lines:
        return None
    
    character = lines[0].strip()
    
    with open(filename, 'w') as f:
        f.writelines(lines[1:])

    print(f"Retrieved character name: {character}")
    return character