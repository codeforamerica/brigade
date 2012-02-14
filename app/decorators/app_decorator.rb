class AppDecorator < ApplicationDecorator
  decorates :application

  def participating_brigade_links
    brigade_links = application.participating_brigades.map do |brigade|
      h.link_to(brigade.name, h.brigade_path(brigade))
    end

    h.raw(brigade_links.join(' '))
  end

  def default_description
    if application.description
      application.description
    else
      h.raw application.civic_commons_description
    end
  end

end
