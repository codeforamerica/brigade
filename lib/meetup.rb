require 'net/http'
require 'uri'
require 'json'

class Meetup

  API_KEY = '&key=f261167666d327123161b221b20585e'
  API_BASE_URL ='http://api.meetup.com/'

  attr_accessor :meetup_url, :meetup_id, :community_urlname

  def initialize(meetup_url)
    @meetup_url = meetup_url
    @community_urlname, @meetup_id, @meetup_description, @events = nil

    get_id
  end

  def get_id
    if URI(@meetup_url).path.include?("cfabrigade")
      @community_urlname = URI(@meetup_url).path.split('/').last
      @meetup_id = "cfabrigade"
    else
      @meetup_id = URI(@meetup_url).path.split('/').last
    end
  end

  def get_description
    if @community_urlname.nil?
      url = API_BASE_URL + "/2/groups?sign=true&group_urlname=" + @meetup_id
    else
      url = API_BASE_URL + "/ew/communities?&sign=true&urlname=cfabrigade&community_urlname=#{@community_urlname}"
    end

    meetup_response = Net::HTTP.get(URI(url + API_KEY))
    meetup_parsed = JSON.parse(meetup_response)["results"]
    @meetup_description =  meetup_parsed[0]

    @meetup_description    
  end

  def get_events
    if @community_urlname
      url = API_BASE_URL + "/ew/events?status=upcoming&sign=true&urlname=cfabrigade&community_urlname=#{@community_urlname}"
    else
      url = API_BASE_URL + "/2/events?status=upcoming&sign=true&group_urlname=" + @meetup_id
    end

    events_response = Net::HTTP.get(URI(url + API_KEY))
    events_parsed = JSON.parse(events_response)["results"]

    @events = events_parsed.to_a unless events_parsed.length == 0
  end
end