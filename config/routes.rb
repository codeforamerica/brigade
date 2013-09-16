CodeForAmerica::Application.routes.draw do

  mount RailsAdmin::Engine => '/admin', :as => 'rails_admin'

  devise_for :users, :path => "members", controllers: { registrations: 'registrations', omniauth_callbacks: 'users/omniauth_callbacks' }

  devise_scope :user do
    get '/sign-in'  => 'sessions#new',     as: :sign_in
    get '/sign-out' => 'sessions#destroy', as: :sign_out
    get '/organize'  => 'registrations#new_organizer',     as: :new_organizer
  end

  resources :users, :path => 'members', only: [:show, :index, :edit, :update, :destroy]

  # Redirects after switching users to members
  match "/users/sign_up"        => redirect("/members/sign_up")
  match "/users/sign_in"        => redirect("/members/sign_in")
  match "/users/sign_out"       => redirect("/members/sign_out")
  match "/users/password/new"   => redirect("/members/password/new")
  match "/users/edit"           => redirect("/members/edit")
  match "/users"                => redirect("/members")
  match "/users/:id/edit"       => redirect("/members/:id/edit")
  match "/users/:id"            => redirect("/members/:id")

  # Move legacy events and campaigns to /events & /campaigns
  # TODO: wildcards & regex
  match "/openimpact"                     => 'high_voltage/pages#show', :id => "/campaigns/openimpact"
  match "/pages/openimpact"               => 'high_voltage/pages#show', :id => "/campaigns/openimpact"
  match "/openimpact-citizen"             => 'high_voltage/pages#show', :id => "/campaigns/openimpact-citizen"
  match "/pages/openimpact-citizen"       => 'high_voltage/pages#show', :id => "/campaigns/openimpact-citizen"
  match "/openimpact-government"          => 'high_voltage/pages#show', :id => "/campaigns/openimpact-government"
  match "/pages/openimpact-government"    => 'high_voltage/pages#show', :id => "/campaigns/openimpact-government"
  match "/race-for-reuse"                 => 'high_voltage/pages#show', :id => "/campaigns/race-for-reuse"
  match "/pages/race-for-reuse"           => 'high_voltage/pages#show', :id => "/campaigns/race-for-reuse"
  match "/codeacross"                     => 'high_voltage/pages#show', :id => "/events/codeacross"
  match "/pages/codeacross"               => 'high_voltage/pages#show', :id => "/events/codeacross"
  match "/national-day-of-civic-hacking"  => 'high_voltage/pages#show', :id => "/events/national-day-of-civic-hacking"
  match "/hackforchange"                  => 'high_voltage/pages#show', :id => "/events/national-day-of-civic-hacking"
  match "/campaigns"                      => 'high_voltage/pages#show', :id => "/campaigns"
  match "/civic-coding"                   => 'high_voltage/pages#show', :id => "/campaigns/civic-coding"
  match "/survey"                         => 'high_voltage/pages#show', :id => "/newsletters"


  resources :applications, only: [:index, :show] do
    resources :deployed_applications, only: [:new, :create], controller: 'applications/deployed_applications'
  end

  resources :brigades do
    collection do
      post :find
      get :locations
    end

    member do
      get :join
      get :leave
      get :application_locations
    end

    resources :deployed_applications, only: [:new, :create, :index], controller: 'brigades/deployed_applications'
  end

  resources :locations do
    collection do
      post :find
    end

    resources :deployed_applications, only: [:new, :create, :index], controller: 'locations/deployed_applications'
  end

  resources :deployed_applications, only: [:index, :new, :create, :show, :edit, :update]
  resources :challenges, only: [:new, :create, :index]
  resources :home
  root :to => 'home#index'

  match "/pages/*id" => 'pages#show', :as => :page, :format => false

  match '/about'          => 'high_voltage/pages#show', :id => 'about'
  match '/tools'          => 'high_voltage/pages#show', :id => 'tools'
  match '/events'         => 'high_voltage/pages#show', :id => 'events'
  match '/activities'     => 'high_voltage/pages#show', :id => 'activities'
  match '/connect'        => 'high_voltage/pages#show', :id => 'connect'
  match '/forums'         => 'high_voltage/pages#show', :id => 'forums'
  match "/captain"        => 'high_voltage/pages#show', :id => 'captain'
  match "/opendata"       => 'high_voltage/pages#show', :id => 'opendata'
  match "/apps"           => 'high_voltage/pages#show', :id => 'apps'
  match "/ogi"            => 'high_voltage/pages#show', :id => 'ogi'
  match "/opengovernment" => 'high_voltage/pages#show', :id => 'opengovernment'
  match "/opensource"     => 'high_voltage/pages#show', :id => 'opensource'

  match '/404' => 'application#render_404_error'
  match '/500' => redirect("/error")
end
