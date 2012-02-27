require 'spec_helper'

describe Picture do
  VCR.use_cassette(:s3_file_save) { subject { Factory(:picture) } }

  it 'should be valid with valid attributes' do
    subject.should be_valid
  end
end
