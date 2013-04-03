CodeForAmerica::Application.routes.draw do

  mount RailsAdmin::Engine => '/admin', :as => 'rails_admin'

  devise_for :users, :path => "members", controllers: { registrations: 'registrations', omniauth_callbacks: 'users/omniauth_callbacks' }

  devise_scope :user do
    get '/sign-in'  => 'sessions#new',     as: :sign_in
    get '/sign-out' => 'sessions#destroy', as: :sign_out
  end

  resources :users, :path => 'members', only: [:show, :index, :edit, :update]

  # Redirects after switching users to members
  match "/users/sign_up"        => redirect("/members/sign_up")
  match "/users/sign_in"        => redirect("/members/sign_in")
  match "/users/password/new"   => redirect("/members/password/new")
  match "/users/edit"           => redirect("/members/edit")
  match "/users"                => redirect("/members")
  match "/users/:id/edit"       => redirect("/members/:id/edit")
  match "/users/:id"            => redirect("/members/:id")

  match "/captain"              => redirect("/pages/captain")
  match "/opendata"             => redirect("/pages/opendata")
  match "/apps"                 => redirect("/pages/apps")
  match "/ogi"                  => redirect("/pages/ogi")
  match "/opengovernment"       => redirect("/pages/ogi")
  match "/opensource"           => redirect("/pages/opensource")
  
  # Move legacy events and campaigns to /events & /campaigns
  # TODO: wildcards & regex
  match "/openimpact"                     => redirect("/pages/campaigns/openimpact")
  match "/pages/openimpact"               => redirect("/pages/campaigns/openimpact")
  match "/openimpact-citizen"             => redirect("/pages/campaigns/openimpact-citizen")
  match "/pages/openimpact-citizen"       => redirect("/pages/campaigns/openimpact-citizen")
  match "/openimpact-government"          => redirect("/pages/campaigns/openimpact-government")
  match "/pages/openimpact-government"    => redirect("/pages/campaigns/openimpact-government")
  match "/race-for-reuse"                 => redirect("/pages/campaigns/race-for-reuse")
  match "/pages/race-for-reuse"           => redirect("/pages/campaigns/race-for-reuse")
  match "/codeacross"                     => redirect("/pages/events/codeacross")
  match "/pages/codeacross"               => redirect("/pages/events/codeacross")
  match "/national-day-of-civic-hacking"  => redirect("/pages/events/national-day-of-civic-hacking")
  match "/ndoch"                          => redirect("/pages/events/national-day-of-civic-hacking")

  
  resources :applications, only: [:index, :show] do
    resources :deployed_applications, only: [:new, :create], controller: 'applications/deployed_applications'
  end

  resources :brigades do
    collection do
      post :find
    end

    member do
      get :join
      get :leave
    end

    resources :deployed_applications, only: [:new, :create, :index], controller: 'brigades/deployed_applications'
  end

  resources :locations do
    collection do
      post :find
    end

    resources :deployed_applications, only: [:new, :create, :index], controller: 'locations/deployed_applications'
  end

  resources :deployed_applications, only: [:index, :new, :create, :show]
  resources :challenges, only: [:new, :create, :index]
  resources :home
  root :to => 'home#index'

  match "/pages/*id" => 'pages#show', :as => :page, :format => false

  match '/about'        => 'high_voltage/pages#show', :id => 'about'
  match '/tools'        => 'high_voltage/pages#show', :id => 'tools'
  match '/events'       => 'high_voltage/pages#show', :id => 'events'
  match '/activities'   => 'high_voltage/pages#show', :id => 'activities'
  match '/connect'      => 'high_voltage/pages#show', :id => 'connect'

  match '/404' => 'application#render_404_error'
  match '/500' => redirect("/error")
end
