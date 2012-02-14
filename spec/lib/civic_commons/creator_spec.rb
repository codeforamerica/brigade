require 'civic_commons/creator'

describe CivicCommons::Creator do
  subject { CivicCommons::Creator.new('13370') }

  before do
    CivicCommons::Client.any_instance.stub(:retrieve_node).with('13370').and_return(Hashie::Mash.new({ title: "OpenPlans" }))
  end

  describe '#get_title' do
    it "gets an creator's title" do
      subject.get_title.should == 'OpenPlans'
    end
  end
end
