module ApplicationHelper

  def display_session_links
    classes = "btn btn-regular"
    if current_user
       header = (content_tag :li, (link_to(current_user.full_name, user_url(current_user))))
       header << (content_tag :li, raw(link_to('Admin', rails_admin_path))) if current_user.admin?
       header << (content_tag :li, link_to("Sign out", destroy_user_session_path, :class => classes, :method => :delete))
       return header
    else
      # Use '<<' to concat the two links so that they're returned together
      (content_tag :li, (link_to 'Sign In', sign_in_path, class: 'btn btn-regular')) 
       #<< (content_tag :li, (link_to 'Sign Up', new_user_registration_path, class: 'btn btn-info'))
    end
  end

  def display_join_button
      (content_tag :p, (link_to 'JOIN US!', new_user_registration_path, class: 'btn-large btn-join'))
  end


  def unsorted_grouped_options_for_select(grouped_options, selected_key = nil, prompt = nil)
    body = ''
    body << content_tag(:option, prompt, { :value => "" }, true) if prompt

    grouped_options.each do |group|
      body << content_tag(:optgroup, options_for_select(group[1], selected_key), :label => group[0])
    end

    body.html_safe
  end

  def user_session_management_link
    classes = "btn btn-regular"

    if user_signed_in?
      link_to("Sign out", destroy_user_session_path, :class => classes, :method => :delete)
    else
      link_to("Sign in", new_user_session_path, :class => classes)
    end
  end
end
