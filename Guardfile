# A sample Guardfile
# More info at https://github.com/guard/guard#readme

guard 'bundler' do
  watch('Gemfile')
end

guard 'livereload' do
  watch(%r{app/.+\.(erb|haml)})
  watch(%r{app/helpers/.+\.rb})
  watch(%r{(public/|app/assets).+\.(css|js|html)})
  watch(%r{(app/assets/.+\.css)\.s[ac]ss}) { |m| m[1] }
  watch(%r{(app/assets/.+\.js)\.coffee}) { |m| m[1] }
  watch(%r{config/locales/.+\.yml})
end

guard 'pow' do
  watch('.powrc')
  watch('.powenv')
  watch('.rvmrc')
  watch('Gemfile')
  watch('Gemfile.lock')
  watch('config/application.rb')
  watch('config/environment.rb')
  watch(%r{^config/environments/.*\.rb$})
  watch(%r{^config/initializers/.*\.rb$})
end

guard 'spork', wait: 60, cucumber: true, rspec: true, test_unit: false do
  watch('config/application.rb')
  watch('config/environment.rb')
  watch(%r{^config/environments/.+\.rb$})
  watch(%r{^config/initializers/.+\.rb$})
  watch('Gemfile')
  watch('spec/spec_helper.rb')
end

guard 'cucumber', bundle: false, keep_failed: true, cli: '--drb --format pretty --color --strict --no-profile --tags ~@slow --tags ~@wip'  do
  watch(%r{^app/(.+)\.rb$})
  watch(%r{^app/(.+)\.erb$})
  watch(%r{^app/(.+)\.haml$})
  watch(%r{^lib/(.+)\.rb$})
  watch(%r{^features/.+\.feature$})
  watch(%r{^features/support/.+$})          { 'features' }
  watch(%r{^features/step_definitions/(.+)_steps\.rb$})
end

guard 'rspec', version: 2, cli: '--drb --format progress --color' do
  watch(%r{^spec/.+_spec\.rb$})
  watch(%r{^spec/factories/(.+).rb$})
  watch(%r{^lib/(.+)\.rb$})     { |m| "spec/lib/#{m[1]}_spec.rb" }
  watch('spec/spec_helper.rb')  { "spec" }

  # Rails example
  watch(%r{^spec/.+_spec\.rb$})
  watch(%r{^app/(.+)\.rb$})                           { |m| "spec/#{m[1]}_spec.rb" }
  watch(%r{^lib/(.+)\.rb$})                           { |m| "spec/lib/#{m[1]}_spec.rb" }
  watch(%r{^app/controllers/(.+)_(controller)\.rb$})  { |m| ["spec/routing/#{m[1]}_routing_spec.rb", "spec/#{m[2]}s/#{m[1]}_#{m[2]}_spec.rb"] }
  watch(%r{^spec/support/(.+)\.rb$})                  { "spec" }
  watch('spec/spec_helper.rb')                        { "spec" }
  watch('app/controllers/application_controller.rb')  { "spec/controllers" }
end

# guard 'jasmine' do
#   watch(%r{app/assets/javascripts/(.+)\.(js\.coffee|js|coffee)$}) { |m| "spec/javascripts/#{m[1]}_spec.#{m[2]}" }
#   watch(%r{spec/javascripts/(.+)_spec\.(js\.coffee|js|coffee)$})  { |m| puts m.inspect; "spec/javascripts/#{m[1]}_spec.#{m[2]}" }
#   watch(%r{spec/javascripts/spec\.(js\.coffee|js|coffee)$})       { "spec/javascripts" }
# end
