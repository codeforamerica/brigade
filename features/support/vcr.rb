require 'vcr'

VCR.configure do |c|
  c.hook_into        :webmock
  c.ignore_localhost = true
end
