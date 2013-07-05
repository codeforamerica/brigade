require 'spec_helper'

describe UserDecorator do
  before { ApplicationController.new.set_current_view_context }
  subject { UserDecorator.new(FactoryGirl.create(:user)) }

  describe '#contact_preference' do

    it 'returns a clickable email address when someone has chosen to opt in' do
      subject.opt_in = true
      subject.contact_preference.should == "<a href=\"mailto:#{subject.email}\">#{subject.email}</a>"
    end

    it 'returns an opt-out message when someone has chosen to opt out' do
      subject.opt_in = false
      subject.contact_preference.should == 'Does not want to be contacted by other civic hackers.'
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
      subject.skill_set.should match /ruby/
      subject.skill_set.should match /foo/
      subject.skill_set.should match /random/
    end

  end

  describe '#gravatr_small' do

    it 'returns an img tag containing a link with the md5 generated from the user email address' do
      subject.gravatar_small.should match /#{Digest::MD5.hexdigest(subject.email)}/
    end
  end

  # These stories don't pass right now because we're throwing in the image tag
  #
  describe '#as_link' do

    it 'returns a link to the user profile page' do
      subject.as_link.should match /#{subject.user.id}/
    end
  end
end
