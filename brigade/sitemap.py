from datetime import datetime
import json

from flask_sitemap import Sitemap
from flask import Blueprint, send_from_directory, request

from cfapi import get_brigades


class SitemapBlueprint(Blueprint):
    '''
    Contain all the logic for generating a sitemap.xml
    '''
    STATIC_ROUTES = [
        'brigade.index',
        'brigade.about',
        'brigade.resources',
        'brigade.free_software_index',
    ]

    PER_BRIGADE_ROUTES = [
        'brigade.brigade',
        'brigade.projects',
    ]

    OTHER_ROUTES = [
        ('brigade.free_software_show', {"software": "bizspark"}),
        ('brigade.free_software_show', {"software": "twilio"}),
        ('brigade.free_software_show', {"software": "slack"}),
        ('brigade.free_software_show', {"software": "carto"}),
        ('brigade.free_software_show', {"software": "github"}),
    ]

    # NOTE: This is configured to output https URLs via the SITEMAP_URL_SCHEME
    # environment variable.
    def register(self, app, options, first_registration=False):
        sitemap = Sitemap(app=app)

        @app.route('/robots.txt')
        def static_from_root():
            return send_from_directory(app.static_folder, request.path[1:])

        @sitemap.register_generator
        def index():
            # (route, options, lastmod, changefreq, priority)
            for route in self.STATIC_ROUTES:
                yield (route, {}, None, 'monthly', '0.5')

            brigades = get_brigades()
            for brigade in brigades:
                last_updated = datetime.fromtimestamp(brigade['properties']['last_updated'])

                for route in self.PER_BRIGADE_ROUTES:
                    yield (
                        route,
                        {'brigadeid': brigade['id']},
                        last_updated.strftime("%Y-%m-%d"),
                        'weekly',
                        '1.0'
                    )


sitemap_blueprint = SitemapBlueprint('sitemap', __name__)
