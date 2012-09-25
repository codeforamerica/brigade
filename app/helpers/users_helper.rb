module UsersHelper
  def display_brigades?(user)
    user.brigades.any?
  end

  def brigade_links(user)
    unless user.brigades.empty?
      raw user.brigades.uniq.map{|b| link_to b.name, brigade_url(:id => b.id)}.join(', ')
    end
  end
end
