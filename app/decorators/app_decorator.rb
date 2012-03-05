class AppDecorator < ApplicationDecorator
  decorates :application

  def participating_brigade_links
    unless application.participating_brigades.empty?
      raw_html = '<ul class="unstyled">'
        application.participating_brigades.each do |brigade|
          raw_html << '<li>'
          raw_html << h.link_to(brigade.name, h.brigade_path(brigade))
          raw_html << '</li>'
        end
      raw_html << '</ul>'
      h.raw(raw_html)
    end
  end

  def default_description
    if application.description && ! application.description.empty?
      application.description
    else
      h.raw application.civic_commons_description
    end
  end

  def picture_gallary
    unless application.pictures.empty?
      raw_html = '<ul class="thumbnails">'
        application.pictures.each do |pic|
          raw_html << '<li class="span2">'
          raw_html << h.image_tag(pic.file_url(:thumb))
          raw_html << '</li>'
        end
      raw_html << '</ul>'

      h.raw(raw_html)
    end
  end

  def task_list
    unless application.tasks.empty?
      raw_html = '<ul class="check-boxes unstyled">'
      application.tasks.each do |task|
        raw_html << "<li>#{task.description}<span class=\"check-this green\">%</span></li>"
      end
      raw_html << '</ul>'

      h.raw(raw_html)
    end
  end

  def decorated_deployed_application_users
    raw_html = '<ul id="user-grid">'
    deployed_application_users.each do |user|
      raw_html << "<li>#{UserDecorator.new(user).as_link}</li>"
    end
    raw_html << '</ul>'

    h.raw raw_html
  end
end
