from models import Room

def find_best_room(description):
    description = description.lower()
    keywords = {
        "двухместная": "double",
        "одноместная": "single",
        "с видом": "view",
        "тихо": "quiet"
    }

    for word, room_type in keywords.items():
        if word in description:
            return Room.query.filter_by(type=room_type, is_available=True).first()

    # если не нашли по ключевым словам — вернуть любую свободную
    return Room.query.filter_by(is_available=True).first()
