require 'net/http'
require 'uri'
require 'json'
require 'meetup'

namespace :meetup do

  desc "get upcoming brigade events from group's meetup page"
  task :update => :environment do

    Brigade.all.each do |brigade|
      if brigade.meetup_url
        m = Meetup.new(brigade.meetup_url)

        meetup_description = m.get_description
        meetup_description['events'] = m.get_events

        brigade.meetup_json_data = meetup_description.to_json
        brigade.save!
      end
    end
  end
end