[ '14133', '14387', '13422', '13685', '14012', '14110', '13489', '13465', '13744', '13808' ].each { |node_id| Application.create!(nid: node_id) }

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
