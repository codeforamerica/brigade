require 'meetup'

describe "meetup api class" do
  m = Meetup.new('http://meetup.com/betanyc/')  

  describe 'meetup initialize' do
    it 'returns meetup_id' do
      m.meetup_id.should eq('betanyc')
    end

    it 'returns meetup_id' do
      n = Meetup.new('http://meetup.com/betanyc/asdfljkha/sd')  
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

end
