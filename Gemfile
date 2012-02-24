source 'https://rubygems.org'

gem 'rails', '~> 3.2.1'

gem 'pg', '~> 0.12.1'

#Devise for user registration and cancan for authorization
gem 'devise', '~> 2.0.0'
gem 'cancan', '~> 1.6.7'

# Allow Devise to authenticate via github
gem 'omniauth-github', '~> 1.0.1'

# provide a comprehensive library of sass mixins
gem 'bourbon'

# alternate HTTP server for Rack applications
gem 'unicorn'

#Simple form for better form management
gem 'simple_form', '~> 2.0.0.rc'

#Rails Admin for managing the database
gem "rails_admin", :git => "git://github.com/sferik/rails_admin.git"

# Draper for nice decorators for the views
gem 'draper', '~> 0.10.0'

# Stamp and chronic for parsing and formatting dates
gem 'stamp', '~> 0.1.6'
gem 'chronic', '~> 0.6.7'

# Kaminari for adding pagination
gem 'kaminari', '~> 0.13.0'

# Faraday to serve as middleware to perform requests on civic commons API
gem 'faraday', '~> 0.7.6'
gem 'faraday_middleware', '~> 0.8.4'

# Hashie to convert hashes to objects
gem 'hashie', '~> 1.2.0'

# CarrierWave for uploading files
gem 'rmagick', '~> 2.13.1', :require => 'RMagick'
gem 'carrierwave', '~> 0.5.8'

# fog for using Amazon S3 with carrierwave
gem 'fog', '~> 1.1.2'

# acts as taggable for tagging user skills and app requirements
gem 'acts-as-taggable-on', '~> 2.2.2'

# Gems used only for assets and not required
# in production environments by default.
group :assets do
  gem 'sass-rails',   '~> 3.2.3'
  gem 'coffee-rails', '~> 3.2.1'
  gem "jquery-rails", '~> 2.0.0'

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
  gem 'factory_girl_rails', '~> 1.6.0'

  # Gem haml-rails for generators
  gem 'haml-rails', '~> 0.3.4'
end

group :test do
  gem 'database_cleaner', '~> 0.7.1'

  #Spork
  gem 'spork', '~> 0.9.0'

  #Cucumber for better acceptance testing
  gem 'cucumber-rails', '~> 1.2.1'

  #Rspec for testing instead of test::unit
  gem "rspec-rails", '~> 2.8.1'

  gem 'launchy', '~> 2.0.5'

  #VCR for recording transcations with webmock
  gem 'webmock', '~> 1.7.10'
  gem 'vcr', '~> 1.11.3'

  # Guard for file monitoring
  gem 'rb-fsevent', '~> 0.9.0'
  gem 'guard', '~> 1.0.0'
  gem 'guard-bundler', '~> 0.1.3'
  gem 'guard-cucumber', '~> 0.7.5'
  gem 'guard-rspec', '~> 0.6.0'
  gem 'guard-spork', '~> 0.5.2'
  gem 'guard-livereload', '~> 0.4.0'
  gem 'guard-pow', '~> 0.2.1'

  gem "capybara-webkit", '~> 0.9.0'
end
