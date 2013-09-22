Rack::Attack.blacklist('block 46.161.41.7') do |req|
  # Request are blocked if the return value is truthy
  '46.161.41.7' == req.ip
end

Rack::Attack.blacklisted_response = lambda do |env|
  # Using 503 because it may make attacker think that they have successfully
  # DOSed the site. Rack::Attack returns 401 for blacklists by default
  [ 503, {}, ['Blocked']]
end
