class BrigadeDecorator < ApplicationDecorator
  decorates :brigade

  def decorated_members
    if  brigade.users.uniq.any?
      raw_html = '<ul id="user-grid">'
      brigade.users.uniq.each do |user|
        raw_html << "<li>#{UserDecorator.new(user).as_link}</li>"
      end
      raw_html << '</ul>'

      h.raw raw_html
    else
      h.content_tag :i, 'There are currently no users participating'
    end
  end
end

