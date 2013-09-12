require 'rubygems'
require 'spork'
require 'sunspot_test/rspec'

Spork.prefork do
  # This file is copied to spec/ when you run 'rails generate rspec:install'
  ENV["RAILS_ENV"] ||= 'test'
  require "rails/application"
  require 'simplecov'
  SimpleCov.start 'rails'

  # Use of https://github.com/sporkrb/spork/wiki/Spork.trap_method-Jujutsu
  Spork.trap_method(Rails::Application, :reload_routes!)
  Spork.trap_method(Rails::Application::RoutesReloader, :reload!)

  # Prevent main application to eager_load in the prefork block (do not load files in autoload_paths)
  Spork.trap_method(Rails::Application, :eager_load!)

  require File.expand_path("../../config/environment", __FILE__)
  require 'rspec/rails'
  require 'rspec/autorun'
  require 'draper/rspec_integration'
  require 'email_spec'

  # Requires supporting ruby files with custom matchers and macros, etc,
  # in spec/support/ and its subdirectories.
  Dir[Rails.root.join("spec/support/**/*.rb")].each {|f| require f}

  RSpec.configure do |config|
    config.mock_with :rspec

    # Enable Specs to be targeted using :focus => true tag
    config.treat_symbols_as_metadata_keys_with_true_values = true
    config.filter_run :focus => true
    config.run_all_when_everything_filtered = true

    config.use_transactional_fixtures = true
    config.include Devise::TestHelpers, :type => :controller
    include CustomMatchers
    include EmailSpec::Helpers
    include EmailSpec::Matchers

    config.infer_base_class_for_anonymous_controllers = false
  end

  Geocoder.configure(:lookup => :test)

  Geocoder::Lookup::Test.set_default_stub(
      [
          {
              'latitude'     => 40.7143528,
              'longitude'    => -74.0059731,
              'address'      => 'New York, NY, USA',
              'state'        => 'New York',
              'state_code'   => 'NY',
              'country'      => 'United States',
              'country_code' => 'US'
          }
      ]
  )

  # Load all railties files
  Rails.application.railties.all { |r| r.eager_load! }

end

Spork.each_run do
  FactoryGirl.reload
end
