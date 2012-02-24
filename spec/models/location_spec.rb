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
end
