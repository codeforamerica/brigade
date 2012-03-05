# Production Data
[ '14133', '14387', '13422', '13685', '14012', '14110', '13489', '13465', '13744', '13808' ].each { |node_id| Application.create!(nid: node_id) }

# Github repos to be associated
# https://github.com/derekeder/Chicago-Buildings
# https://github.com/codeforamerica/adopt-a-hydrant
# https://github.com/open-city/Look-at-Cook
# https://github.com/codeforamerica/public_art_finder
# https://github.com/openplans/shareabouts/

# Test and Dev Data
[ 'Titans Brigade', 'Code For America Brigade', 'Thoughbot Brigade'].each { |brigade_name| Brigade.create!(name: brigade_name) }

[ 'Norfolk, VA', 'San Fransisco, CA', 'Boston, MA' ].each { |location_name| Location.create!(name: location_name) }

Application.all.each do |app|

  5.times do |i|
    app.tasks.create!(description: "Task #{i} in checklist")
  end

  Brigade.all.each do |brigade|
    Location.all.each do |location|
      DeployedApplication.create!(application_id: app.id, brigade_id: brigade.id, location_id: location.id)
    end
  end
end

user = User.create!(email: 'ryan@wearetitans.net', password: 'foobar', skill_list: 'ruby, javascript, html')
user.brigades << Brigade.first

user = User.create!(email: 'joe@wearetitans.net', password: 'rosebud', skill_list: 'java, coffeescript, css')
user.brigades << Brigade.last


