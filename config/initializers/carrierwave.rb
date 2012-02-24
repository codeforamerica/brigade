CarrierWave.configure do |config|
  config.storage :fog

  config.fog_credentials = {
    :provider               => 'AWS',
    :aws_access_key_id      => 'AKIAJM7D4ASWWMB6TOTA',
    :aws_secret_access_key  => ENV['S3_SECRET']
  }

  config.cache_dir = "#{Rails.root}/tmp/uploads"

  if Rails.env.production?
    config.fog_directory  = 'brigade_production'
  elsif Rails.env.test?
    config.fog_directory  = 'brigade_test'
  else
    config.fog_directory  = 'brigade_dev'
  end
end
