class PagesController < HighVoltage::PagesController
  def show
    @user ||= User.new

    KM.record('Connect')                if params[:id] == 'connect'
    KM.record('Deploy Apps')            if params[:id] == 'apps'
    KM.record('Hack Your City')         if params[:id] == 'activities'
    KM.record('Find Events')            if params[:id] == 'events'
    KM.record('Captain Brigade')        if params[:id] == 'captain'
    KM.record('Open Civic Data')        if params[:id] == 'opendata'
    KM.record('Advocate')               if params[:id] == 'ogi'
    KM.record('Commit Open Source')     if params[:id] == 'opensource'

    super
  end
end
