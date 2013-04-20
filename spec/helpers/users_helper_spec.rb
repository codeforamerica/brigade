require "spec_helper"

describe UsersHelper do
  describe "#display_brigades?" do
    subject { helper.display_brigades?(user) }

    let(:user)     { mock(User)    }
    let(:brigade)  { mock(Brigade) }

    before do
      user.stub(:brigades).and_return(brigades)
    end

    context "user is associated with brigades" do
      let(:brigades) { [ brigade ]   }
      it { should be_true }
    end

    context "user is not associated with any brigades" do
      let(:brigades) { [ ]   }
      it { should be_false }
    end
  end

  describe "#brigade_links" do
    let(:user)    { mock(User)    }
    let(:brigade_1) { mock(Brigade, :name => "foo", :id => 1) }
    let(:brigade_2) { mock(Brigade, :name => "bar", :id => 2) }

    subject { helper.brigade_links(user) }

    before do
      user.stub(:brigades).and_return(brigades)
    end

    let(:brigade_1_link) { "<a href=\"http://test.host/brigades/1\">foo</a>" }
    let(:brigade_2_link) { "<a href=\"http://test.host/brigades/2\">bar</a>" }

    context "user does not belong to any brigades" do
      let(:brigades) { [] }
      it { should be_nil }
    end

    context "user belongs to one brigade" do
      let(:brigades)          { [ brigade_1 ] }
      let(:expected_response) { brigade_1_link  }

      it { should eql(expected_response) }
    end

    context "user belongs to multiple brigades" do
      context "containing duplicates" do
        let(:brigades)  { [ brigade_1, brigade_1 ] }
        let(:expected_response) { "#{brigade_1_link}" }

        it { should eql(expected_response) }
      end

      context "containing no duplicates" do
        let(:brigades)  { [ brigade_1, brigade_2 ] }
        let(:expected_response) { "#{brigade_1_link}, #{brigade_2_link}" }

        it { should eql(expected_response) }
      end
    end

  end
end
