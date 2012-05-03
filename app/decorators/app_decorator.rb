class AppDecorator < ApplicationDecorator
  decorates :application

  def participating_brigade_links
    unless application.participating_brigades.uniq.empty?
      raw_html = '<ul class="unstyled">'
        application.participating_brigades.uniq.each do |brigade|
          raw_html << '<li>'
          raw_html << h.link_to(brigade.name, h.brigade_path(brigade))
          raw_html << '</li>'
        end
      raw_html << '</ul>'
      h.raw(raw_html)
    else
      h.content_tag :i, 'No brigades have deployed this application yet'
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
          raw_html << h.link_to(h.image_tag(pic.file_url(:thumb)), pic.file_url)
          raw_html << '</li>'
        end
      raw_html << '</ul>'

      h.raw(raw_html)
    end
  end

  def task_list
    unless application.tasks.empty?
      raw_html = '<ul class="check-boxes unstyled">'
      application.tasks(:order => 'id').each do |task|
        raw_html << "<li>#{task.description}<span class=\"check-this green\">%</span></li>"
      end
      raw_html << '</ul>'

      h.raw(raw_html)
    end
  end

  def decorated_deployed_application_users
    if deployed_application_users.any?
      raw_html = '<ul id="user-grid">'
      deployed_application_users.each do |user|
        raw_html << "<li>#{UserDecorator.new(user).as_link}</li>"
      end
      raw_html << '</ul>'

      h.raw raw_html
    else
      h.content_tag :i, 'There are currently no users participating'
    end
  end

  def repository_participation
    if model.repository_url.present?
      uri = URI.parse(model.repository_url.sub(/http:/, 'https:') + '/graphs/participation')
      http = Net::HTTP.new(uri.host, uri.port)
      http.use_ssl = true
      begin
        request = Net::HTTP::Get.new(uri.request_uri)
        json = JSON.parse(http.request(request).body)
      rescue
        json =''
      end
      return json['all'][22..52] if json['all'].present?
    end
  end

  def repository_sparkline
    participation = AppDecorator.new(model).repository_participation
    raw_html = ''
    unless participation.blank?
      raw_html << h.content_tag('td', '', class: 'inlinesparkline')
      h.raw raw_html
    else
      raw_html << h.content_tag('td','')
      h.raw raw_html
    end
  end

  def repository_sparkline_label
    participation = AppDecorator.new(model).repository_participation
    unless participation.blank?
      'Commits/30 days'
    end
  end

  def number_of_deploys
    model.deployed_applications.count
  end

  def repository_url_link
    handle_none model.repository_url do
      h.link_to 'Github repository', model.repository_url
    end
  end

  def irc_channel
    handle_none model.irc_channel do
      model.irc_channel
    end
  end

  def twitter_hashtag
    handle_none model.twitter_hashtag do
      model.twitter_hashtag
    end
  end

  def creator
    handle_none model.creator do
      model.creator
    end
  end

  def license
    handle_none model.license do
      model.license
    end
  end

  def mailing_list_url_link
    handle_none model.mailing_list do
      h.mail_to model.mailing_list, nil, :replace_at => "_at_", :replace_dot => "_dot_"
    end
  end


  private

  def handle_none(value)
    if value.present?
      yield
    else
      h.content_tag :span, "None supplied", class: "none"
    end
  end
end
