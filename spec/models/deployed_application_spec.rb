require 'spec_helper'

describe DeployedApplication do

  subject { FactoryGirl.create(:deployed_application) }

  it 'is valid with valid attributes' do
    subject.should be_valid
  end

  describe 'self.search' do

    context 'when there were no search parameters passed into the search method' do

      it 'returns all the deployed application' do
        all_deployed_apps = [ mock('DeployedApplication'), mock('DeployedApplication') ]

        DeployedApplication.stub(:all).and_return all_deployed_apps
        DeployedApplication.search().should == all_deployed_apps
      end

      context 'when search parameters are passed in' do
        it 'returns any deployed applications whose brigade name is like the query' do
          brigade = FactoryGirl.create(:brigade, name: 'Test Brigade')
          application = FactoryGirl.create(:application, name: 'Cool Application')
          deployed_application = Factory.create(:deployed_application, application: application, brigade: brigade)

          DeployedApplication.search('Test').should == [deployed_application]
        end
      end
    end
  end
end
