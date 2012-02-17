Dir["#{Rails.root}/app/jobs/*.rb"].each { |file| require file }

desc "This task is called by the Heroku scheduler add-on to retrieve application data from civic commons and cache it locally"
task :cache_civic_commons_application_data => :environment do
  puts "Updating all applications with civic commons data..."
  UpdateApplicationsFromCivicCommons.perform
  puts "done."
end
