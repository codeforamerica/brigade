CodeForAmerica::Application.routes.draw do
  mount RailsAdmin::Engine => '/admin', :as => 'rails_admin'

  devise_for :users, controllers: { registrations: 'registrations', omniauth_callbacks: 'users/omniauth_callbacks' }

  devise_scope :user do
    get '/sign-in'  => 'sessions#new',     as: :sign_in
    get '/sign-out' => 'sessions#destroy', as: :sign_out
  end

  resources :users, only: [:show, :index, :edit, :update]

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
  root :to => 'home#index'
end
