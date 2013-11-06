require 'net/http'
require 'uri'
require 'json'


module CheckMeetupParams
  def valid_url(base, brigade_url, api_params)
    
    brigade = URI(brigade_url).path.split('/').last

    begin
      # construct a url like:
      # http://api.meetup.com/2/events?sign=true&group_urlname=betanyc&key=1234567890
      events_response = Net::HTTP.get(URI(base + meetup + api_params))
      events_parsed = JSON.parse(events_response)

      raise NoResultsError if events_parsed["results"].empty?
    rescue
      puts 'save from api timeout'
    end
  end

end