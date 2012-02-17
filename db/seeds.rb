[ 'Application Name', 'Other Name', 'Random Name'].each { |app_name| Application.create!(name: app_name) }

[ 'Titans Brigade', 'Code For America Brigade', 'Thoughbot Brigade'].each { |brigade_name| Brigade.create!(name: brigade_name) }

[ 'Norfolk, VA', 'San Fransico, CA', 'Boston, MA' ].each { |location_name| Location.create!(name: location_name) }

Application.all.each do |app|
  Brigade.all.each do |brigade|
    Location.all.each do |location|
      DeployedApplication.create!(application_id: app.id, brigade_id: brigade.id, location_id: location.id)
    end
  end
end
