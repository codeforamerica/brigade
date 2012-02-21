require 'spec_helper'

describe User do
  subject { Factory(:user) }

  describe '#location_name' do
    it 'knows the name of its location' do
      subject.location_name.should == 'Test'
    end
  end
end
