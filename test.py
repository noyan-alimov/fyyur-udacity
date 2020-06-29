from app import Artist

artists = Artist.query.all()

data = []
for artist in artists:
    obj = {
        'id': artist.id,
        'name': artist.name
    }
    data.append(obj)

print(data)
