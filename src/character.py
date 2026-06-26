def getCharacterName(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    if not lines:
        return None
    
    character = lines[0].strip()

    print(f"Retrieved character name: {character}")
    return character

def removeCharacterName(filename, character):
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    with open(filename, 'w') as f:
        for line in lines:
            if line.strip() != character:
                f.write(line)