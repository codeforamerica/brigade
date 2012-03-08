# Production Data
app_data =[ {id: '14133', git: 'https://github.com/openplans/shareabouts'}, {id: '14387', git: 'https://github.com/codeforamerica/public_art_finder'},
            {id: '13422'}, {id: '13685', git: 'https://github.com/open-city/Look-at-Cook'}, {id: '14012'}, {id: '14110'}, {id: '13489'},
            {id: '13465', git: 'https://github.com/codeforamerica/adopt-a-hydrant'}, {id: '13744'}, {id: '13808', git: 'https://github.com/derekeder/Chicago-Buildings'} ]

app_data.each do |app|
  Application.create!(nid: app[:id], repository_url: app[:git])
end

# Test and Dev Data
[ 'Titans Brigade', 'Code For America Brigade', 'Thoughbot Brigade'].each { |brigade_name| Brigade.create!(name: brigade_name, point_of_contact_address: "testman@example.com") }

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

user = User.create!(email: 'ryan@wearetitans.net', password: 'foobar', name: 'Ryan Castillo', skill_list: 'ruby, javascript, html')
user.brigades << Brigade.first

Location.all.each(&:geocode)
