require 'vcr'

VCR.configure do |c|
  c.cassette_library_dir     = 'spec/cassettes'
  c.ignore_localhost         = true
  c.hook_into                :webmock
end

RSpec.configure do |c|
  c.extend VCR::RSpec::Macros
end
