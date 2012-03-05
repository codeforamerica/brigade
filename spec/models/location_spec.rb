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
end
