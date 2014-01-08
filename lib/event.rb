class Event
  def initialize(event_data)
    @event_data = event_data
  end

  def get_name
    @event_data['name']
  end

  def get_venue_name
    @event_data['venue']['name'] if @event_data['venue']
  end

  def get_venue_address
    @event_data['venue']['address_1'] if @event_data['venue']
  end

  def get_event_url
    @event_data['event_url']
  end

  def get_event_time
    if @event_data['time']
      formatted_time = Time.at(@event_data['time'] / 1000)
      formatted_time.strftime("%b %e %l:%M%p")
    end
  end
end