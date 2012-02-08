require 'spec_helper'

describe AppDecorator do
  before { ApplicationController.new.set_current_view_context }

  describe 'brigades' do

    it 'should return a list of brigade names when the application has deployed apps' do
      application = FactoryGirl.build(:application)
      first_brigade = FactoryGirl.build(:brigade)
      second_brigade = FactoryGirl.build(:brigade)

      application.stub(:participating_brigades).and_return([first_brigade, second_brigade])
      subject = AppDecorator.new(application)
      subject.participating_brigade_links.should match /#{first_brigade.name}/ #, second_brigade.name]
    end

    it 'should return nil when the application does not have deployed apps' do
      application = FactoryGirl.build(:application)
      subject = AppDecorator.new(application)
      subject.participating_brigade_links.should == ''
    end
  end
end
