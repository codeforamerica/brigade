class GeolocateAllLocations < ActiveRecord::Migration
  def up
    Location.all.each(&:geocode)
  end

  def down
  end
end
