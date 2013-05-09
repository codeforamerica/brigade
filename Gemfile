source 'https://rubygems.org'

gem 'rails', '~> 3.2.11'

#Devise for user registration and cancan for authorization
gem 'devise', '~> 2.1.0'
gem 'cancan', '~> 1.6.7'

# Allow Devise to authenticate via github
gem 'omniauth-github', '~> 1.0.1'

# provide a comprehensive library of sass mixins
gem 'bourbon'

# alternate HTTP server for Rack applications
gem 'unicorn'

# for yaml parsing
gem 'psych'

#Simple form for better form management
gem 'simple_form', '~> 2.0.0.rc'

#Rails Admin for managing the database
gem 'rails_admin', '~> 0.4.4'
gem 'rails_admin_tag_list', :git => 'https://github.com/kryzhovnik/rails_admin_tag_list.git'

# Draper for nice decorators for the views
gem 'draper', '~> 0.14.0'

# Stamp and chronic for parsing and formatting dates
gem 'stamp', '~> 0.1.6'
gem 'chronic', '~> 0.6.7'

#for auto_link
gem 'rails_autolink'

# Kaminari for adding pagination
gem 'kaminari', '~> 0.14.1'
gem 'kaminari-bootstrap'

# Error messages
gem 'errship', '~> 2.2.0'

# Faraday to serve as middleware to perform requests on civic commons API
gem 'faraday', '~> 0.8.0'
gem 'faraday_middleware', '~> 0.8.4'

# Hashie to convert hashes to objects
gem 'hashie', '~> 1.2.0'

# CarrierWave for uploading files
gem 'rmagick', '~> 2.13.1', :require => 'RMagick'
gem 'carrierwave', '~> 0.6.2'

# fog for using Amazon S3 with carrierwave
gem 'fog', '~> 1.3.1'

# acts as taggable for tagging user skills and app requirements
gem 'acts-as-taggable-on', '~> 2.2.2'

#Sunspot for search with Solr
gem 'sunspot_rails', '~> 1.3.0'
gem 'sunspot_test'

# state_machine for adds support for creating state machines for attribute
gem 'state_machine', '~>1.1.2'

# geocoder to geocode city/state pairs
gem 'geocoder', '~> 1.1.1'

gem 'airbrake'

gem 'pg'

# HighVoltage for static pages
gem 'high_voltage'

# KISS Metrics
gem 'km'

# Gems used only for assets and not required
# in production environments by default.
group :assets do
  gem 'sass-rails',   '~> 3.2.6'
  gem 'coffee-rails', '~> 3.2.2'
  gem 'jquery-rails', '~> 2.2.0'

  # See https://github.com/sstephenson/execjs#readme for more supported runtimes
  # gem 'therubyracer'

  gem 'uglifier', '>= 1.0.3'
end

group :development, :test do

  # Pry is a nice drop in for irb, which allows for debugging
  # of your code anywhere 'binding.pry' is included
  gem 'pry', '~> 0.9.8'
  gem 'pry-remote', '~> 0.1.0'

  #Factory girl for using factories instead of fixtures
  gem 'factory_girl_rails', '~> 3.3.0'

  # Gem haml-rails for generators
  gem 'haml-rails', '~> 0.4'

  gem 'sunspot_solr', '~> 1.3.0'

  gem 'simplecov'

  #Rspec for testing instead of test::unit
  gem 'rspec-rails'
  gem 'heroku'
  gem 'taps'
  gem 'sqlite3'
end

group :test do
  gem 'database_cleaner', '~> 0.7.1'

  #Spork
  gem 'spork', '~> 0.9.2'

  #Cucumber for better acceptance testing
  gem 'cucumber-rails', '~> 1.3.0', require: false

  #Email spec for cucumber matchers for emails
  gem 'email_spec', '~> 1.2.1'

  gem 'launchy', '~> 2.1.0'

  #VCR for recording transcations with webmock
  gem 'webmock', '~> 1.8.7'
  gem 'vcr', '~> 2.1.1'

  # Guard for file monitoring
  gem 'rb-fsevent', '~> 0.9.0'
  gem 'guard', '~> 1.0.0'
  gem 'guard-bundler', '~> 0.1.3'
  gem 'guard-cucumber', '~> 0.8.0'
  gem 'guard-rspec', '~> 0.7.0'
  gem 'guard-spork', '~> 0.8.0'
  gem 'guard-livereload', '~> 0.4.0'
  gem 'guard-pow', '~> 0.2.1'

  gem 'capybara-webkit', '~> 0.12.0'
end
