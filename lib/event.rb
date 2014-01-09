class Event
  def initialize(event_data)
    @event_data = event_data
  end

  def get_name
    @event_data['name'] || @event_data['short_description']
  end

  def get_venue_name
    if @event_data['venue']
      @event_data['venue']['name']
    elsif @event_data['community']
      @event_data['venue_name']
    end
  end

  def get_venue_address
    if @event_data['venue']
      @event_data['venue']['address_1']
    elsif @event_data['community']
      @event_data['address1']
    end
  end

  def get_event_url
    @event_data['event_url'] || @event_data['meetup_url']
  end

  def get_event_time
    if @event_data['time']
      formatted_time = Time.at(@event_data['time'] / 1000)
      formatted_time.strftime("%b %e %l:%M%p")
    end
  end
end