require 'spec_helper'

describe Application do
  subject { Factory(:application) }

  it 'should be valid with valid attributes' do
    subject.should be_valid
  end

  it 'should be invalid without a name' do
    subject.name = nil

    subject.should_not be_valid
  end

end
