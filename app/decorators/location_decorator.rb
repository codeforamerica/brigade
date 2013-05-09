class LocationDecorator < ApplicationDecorator
  decorates :location

  def decorated_members
    if  location.users.uniq.any?
      raw_html = '<ul id="user-grid">'
      location.users.uniq.each do |user|
        raw_html << "<li>#{UserDecorator.new(user).as_link}</li>"
      end
      raw_html << '</ul>'

      h.raw raw_html
    else
      h.content_tag :i, 'There are currently no users participating'
    end
  end
end

