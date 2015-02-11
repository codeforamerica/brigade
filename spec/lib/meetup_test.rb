require 'meetup'

describe "meetup api class" do
  m = Meetup.new('http://meetup.com/betanyc/')  

  describe 'meetup initialize' do
    it 'returns meetup_id' do
      m.meetup_id.should eq('betanyc')
    end

    it 'returns meetup_id' do
      n = Meetup.new('http://meetup.com/betanyc')  
      n.meetup_id.should eq('betanyc')
    end
  end

  describe 'gets meetup description' do
    it 'return valid meetup_description' do
      m.get_description.should_not be_nil
      m.get_description['urlname'].should eq(m.meetup_id)
    end

    it 'returns nil for invalid meetup_id' do
      n = Meetup.new('http://meetup.com/1234567890')
      n.get_description.should be_nil
    end
  end

  describe 'gets meetup events' do
    it 'return valid meetup events' do
      m.get_events.should_not be_nil
      m.get_events.length.should_not eq(0)
    end

    it 'returns nil for invalid group' do
      n = Meetup.new('http://meetup.com/1234567890')
      n.get_events.should be_nil
    end
  end

  describe 'community group cfabrigade' do
    c = Meetup.new('http://www.meetup.com/cfabrigade/Open-San-Diego/')
    n = Meetup.new('http://meetup.com/cfabrigade/fakecommunity')

    it 'returns community_urlname' do
      c.community_urlname.should eq('Open-San-Diego')
    end
    it 'returns container community name' do
      c.meetup_id.should eq('cfabrigade')
    end

    describe 'gets description' do
      it 'returns nil for invalid everywhere community' do
        n.community_urlname.should eq('fakecommunity')
        n.meetup_id.should eq('cfabrigade')
        n.get_description.should be_nil
      end

      it 'returns valid everywhere community description for communities' do
        c.get_description.should_not be_nil

        c.get_description['urlname'].should eq(c.community_urlname)
        c.get_description['container']['urlname'].should eq(c.meetup_id)
      end
    end

    describe 'gets events' do
      it 'returns nil for invalid group' do
        n.get_events.should be_nil
      end

      # returns nil, no UPCOMING events for the Open-San-Diego group
      # bad test, but no groups have any events :(
      it 'returns valid events' do
        c.get_events.should_not be_nil
        c.get_events.length.should_not eq(0)
      end
    end
  end
end
