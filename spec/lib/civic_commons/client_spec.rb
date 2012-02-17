require 'civic_commons/client'

describe CivicCommons::Client do

  it 'retrieves a node from the civic commons api' do
    VCR.use_cassette(:civic_commons_node_request) { subject.retrieve_node('14133').should_not be_nil }
  end

  it 'retrieves a taxonomy_term from the civic commons api' do
    VCR.use_cassette(:civic_commons_term_request) { subject.retrieve_taxonomy_term('91').should_not be_nil }
  end

end
