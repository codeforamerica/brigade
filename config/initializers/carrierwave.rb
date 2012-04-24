CarrierWave.configure do |config|
  config.storage :fog

  config.fog_credentials = {
    :provider               => 'AWS',
    :aws_access_key_id      => ENV['S3_ACCESS_KEY'],
    :aws_secret_access_key  => ENV['S3_SECRET']
  }

  config.cache_dir = "#{Rails.root}/tmp/uploads"

  if Rails.env.production?
    config.fog_directory  = 'brigade-production'
  elsif Rails.env.test?
    config.fog_directory  = 'brigade-test'
  else
    config.fog_directory  = 'brigade-dev'
  end
end
