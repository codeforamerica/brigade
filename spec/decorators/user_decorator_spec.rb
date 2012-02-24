require 'spec_helper'

describe UserDecorator do
  before { ApplicationController.new.set_current_view_context }
  subject { UserDecorator.new(Factory(:user)) }

  describe '#contact_preference_message' do

    it 'returns an opt-in message when someone has chosen to opt in' do
      subject.contact_preference_message.should == 'Does want to be contacted by other civic hackers.'
    end

    it 'returns an opt-out message when someone has chosen to opt out' do
      subject.opt_out = true
      subject.contact_preference_message.should == 'Does not want to be contacted by other civic hackers.'
    end
  end

  describe '#location_name' do

    it 'returns a location name when the user has an associated location' do
      subject.build_location(name: 'Random Location')
      subject.location_name.should == 'Random Location'
    end

    it 'returns nil when the user does not have an associated location' do
      subject.location_name.should == nil
    end
  end

  describe '#skill_set' do

    it 'returns a comma separated string with user skills' do
      subject.skill_set.should == 'ruby, foo, random'
    end

  end
end
