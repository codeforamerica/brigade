require "spec_helper"

describe "The application itself" do
  it "has no malformed whitespace" do
    Dir.chdir(File.expand_path("../..", __FILE__)) do
      files = `git ls-files`.split("\n").find_all do |filename|
        ignore = %w{tags Guardfile app/views/pages/race-for-reuse.html app/views/pages/race-for-reuse-2.html app/assets/stylesheets/r2r/style.css features/cassettes/cucumber_tags/vcr.yml features/support/env.rb lib/tasks/cucumber.rake spec/javascripts/helpers/jasmine-jquery-1.3.1.js spec/javascripts/helpers/mock-ajax.js}
        !ignore.include?(filename) && filename !~ /\.gitmodules|solr|vendor|fonts|cassettes|.DS_Store|\.png$|\.jpg$|\.gif$|\.pdf$|\.js$/
      end
      files.should be_well_formed
    end
  end
end
