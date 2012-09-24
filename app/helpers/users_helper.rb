module UsersHelper
  def display_brigades?(user)
    user.brigades.any?
  end

  def brigade_links(user)
    html_safe user.brigades.uniq.map do |brigade|
      link_to(brigade.name, brigade_url(brigde))
    end.join(", ")
  end
end
