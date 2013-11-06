require 'net/http'
require 'uri'
require 'json'

namespace :meetup do

  desc "get upcoming brigade events from group's meetup page"
  task :get_events => :environment do
    base = 'http://api.meetup.com'
    events = '/2/events?sign=true&group_urlname='
    api_key = 'f261167666d327123161b221b20585e'

    Brigade.all.each do |brigade|
      if brigade.meetup_url
        meetup = URI(brigade.meetup_url).path.split('/').last

        events_response = Net::HTTP.get(URI(base + events + meetup + "&key=#{api_key}"))
        events_parsed = JSON.parse(events_response)

        @events = events_parsed["results"].map do |event|
          { 
            :name => event["name"],
            :time => Time.at(event["time"] / 1000.0),
            :event_url => event["event_url"],
            :venue => {
              ## return empty array if no events upcoming
              :name => event["venue"] && event["venue"]["name"],
              :address_1 => event["venue"] && event["venue"]["address_1"],
              :city => event["venue"] && event["venue"]["city"],
              :state => event["venue"] && event["venue"]["state"]
            }
          }

        end
        events_json = JSON.parse(brigade.meetup_json_data)
        events_json[0]['events'] = @events
        brigade.meetup_json_data = events_json.to_json
        brigade.save!
      end
    end
  end


  desc "get brigade description from meetup profiles"
  task :get_description => :environment do
    base = 'http://api.meetup.com'
    general = '/2/groups?sign=true&group_urlname='
    api_key = 'f261167666d327123161b221b20585e'

    Brigade.all.each do |brigade|
      if brigade.meetup_url
        meetup = URI(brigade.meetup_url).path.split('/').last

        meetup_response = Net::HTTP.get(URI(base + general + meetup + "&key=#{api_key}"))
        meetup_parsed = JSON.parse(meetup_response)

        @info = meetup_parsed["results"].map do |info|
          {
            :name => info["name"],
            :members_count => info["members"],
            :description => info["description"]
          }
        end

        brigade.meetup_json_data = @info.to_json
        brigade.save!
      end
    end
  end

end