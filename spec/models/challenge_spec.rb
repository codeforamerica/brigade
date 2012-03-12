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

  context '#i_statement' do

    it "is a combination of a challenge's location and purpose" do
      subject.i_statement.should == "I challenge #{subject.location.name} to #{subject.purpose}."
    end
  end

  context "#publicly_visible_challenges" do

    it "is a list of challenges that are publicly visible" do
      public_challenge_1 = FactoryGirl.create(:challenge, public_visibility: true)
      public_challenge_2 = FactoryGirl.create(:challenge, public_visibility: true)
      private_challenge = FactoryGirl.create(:challenge, public_visibility: false)

      Challenge.publicly_visible_challenges.size.should == 2
    end
  end
end
