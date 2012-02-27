class AppDecorator < ApplicationDecorator
  decorates :application

  def participating_brigade_links
    brigade_links = application.participating_brigades.map do |brigade|
      h.link_to(brigade.name, h.brigade_path(brigade))
    end

    h.raw(brigade_links.join('<br/>'))
  end

  def default_description
    if application.description
      application.description
    else
      h.raw application.civic_commons_description
    end
  end

  def picture_gallary
    unless application.pictures.empty?
      raw_html = '<ul class="thumbnails">'
        application.pictures.each do |pic|
          raw_html << '<li class="span3">'
          raw_html << h.image_tag(pic.file_url(:thumb), class: "thumbnail")
          raw_html << '</li>'
        end
      raw_html << '</ul>'

      h.raw(raw_html)
    end
  end
end
