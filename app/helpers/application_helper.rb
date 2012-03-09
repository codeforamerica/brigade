module ApplicationHelper

  def display_session_links
    if current_user
       (content_tag :li, (raw('Welcome, ' + link_to(current_user.full_name, user_url(current_user))))) << (content_tag :li, (link_to 'Sign Out', sign_out_path)) 
    else
      # Use '<<' to concat the two links so that they're returned together
      (content_tag :li, (link_to 'Sign In', sign_in_path)) << (content_tag :li, (link_to 'Sign Up', new_user_registration_path))
    end
  end
end
