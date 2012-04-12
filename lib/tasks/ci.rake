namespace :ci do

  desc "Run tests on Travis"
  task :travis do
    if ENV['BUILD_TYPE'] == 'cucumber'
      puts "Running cucumber features..."
      system("export DISPLAY=:99.0 && bundle exec rake cucumber")
      raise "Cucumber failed!" unless $?.exitstatus == 0
    else
      ["rake spec"].each do |cmd|
        puts "Running bundle exec #{cmd}..."
        system("bundle exec #{cmd}")
        raise "#{cmd} failed!" unless $?.exitstatus == 0
      end
    end
  end

end

task :travis => "ci:travis"
