SOCIAL_NETWORKS = YAML::load(File.read(Rails.root.join('config/social_networks.yml')))[Rails.env]
