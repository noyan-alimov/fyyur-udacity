#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from datetime import datetime

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
# app.config.from_object('config')
app.config['SECRET_KEY'] = 'mysecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres:password@localhost:5432/fyyur'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=True)
    image_link = db.Column(db.String(500), nullable=True)
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    website_link = db.Column(db.String(), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    seeking = db.Column(db.Boolean, nullable=True)
    seeking_description = db.Column(db.String(), nullable=True)
    shows = db.relationship('Show', backref='venues', lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate


class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    website_link = db.Column(db.String(), nullable=True)
    genres = db.Column(db.ARRAY(db.String), nullable=False)
    image_link = db.Column(db.String(500), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    seeking = db.Column(db.Boolean, nullable=True)
    seeking_description = db.Column(db.String(), nullable=True)
    shows = db.relationship('Show', backref='artists', lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration.


class Show(db.Model):
    __tablename__ = 'shows'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    artist_id = db.Column(db.Integer, db.ForeignKey(
        'artists.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey(
        'venues.id'), nullable=False)


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#


@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    venues = Venue.query.all()
    data = []
    for venue in venues:
        city = venue.city
        state = venue.state
        specific_venues = Venue.query.filter_by(city=city, state=state).all()
        for specific_venue in specific_venues:
            id_of_specific_venue = specific_venue.id
            name_of_specific_venue = specific_venue.name
            number_of_shows_of_specific_venue = len(specific_venue.shows)
            obj = {
                'city': city,
                'state': state,
                'venues': [{
                    'id': id_of_specific_venue,
                    'name': name_of_specific_venue,
                    'num_upcoming_shows': number_of_shows_of_specific_venue
                }]
            }
            data.append(obj)

    # data = [{
    #     "city": "San Francisco",
    #     "state": "CA",
    #     "venues": [{
    #         "id": 1,
    #         "name": "The Musical Hop",
    #         "num_upcoming_shows": 0,
    #     }, {
    #         "id": 3,
    #         "name": "Park Square Live Music & Coffee",
    #         "num_upcoming_shows": 1,
    #     }]
    # }, {
    #     "city": "New York",
    #     "state": "NY",
    #     "venues": [{
    #         "id": 2,
    #         "name": "The Dueling Pianos Bar",
    #         "num_upcoming_shows": 0,
    #     }]
    # }]
    return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    response = {
        "count": 1,
        "data": [{
            "id": 2,
            "name": "The Dueling Pianos Bar",
            "num_upcoming_shows": 0,
        }]
    }
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id

    venues = Venue.query.all()
    shows = Show.query.all()
    past_shows = []
    upcoming_shows = []

    for show in shows:
        current_date = datetime.now()
        show_date = show.date
        if show_date > current_date:
            upcoming_shows.append(show)
        else:
            past_shows.append(show)

    def find_past_shows(venueId):
        if past_shows:
            for past_show in past_shows:
                if past_show.venue_id == venueId:
                    past_show_artist = Artist.query.get(past_show.artist_id)
                    return [{
                        'artist_id': past_show.artist_id,
                        'artist_name': past_show_artist.name,
                        'artist_image_link': past_show_artist.image_link,
                        'start_time': str(past_show.date)
                    }]
                else:
                    return []
        else:
            return []

    def find_upcoming_shows(venueId):
        if upcoming_shows:
            for upcoming_show in upcoming_shows:
                if upcoming_show.venue_id == venueId:
                    upcoming_show_artist = Artist.query.get(
                        upcoming_show.artist_id)
                    return [{
                        'artist_id': upcoming_show.artist_id,
                        'artist_name': upcoming_show_artist.name,
                        'artist_image_link': upcoming_show_artist.image_link,
                        'start_time': str(upcoming_show.date)
                    }]
                else:
                    return []
        else:
            return []

    venues_data = []

    for venue in venues:
        data = {
            'id': venue.id,
            'name': venue.name,
            'genres': venue.genres,
            'address': venue.address,
            'city': venue.city,
            'state': venue.state,
            'phone': venue.phone,
            'website': venue.website_link,
            'facebook_link': venue.facebook_link,
            'seeking_talent': venue.seeking,
            'seeking_description': venue.seeking_description,
            'image_link': venue.image_link,
            'past_shows': find_past_shows(venue.id),
            'upcoming_shows': find_upcoming_shows(venue.id),
            'past_shows_count': len(find_past_shows(venue.id)),
            'upcoming_shows_count': len(find_upcoming_shows(venue.id))}
        venues_data.append(data)

    venue = list(filter(lambda d: d['id'] ==
                        venue_id, venues_data))[0]
    return render_template('pages/show_venue.html', venue=venue)

#  Create Venue
#  ----------------------------------------------------------------


@app.route('/venues/create', methods=['GET', 'POST'])
def create_venue_form():
    form = VenueForm()
    if form.validate_on_submit():
        error = False
        try:
            venue = Venue(name=form.name.data, city=form.city.data, state=form.state.data,
                          address=form.address.data, phone=form.phone.data, genres=form.genres.data, website_link=form.website_link.data, image_link=form.image_link.data, facebook_link=form.facebook_link.data, seeking=form.seeking.data,
                          seeking_description=form.seeking_description.data)
            db.session.add(venue)
            db.session.commit()
        except:
            db.session.rollback()
            print('Error adding a new Venue to a database')
            flash('Error creating a new Venue')
            error = True
        finally:
            db.session.close()
        if not error:
            flash('Thank you for creating a Venue!')

    return render_template('forms/new_venue.html', form=form)


# @app.route('/venues/create', methods=['POST'])
# def create_venue_submission():
#     # TODO: insert form data as a new Venue record in the db, instead
#     # TODO: modify data to be the data object returned from db insertion

#     # on successful db insert, flash success
#     flash('Venue ' + request.form['name'] + ' was successfully listed!')
#     # TODO: on unsuccessful db insert, flash an error instead.
#     # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
#     # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
#     return render_template('pages/home.html')


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    # TODO: replace with real data returned from querying the database
    artists = Artist.query.all()
    data = []
    for artist in artists:
        obj = {
            'id': artist.id,
            'name': artist.name
        }
        data.append(obj)
    # data = [{
    #     "id": 4,
    #     "name": "Guns N Petals",
    # }, {
    #     "id": 5,
    #     "name": "Matt Quevedo",
    # }, {
    #     "id": 6,
    #     "name": "The Wild Sax Band",
    # }]
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    response = {
        "count": 1,
        "data": [{
            "id": 4,
            "name": "Guns N Petals",
            "num_upcoming_shows": 0,
        }]
    }
    return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the venue page with the given venue_id
    # TODO: replace with real venue data from the venues table, using venue_id

    artists = Artist.query.all()
    shows = Show.query.all()
    past_shows = []
    upcoming_shows = []

    for show in shows:
        current_date = datetime.now()
        show_date = show.date
        if show_date > current_date:
            upcoming_shows.append(show)
        else:
            past_shows.append(show)

    def find_past_shows(artistId):
        if past_shows:
            for past_show in past_shows:
                if past_show.artist_id == artistId:
                    past_show_venue = Venue.query.get(past_show.venue_id)
                    return [{
                        'venue_id': past_show.venue_id,
                        'venue_name': past_show_venue.name,
                        'venue_image_link': past_show_venue.image_link,
                        'start_time': str(past_show.date)
                    }]
                else:
                    return []
        else:
            return []

    def find_upcoming_shows(artistId):
        if upcoming_shows:
            for upcoming_show in upcoming_shows:
                if upcoming_show.artist_id == artistId:
                    upcoming_show_venue = Venue.query.get(
                        upcoming_show.venue_id)
                    return [{
                        'venue_id': upcoming_show.venue_id,
                        'venue_name': upcoming_show_venue.name,
                        'venue_image_link': upcoming_show_venue.image_link,
                        'start_time': str(upcoming_show.date)
                    }]
                else:
                    return []
        else:
            return []

    artists_data = []

    for artist in artists:
        data = {
            'id': artist.id,
            'name': artist.name,
            'genres': artist.genres,
            'city': artist.city,
            'state': artist.state,
            'phone': artist.phone,
            'website': artist.website_link,
            'facebook_link': artist.facebook_link,
            'seeking_venue': artist.seeking,
            'seeking_description': artist.seeking_description,
            'image_link': artist.image_link,
            'past_shows': find_past_shows(artist.id),
            'upcoming_shows': find_upcoming_shows(artist.id),
            'past_shows_count': len(find_past_shows(artist.id)),
            'upcoming_shows_count': len(find_upcoming_shows(artist.id))}
        artists_data.append(data)

    artist = list(filter(lambda d: d['id'] ==
                         artist_id, artists_data))[0]
    return render_template('pages/show_artist.html', artist=artist)

    #  Update
    #  ----------------------------------------------------------------


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = {
        "id": 4,
        "name": "Guns N Petals",
        "genres": ["Rock n Roll"],
        "city": "San Francisco",
        "state": "CA",
        "phone": "326-123-5000",
        "website": "https://www.gunsnpetalsband.com",
        "facebook_link": "https://www.facebook.com/GunsNPetals",
        "seeking_venue": True,
        "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
        "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
    }
    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # TODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes

    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    venue = {
        "id": 1,
        "name": "The Musical Hop",
        "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
        "address": "1015 Folsom Street",
        "city": "San Francisco",
        "state": "CA",
        "phone": "123-123-1234",
        "website": "https://www.themusicalhop.com",
        "facebook_link": "https://www.facebook.com/TheMusicalHop",
        "seeking_talent": True,
        "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
        "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
    }
    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # TODO: take values from the form submitted, and update existing
    # venue record with ID <venue_id> using the new attributes
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET', 'POST'])
def create_artist_form():
    form = ArtistForm()
    if form.validate_on_submit():
        error = False
        try:
            artist = Artist(name=form.name.data, city=form.city.data, state=form.state.data,
                            phone=form.phone.data, genres=form.genres.data,
                            website_link=form.website_link.data, image_link=form.image_link.data, facebook_link=form.facebook_link.data, seeking=form.seeking.data)
            db.session.add(artist)
            db.session.commit()
        except:
            db.session.rollback()
            print('Error creating a new Artist')
            flash('Error creating a new Artist')
            error = True
        finally:
            db.session.close()
        if not error:
            flash('Thank you for creating a new Artist')

    return render_template('forms/new_artist.html', form=form)


# @app.route('/artists/create', methods=['POST'])
# def create_artist_submission():
#     # called upon submitting the new artist listing form
#     # TODO: insert form data as a new Venue record in the db, instead
#     # TODO: modify data to be the data object returned from db insertion

#     # on successful db insert, flash success
#     flash('Artist ' + request.form['name'] + ' was successfully listed!')
#     # TODO: on unsuccessful db insert, flash an error instead.
#     # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
#     return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    data = [{
        "venue_id": 1,
        "venue_name": "The Musical Hop",
        "artist_id": 4,
        "artist_name": "Guns N Petals",
        "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
        "start_time": "2019-05-21T21:30:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 5,
        "artist_name": "Matt Quevedo",
        "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
        "start_time": "2019-06-15T23:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-01T20:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-08T20:00:00.000Z"
    }, {
        "venue_id": 3,
        "venue_name": "Park Square Live Music & Coffee",
        "artist_id": 6,
        "artist_name": "The Wild Sax Band",
        "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
        "start_time": "2035-04-15T20:00:00.000Z"
    }]
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create', methods=['GET', 'POST'])
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    if form.validate_on_submit():
        show = Show(artist_id=form.artist_id.data,
                    venue_id=form.venue_id.data, date=form.start_time.data)
        db.session.add(show)
        db.session.commit()
        flash('Thank you for creating a new Show')
    print(form.errors)
    return render_template('forms/new_show.html', form=form)


# @app.route('/shows/create', methods=['POST'])
# def create_show_submission():
#     # called to create new shows in the db, upon submitting new show listing form
#     # TODO: insert form data as a new Show record in the db, instead

#     # on successful db insert, flash success
#     flash('Show was successfully listed!')
#     # TODO: on unsuccessful db insert, flash an error instead.
#     # e.g., flash('An error occurred. Show could not be listed.')
#     # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
#     return render_template('pages/home.html')


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
