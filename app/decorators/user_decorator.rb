class UserDecorator < ApplicationDecorator
  decorates :user

  def contact_preference
    unless user.opt_in?
      'Does not want to be contacted by other civic hackers.'
    else
      h.mail_to user.email
    end
  end

  def location_name
    if user.location
      user.location.name
    end
  end

  def skill_set
    user.skills * ", "
  end

  def gravatar_small
    gravatar_image_tag(48)
  end

  def gravatar_medium
    gravatar_image_tag(128)
  end

  def as_link
    raw_html = ''
    if user.opt_in?
      raw_html << h.mail_to(user.email, gravatar_small)
    else
      raw_html << gravatar_small
    end
    raw_html << h.content_tag(:span, user.full_name + '&nbsp;(' + h.link_to('profile', h.user_url(user)) + ')', {class: 'hidden'})

    return h.raw raw_html
  end

  private

  def gravatar_image_tag(size)
    h.image_tag "http://www.gravatar.com/avatar/#{Digest::MD5.hexdigest(user.email)}?s=#{size}"
  end
end
