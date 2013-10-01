require 'net/http'
require 'uri'
require 'json'

task :get_meetup_events => :environment do
  base = 'http://api.meetup.com'
  events = '/2/events?sign=true&group_urlname='
  api_key = 'f261167666d327123161b221b20585e'

  Brigade.all.each do |brigade|
    if brigade.meetup_url
      events_response = Net::HTTP.get(URI(base + events + brigade.meetup_url + "&key=#{api_key}"))
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
      brigade.meetup_json_data = @events.to_json
      brigade.save!
    end
  end
end



task :get_meetup_description => :environment do
  base = 'http://api.meetup.com'
  general = '/2/groups?sign=true&group_urlname='
  api_key = 'f261167666d327123161b221b20585e'

  Brigade.all.each do |brigade|
    if brigade.meetup_url
      meetup_response = Net::HTTP.get(URI(base + general + brigade.meetup_url + "&key=#{api_key}"))
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