require 'spec_helper'

describe UpdateApplicationsFromCivicCommons do
  Factory(:application)

  it 'updates application attributes based on data from civic commons' do
    app = Application.last
    app.short_description.should be_nil
    app.creator.should be_nil
    app.license.should be_nil
    app.civic_commons_description.should be_nil

    VCR.use_cassette(:civic_commons_request, record: :new_episodes) { UpdateApplicationsFromCivicCommons.perform }
    app = Application.last

    app.short_description.should_not be_nil
    app.creator.should_not be_nil
    app.license.should_not be_nil
    app.civic_commons_description.should_not be_nil
  end

  it "keeps an applications's license at nil if civic commons does not have the data it is looking for" do
    app = FactoryGirl.create(:application, nid: '14133')
    app.license.should be_nil

    VCR.use_cassette(:civic_commons_request, record: :new_episodes) { UpdateApplicationsFromCivicCommons.perform }
    app = Application.find_by_nid('14133')
    app.license.should be_nil
  end

  it "keeps an application's creator nil if civic commons does not have the creator" do
    app = FactoryGirl.create(:application, nid: '13422')
    app.creator.should be_nil

    VCR.use_cassette(:civic_commons_request, record: :new_episodes) { UpdateApplicationsFromCivicCommons.perform }
    app = Application.find_by_nid('13422')
    app.creator.should be_nil

  end
end
