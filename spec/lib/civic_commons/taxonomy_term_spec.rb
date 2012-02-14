require 'civic_commons/taxonomy_term'

describe CivicCommons::TaxonomyTerm do
  subject { CivicCommons::TaxonomyTerm.new('91') }

  before do
    CivicCommons::Client.any_instance.stub(:retrieve_taxonomy_term).with('91').and_return(Hashie::Mash.new({ name: "BSD" }))
  end

  describe '#get_name' do
    it "gets a Taxonomy Term's name" do
      subject.get_name.should == 'BSD'
    end
  end

end
