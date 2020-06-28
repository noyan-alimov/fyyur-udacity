from app import Venue, Artist
import datetime

venues = Venue.query.all()

past_shows = []
upcoming_shows = []

for venue in venues:
    shows = venue.shows
    for show in shows:
        artist_id = show.artist_id
        artist = Artist.query.get(artist_id)
        # print(artist.image_link)
        # print(show.date)
        current_date = datetime.datetime.now()
        if show.date > current_date:
            upcoming_shows.append(show)
        else:
            past_shows.append(show)

print(len(upcoming_shows))
for upcoming_show in upcoming_shows:
    artist_id = upcoming_show.artist_id
    artist = Artist.query.get(artist_id)
    # print(len(upcoming_show))

# for venue in venues:
#     for past_show in past_shows:
#         for upcoming_show in upcoming_shows:
#             past_show_artist = Artist.query.get(past_show.artist_id)
#             upcoming_show_artist = Artist.query.get(upcoming_show.artist_id)
#             data = {
#                 'id': venue.id,
#                 'name': venue.name,
#                 'genres': venue.genres,
#                 'address': venue.address,
#                 'city': venue.city,
#                 'state': venue.state,
#                 'phone': venue.phone,
#                 'website': venue.website_link,
#                 'facebook_link': venue.facebook_link,
#                 'seeking_talent': venue.seeking,
#                 'seeking_description': venue.seeking_description,
#                 'image_link': venue.image_link,
#                 'past_shows': [{
#                     'artist_id': past_show.artist_id,
#                     'artist_name': past_show_artist.name,
#                     'artist_image_link': past_show_artist.image_link,
#                     'start_time': past_show.date
#                 }],
#                 'upcoming_shows': [{
#                     'artist_id': upcoming_show.artist_id,
#                     'artist_name': upcoming_show_artist.name,
#                     'artist_image_link': upcoming_show_artist.image_link,
#                     'start_time': upcoming_show.date
#                 }],
#                 'past_shows_count': venue,
#                 'upcoming_shows_count': venue}


data3 = {
    "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    "past_shows": [{
        "artist_id": 5,
        "artist_name": "Matt Quevedo",
        "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
        "start_time": "2019-06-15T23:00:00.000Z"
    }],
    "upcoming_shows": [{
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-01T20:00:00.000Z"
    }, {
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-08T20:00:00.000Z"
    }, {
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 1,
    "upcoming_shows_count": 1,
}
