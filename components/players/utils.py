def get_role_from_name(name, players):
    role = None
    for p in players:
        if p.name == name:
            role = p.get_type()
            break
    return role