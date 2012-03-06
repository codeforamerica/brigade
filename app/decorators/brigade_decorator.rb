class BrigadeDecorator < ApplicationDecorator
  decorates :brigade

  def decorated_members
    raw_html = '<ul id="user-grid">'
    brigade.users.each do |user|
      raw_html << "<li>#{UserDecorator.new(user).as_link}</li>"
    end
    raw_html << '</ul>'

    h.raw raw_html
  end
end

