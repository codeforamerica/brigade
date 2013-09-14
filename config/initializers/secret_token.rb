# Be sure to restart your server when you modify this file.

# Your secret key for verifying the integrity of signed cookies.
# If you change this key, all old signed cookies will become invalid!
# Make sure the secret is at least 30 characters and all random,
# no regular words or you'll be exposed to dictionary attacks.

if Rails.env.production? && ENV['SECRET_TOKEN'].blank?
  raise 'The SECRET_TOKEN environment variable is not set. To generate it, run "rake secret", then set it on the production server. If you\'re using Heroku, you do this with "heroku config:set SECRET_TOKEN=the_token_you_generated"'
end

CodeForAmerica::Application.config.secret_token = ENV['SECRET_TOKEN'] || '6b1e071e036f4774088668dd143b1192d762a23d7b14d27f90e8297d48b8dde273d8172454ad9ce91db20b7fcb3e544be2c3cdc28443d5a3f64f31f31b649a95'
