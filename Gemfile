source 'https://rubygems.org'

gem 'rails', '3.2.1'
gem "jquery-rails"

gem 'pg'

#Devise for user registration
gem "devise"

# Gem haml-rails for generators
gem "haml-rails"

#Rails Admin for managing the database
gem "rails_admin", :git => "git://github.com/sferik/rails_admin.git"

# Gems used only for assets and not required
# in production environments by default.
group :assets do
  gem 'sass-rails',   '~> 3.2.3'
  gem 'coffee-rails', '~> 3.2.1'

  # See https://github.com/sstephenson/execjs#readme for more supported runtimes
  # gem 'therubyracer'

  gem 'uglifier', '>= 1.0.3'
end

group :development, :test do

  # Pry is a nice drop in for irb, which allows for debugging
  # of your code anywhere 'binding.pry' is included
  gem 'pry'
  gem 'pry-remote'

  #Factory girl for using factories instead of fixtures
  gem 'factory_girl_rails'

end

group :test do
  gem 'database_cleaner'

  #Spork
  gem 'spork', '0.9.0.rc9'

  #Cucumber for better acceptance testing
  gem "cucumber-rails"

  #Rspec for testing instead of test::unit
  gem "rspec-rails"

  gem "launchy"

  #VCR for recording transcations with webmock
  gem 'webmock'
  gem 'vcr'

  # Guard for file monitoring
  gem 'rb-fsevent'
  gem 'guard'
  gem 'guard-bundler'
  gem 'guard-cucumber'
  gem 'guard-rspec'
  gem 'guard-spork'
  gem 'guard-livereload'
  gem 'guard-pow'
  gem 'guard-sass'
  gem 'guard-jasmine'

  gem "capybara-webkit"
end
