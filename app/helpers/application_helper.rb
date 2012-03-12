module ApplicationHelper

  def display_session_links
    if current_user
       header = (content_tag :li, (raw('Welcome, ' + link_to(current_user.full_name, user_url(current_user)))))
       header << (content_tag :li, raw(link_to('Admin', rails_admin_path))) if current_user.admin?
       header << (content_tag :li, (link_to 'Sign Out', sign_out_path))
       return header
    else
      # Use '<<' to concat the two links so that they're returned together
      (content_tag :li, (link_to 'Sign In', sign_in_path, class: 'btn btn-regular')) << (content_tag :li, (link_to 'Sign Up', new_user_registration_path, class: 'btn btn-info'))
    end
  end


  def unsorted_grouped_options_for_select(grouped_options, selected_key = nil, prompt = nil)
    body = ''
    body << content_tag(:option, prompt, { :value => "" }, true) if prompt

    grouped_options.each do |group|
      body << content_tag(:optgroup, options_for_select(group[1], selected_key), :label => group[0])
    end

    body.html_safe
  end
end
