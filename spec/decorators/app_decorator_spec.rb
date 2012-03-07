require 'spec_helper'

describe AppDecorator do
  before { ApplicationController.new.set_current_view_context }

  describe '#participating_brigade_links' do

    it 'should return a url formatted string containging brigade names and their links when the application has deployed apps' do
      application = FactoryGirl.build(:application)
      first_brigade = FactoryGirl.create(:brigade)
      second_brigade = FactoryGirl.create(:brigade)

      application.stub(:participating_brigades).and_return([first_brigade, second_brigade])
      subject = AppDecorator.new(application)
      subject.participating_brigade_links.should match /#{first_brigade.name}/ #, second_brigade.name]
    end

    it 'should return nil when the application does not have deployed apps' do
      application = FactoryGirl.build(:application)
      subject = AppDecorator.new(application)
      subject.participating_brigade_links.should be_nil
    end
  end

  describe '#picture_gallary' do

    it 'returns nil when there are no pictures' do
      application = AppDecorator.new(FactoryGirl.build(:application))
      application.picture_gallary.should be_nil
    end

    it 'returns raw html for a picture gallary when there is more than one picture' do
      VCR.use_cassette(:s3_file_save) { @app_with_pics = FactoryGirl.create(:application_with_four_pictures) }
      application_with_pictures = AppDecorator.new(@app_with_pics)
      application_with_pictures.picture_gallary.should match /ul class="thumbnails"/
    end
  end

  describe '#number_of_deploys' do

    it 'returns the number of times the application has been deployed' do
      application = AppDecorator.new(FactoryGirl.build(:application))
      application.number_of_deploys.should == application.deployed_applications.count
    end

  end


  describe '#repository_sparkline_label' do

    it 'will not return a label of there is no repository information' do
      application = AppDecorator.new(FactoryGirl.build(:application))
      application.repository_sparkline_label.should == nil
    end

  end
end
