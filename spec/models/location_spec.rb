require 'spec_helper'

describe Location do

  it 'should have unique names' do
    location = Location.create!(name: 'location')
    duplicate_location = Location.new(name: 'location')

    duplicate_location.should_not be_valid
  end

  it 'should not allow blank names' do
    location = Location.create(name: "")

    location.should_not be_valid
  end

  it 'geolocates the name' do
    norfolk = Location.create(name: 'Norfolk, VA')
    VCR.use_cassette 'geocode' do
      norfolk.geocode
    end
    norfolk.longitude.should_not be_blank
    norfolk.latitude.should_not be_blank
  end


  describe '#applications_not_deployed' do

    before do
      @location = Location.create name: 'Norfolk, VA'
      @app_not_deployed = Factory :application
      @app_deployed = Factory :application
      @deploy = Factory :deployed_application, application: @app_deployed, location: @location
    end

    it 'returns a list of applications that have yet to be deployed at the current location' do
      @location.applications_not_deployed.should include @app_not_deployed
    end

    it 'does not return applications that have been deployed at the current location' do
      @location.applications_not_deployed.should_not include @app_deployed
    end
  end
end
