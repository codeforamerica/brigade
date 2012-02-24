require 'vcr'

VCR.config do |c|
  c.stub_with        :webmock
  c.ignore_localhost = true
end
