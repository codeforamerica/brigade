require 'net/http'
require 'uri'
require 'json'


class Meetup

  API_KEY = '&key=f261167666d327123161b221b20585e'
  API_BASE_URL ='http://api.meetup.com/2/'

  attr_accessor :meetup_url, :meetup_id

  def initialize(meetup_url)
    @meetup_url = meetup_url
    @meetup_id = get_id
    @meetup_description = nil
    @events = nil
  end

  def get_id
    URI(@meetup_url).path.split('/').last

    # if cfabrigade is the first path element.  Then use the meetup everywhere api... :(

  end

  def get_description
    
    url = API_BASE_URL + "groups?sign=true&group_urlname="

    if @meetup_description == nil
      meetup_response = Net::HTTP.get(URI(url + @meetup_id + API_KEY))
      meetup_parsed = JSON.parse(meetup_response)["results"]
      @meetup_description =  meetup_parsed[0]
    end

    return @meetup_description    
  end

  def get_events

    url = API_BASE_URL + "events?sign=true&group_urlname="

    events_response = Net::HTTP.get(URI(url + @meetup_id + API_KEY))
    events_parsed = JSON.parse(events_response)["results"]

    @events = events_parsed unless events_parsed.length == 0
  end



end