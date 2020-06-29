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
    form = VenueSubmit()
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
            flash('An error occurred. Venue ' +
                  venue.name + ' could not be listed.')
            error = True
        finally:
            db.session.close()
        if not error:
            flash('Venue ' + request.form['name'] +
                  ' was successfully listed!')

    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/<int:venue_id>/delete', methods=['GET', 'POST'])
def delete_venue(venue_id):
    # TODO: Complete this endpoint for taking a venue_id, and using
    # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
    venue = Venue.query.get(venue_id)
    error = False
    try:
        db.session.delete(venue)
        db.session.commit()
    except:
        db.session.rollback()
        flash('Error deleting a venue')
        print('Error deleting a venue')
        error = True
    finally:
        db.session.close()
    if not error:
        flash('Venue has been deleted')
        return redirect(url_for('index'))

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage

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


@app.route('/artists/<int:artist_id>/edit', methods=['GET', 'POST'])
def edit_artist(artist_id):
    form = ArtistUpdate()
    artist = Artist.query.get(artist_id)
    error = False

    if form.validate_on_submit():
        try:
            artist.name = form.name.data
            artist.city = form.city.data
            artist.state = form.state.data
            artist.phone = form.phone.data
            artist.genres = form.genres.data
            artist.website_link = form.website_link.data
            artist.facebook_link = form.facebook_link.data
            artist.image_link = form.image_link.data
            artist.seeking = form.seeking.data
            artist.seeking_description = form.seeking_description.data

            db.session.commit()
        except:
            db.session.rollback()
            flash('Error editing an artist')
            error = True
        finally:
            db.session.close()
        if not error:
            flash('Edited an artist!')
            return redirect(url_for('index'))

    elif request.method == 'GET':
        form.name.data = artist.name
        form.city.data = artist.city
        form.state.data = artist.state
        form.phone.data = artist.phone
        form.genres.data = artist.genres
        form.website_link.data = artist.website_link
        form.facebook_link.data = artist.facebook_link
        form.image_link.data = artist.image_link
        form.seeking.data = artist.seeking
        form.seeking_description.data = artist.seeking_description

    # TODO: populate form with fields from artist with ID <artist_id>
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/venues/<int:venue_id>/edit', methods=['GET', 'POST'])
def edit_venue(venue_id):
    form = VenueUpdate()
    venue = Venue.query.get(venue_id)
    error = False

    if form.validate_on_submit():
        try:
            venue.name = form.name.data
            venue.city = form.city.data
            venue.state = form.state.data
            venue.address = form.address.data
            venue.phone = form.phone.data
            venue.genres = form.genres.data
            venue.website_link = form.website_link.data
            venue.facebook_link = form.facebook_link.data
            venue.image_link = form.image_link.data
            venue.seeking = form.seeking.data
            venue.seeking_description = form.seeking_description.data

            db.session.commit()
        except:
            db.session.rollback()
            flash('Error editing a venue')
            error = True
        finally:
            db.session.close()
        if not error:
            flash('Edited a venue!')
            return redirect(url_for('index'))

    elif request.method == 'GET':
        form.name.data = venue.name
        form.city.data = venue.city
        form.state.data = venue.state
        form.address.data = venue.address
        form.phone.data = venue.phone
        form.genres.data = venue.genres
        form.website_link.data = venue.website_link
        form.facebook_link.data = venue.facebook_link
        form.image_link.data = venue.image_link
        form.seeking.data = venue.seeking
        form.seeking_description.data = venue.seeking_description

    # TODO: populate form with values from venue with ID <venue_id>
    return render_template('forms/edit_venue.html', form=form, venue=venue)

#  Create Artist
#  ----------------------------------------------------------------


@app.route('/artists/create', methods=['GET', 'POST'])
def create_artist_form():
    form = ArtistSubmit()
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
            flash('An error occurred. Artist ' +
                  artist.name + ' could not be listed.')
            error = True
        finally:
            db.session.close()
        if not error:
            flash('Artist ' + request.form['name'] +
                  ' was successfully listed!')

    return render_template('forms/new_artist.html', form=form)


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # TODO: replace with real venues data.
    #       num_shows should be aggregated based on number of upcoming shows per venue.
    shows = Show.query.all()
    data = []

    def find_venue_name(venueId):
        venue = Venue.query.get(venueId)
        return venue.name

    def find_artist_name(artistId):
        artist = Artist.query.get(artistId)
        return artist.name

    def find_artist_image(artistId):
        artist = Artist.query.get(artistId)
        return artist.image_link

    for show in shows:
        obj = {
            'venue_id': show.venue_id,
            'venue_name': find_venue_name(show.venue_id),
            'artist_id': show.artist_id,
            'artist_name': find_artist_name(show.artist_id),
            'artist_image_link': find_artist_image(show.artist_id),
            'start_time': str(show.date)
        }
        data.append(obj)

    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create', methods=['GET', 'POST'])
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    if form.validate_on_submit():
        error = False
        try:
            show = Show(artist_id=form.artist_id.data,
                        venue_id=form.venue_id.data, date=form.start_time.data)
            db.session.add(show)
            db.session.commit()
        except:
            db.session.rollback()
            flash('Error listing a new Show')
            error = True
        finally:
            db.session.close()
        if not error:
            flash('Thank you for listing a new Show')

    return render_template('forms/new_show.html', form=form)


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
