require 'spec_helper'

describe Task do
  subject { Factory(:task) }

  it 'should be valid with valid attributes' do
    subject.should be_valid
  end

  it 'should not be valid without a description' do
    subject.description = nil
    subject.should_not be_valid
  end

end
