require 'civic_commons/application'

describe CivicCommons::Application do
  subject { CivicCommons::Application.new('14133') }

  before do
    CivicCommons::Client.any_instance.stub(:retrieve_node).with('14133').and_return(Hashie::Mash.new(
      { field_application_sdesc:
          { "und" => [{"value" => "Shareabouts is a mapping app for crowd sourcing."}]},
        field_application_creator:
          {"und" => [{"nid" => "13370"}]},
        field_application_license:
          {"und" => [{"tid" => "89"}]},
        field_application_description:
          {"und" => [{"value" => "Shareabouts has a simple, fun interface that makes it easy to add your voice to the map: suggest a location, add a comment, support other suggestions and share locations with your friends and neighbors. Shareabouts gets out of the way, letting you focus on getting points on the map. Behind the scenes, it\u2019s a Rails app running on PostGIS spatial database, with a nice mapping front end."}]}
      }
    ))
  end

  describe '#get_short_description' do
    it "gets an application's short description" do
      subject.get_short_description.should == 'Shareabouts is a mapping app for crowd sourcing.'
    end
  end

  describe '#get_description' do
    it "gets an application's description" do
      subject.get_description.should == "Shareabouts has a simple, fun interface that makes it easy to add your voice to the map: suggest a location, add a comment, support other suggestions and share locations with your friends and neighbors. Shareabouts gets out of the way, letting you focus on getting points on the map. Behind the scenes, it\u2019s a Rails app running on PostGIS spatial database, with a nice mapping front end."
    end
  end

  describe '#get_creator_nid' do
    it "gets an application's creator nid" do
      subject.get_creator_nid.should == '13370'
    end
  end

  describe '#get_license_nid' do
    it "gets an application's license nid" do
      subject.get_license_tid == '89'
    end

    it "returns nil when there is no ids" do
      CivicCommons::Client.any_instance.stub(:retrieve_node).with('14133').and_return(Hashie::Mash.new(
        { field_application_license: [] }
      ))

      subject.get_license_tid.should == nil
    end
  end
end
