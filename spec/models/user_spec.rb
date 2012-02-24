require 'spec_helper'

describe User do
  subject { Factory(:user) }

  it 'should be valid with valid attributes' do
    subject.should be_valid
  end

  it 'should be valid with an opt_out attribute' do
    subject.opt_out = true
    subject.should be_valid
  end

  context 'opt_out' do
    it 'should be false by default' do
      subject.opt_out.should == false
    end
  end

  describe '#location_name' do
    it 'knows the name of its location' do
      subject.location_name.should == 'Test'
    end
  end

end
