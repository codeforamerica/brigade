class UserDecorator < ApplicationDecorator
  decorates :user

  def contact_preference_message
    if user.opt_out
      'Does not want to be contacted by other civic hackers.'
    else
      'Does want to be contacted by other civic hackers.'
    end
  end

  def location_name
    if user.location
      user.location.name
    end
  end

  def avatar
    if user.avatar?
      h.image_tag model.avatar_url(:thumb), class: "thumbnail"
    else
      h.image_tag '/assets/avatar.jpg', class: "thumbnail"
    end
  end

  def skill_set
    user.skills * ", "
  end
end
