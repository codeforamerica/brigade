class AppDecorator < ApplicationDecorator
  decorates :application

  def participating_brigade_links
    raw_html = '<ul class="unstyled">'
      application.participating_brigades.each do |brigade|
        raw_html << '<li>'
        raw_html << h.link_to(brigade.name, h.brigade_path(brigade))
        raw_html << '</li>'
      end
    raw_html << '</ul>'
    h.raw(raw_html)
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
end
