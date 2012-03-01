require 'spec_helper'

describe Challenge do
  subject { Factory(:challenge) }

  it 'should be valid with valid attributes' do
    subject.should be_valid
  end

  it 'is not valid without a purpose' do
    subject.purpose = nil
    subject.should_not be_valid
  end

  it 'is not valid without an orginization name' do
    subject.organization_name = nil
    subject.should_not be_valid
  end

  it 'is not valid without a description' do
    subject.description = nil
    subject.should_not be_valid
  end

  it 'is not valid without a location' do
    subject.location = nil
    subject.should_not be_valid
  end

  it 'is not valid with an empty technology platform list' do
    subject.technology_platform_list = ''
    subject.should_not be_valid
  end

  it 'is not valid without a success description' do
    subject.success_description = nil
    subject.should_not be_valid
  end

  context '#public_visibility' do

    it 'is false by default' do
      subject.public_visibility.should be_false
    end
  end

  context '#status' do

    it 'is submitted by default' do
      subject.status.should == 'submitted'
    end
  end

end
