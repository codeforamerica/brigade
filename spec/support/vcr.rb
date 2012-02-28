require 'vcr'

VCR.config do |c|
  c.cassette_library_dir     = 'spec/cassettes'
  c.ignore_localhost         = true
  c.stub_with                :webmock
end

RSpec.configure do |c|
  c.extend VCR::RSpec::Macros
end
