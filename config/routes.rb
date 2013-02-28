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

  match "/activities"     => redirect("/pages/activities")
  match "/connect"        => redirect("/pages/connect")
  match "/events"         => redirect("/pages/events")
  match "/tools"          => redirect("/pages/tools")

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

  match '/about' => 'high_voltage/pages#show', :id => 'about'

  match '/404' => 'application#render_404_error'
  match '/500' => redirect("/error")
end
