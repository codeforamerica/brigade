require 'spec_helper'

describe Brigade do
  subject { FactoryGirl.create(:brigade) }

  it 'should be valid with valid attributes' do
    subject.should be_valid
  end

  it 'should not be valid without a name' do
    subject.name = nil
    subject.should_not be_valid
  end

  it 'should not be valid without a point of contact address' do
    subject.point_of_contact_address = nil
    subject.should_not be_valid
  end

  it 'should not be valid when another brigade exists with the same name' do
    other = FactoryGirl.build(:brigade)
    other.name = subject.name
    other.should_not be_valid
  end
end
