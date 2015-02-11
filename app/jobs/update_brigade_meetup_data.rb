require 'net/http'
require 'uri'

class UpdateBrigadeMeetupData
  def self.update
    base = 'https://api.meetup.com/2/events'
    general = '/2/groups'
    events = '/2/events'

    Brigade.all.each do |brigade|
      events_response = Net::HTTP.get(URI("#{base}#{events}?status=upcoming&order=time&format=json&group_urlname=" + brigade.meetup_url ))
      events_parsed = JSON.parse(events_response)


      @events = parsed["results"].map do |event|
        { 
          :name => event["name"],
          :time => Time.at(event["time"] / 1000.0),
          :event_url => event["event_url"],
          :venue => {
            :name => event["venue"]["name"],
            :address_1 => event["venue"]["address_1"],
            :city => event["venue"]["city"],
            :state => event["venue"]["state"]
          }
        }
      end 
    end
  end
end