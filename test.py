from app import Artist, Show, Venue
from datetime import datetime

# artists = Artist.query.all()
# shows = Show.query.all()
# past_shows = []
# upcoming_shows = []

# for show in shows:
#     current_date = datetime.now()
#     show_date = show.date
#     if show_date > current_date:
#         upcoming_shows.append(show)
#     else:
#         past_shows.append(show)


# def find_past_shows(artistId):
#     if past_shows:
#         for past_show in past_shows:
#             if past_show.artist_id == artistId:
#                 past_show_venue = Venue.query.get(past_show.venue_id)
#                 return [{
#                     'venue_id': past_show.venue_id,
#                     'venue_name': past_show_venue.name,
#                     'venue_image_link': past_show_venue.image_link,
#                     'start_time': str(past_show.date)
#                 }]
#             else:
#                 return []
#     else:
#         return []


# def find_upcoming_shows(artistId):
#     if upcoming_shows:
#         for upcoming_show in upcoming_shows:
#             if upcoming_show.artist_id == artistId:
#                 upcoming_show_venue = Venue.query.get(
#                     upcoming_show.venue_id)
#                 return [{
#                     'venue_id': upcoming_show.venue_id,
#                     'venue_name': upcoming_show_venue.name,
#                     'venue_image_link': upcoming_show_venue.image_link,
#                     'start_time': str(upcoming_show.date)
#                 }]
#             else:
#                 return []
#     else:
#         return []


# artists_data = []

# for artist in artists:
#     data = {
#         'id': artist.id,
#         'name': artist.name,
#         'genres': artist.genres,
#         'city': artist.city,
#         'state': artist.state,
#         'phone': artist.phone,
#         'website': artist.website_link,
#         'facebook_link': artist.facebook_link,
#         'seeking_venue': artist.seeking,
#         'seeking_description': artist.seeking_description,
#         'image_link': artist.image_link,
#         'past_shows': find_past_shows(artist.id),
#         'upcoming_shows': find_upcoming_shows(artist.id),
#         'past_shows_count': len(find_past_shows(artist.id)),
#         'upcoming_shows_count': len(find_upcoming_shows(artist.id))}
#     artists_data.append(data)

# artist = list(filter(lambda d: d['id'] ==
#                      1, artists_data))[0]

# print(artists_data)

venues = Venue.query.all()
artists = Artist.query.all()

for venue in venues:
    print(venue.genres)

for artist in artists:
    print(artist.genres)
