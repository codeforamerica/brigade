class AppDecorator < ApplicationDecorator
  decorates :application

  def participating_brigade_links
    brigade_links = application.participating_brigades.map do |brigade|
      h.link_to(brigade.name, h.brigade_path(brigade))
    end

    h.raw(brigade_links.join(' '))
  end
end
