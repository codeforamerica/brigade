# RailsAdmin config file. Generated on February 19, 2012 21:44
# See github.com/sferik/rails_admin for more informations

unless Rails.env == 'test'
  RailsAdmin.config do |config|

    # If your default_local is different from :en, uncomment the following 2 lines and set your default locale here:
    # require 'i18n'
    # I18n.default_locale = :de

    config.current_user_method { current_user } # auto-generated

    # If you want to track changes on your models:
    # config.audit_with :history, User

    # Or with a PaperTrail: (you need to install it first)
    # config.audit_with :paper_trail, User

    # Set the admin name here (optional second array element will appear in a beautiful RailsAdmin red ©)
    config.main_app_name = ['Code For America', 'Admin']
    # or for a dynamic name:
    # config.main_app_name = Proc.new { |controller| [Rails.application.engine_name.titleize, controller.params['action'].titleize] }

    config.authorize_with do
      redirect_to main_app.root_path unless current_user.try(:admin?)
    end

    #  ==> Global show view settings
    # Display empty fields in show views
    # config.compact_show_view = false

    #  ==> Global list view settings
    # Number of default rows per-page:
    # config.default_items_per_page = 20

    #  ==> Included models
    # Add all excluded models here:
    # config.excluded_models = [Application, Brigade, DeployedApplication, Task, User]

    # Add models here if you want to go 'whitelist mode':
    # config.included_models = [Application, Brigade, DeployedApplication, Task, User]

    # Application wide tried label methods for models' instances
    # config.label_methods << :description # Default is [:name, :title]

    #  ==> Global models configuration
    # config.models do
    #   # Configuration here will affect all included models in all scopes, handle with care!
    #
    #   list do
    #     # Configuration here will affect all included models in list sections (same for show, export, edit, update, create)
    #
    #     fields_of_type :date do
    #       # Configuration here will affect all date fields, in the list section, for all included models. See README for a comprehensive type list.
    #     end
    #   end
    # end
    #
    #  ==> Model specific configuration
    # Keep in mind that *all* configuration blocks are optional.
    # RailsAdmin will try his best to provide the best defaults for each section, for each field.
    # Try to override as few things as possible, in the most generic way. Try to avoid setting labels for models and attributes, use ActiveRecord I18n API instead.
    # Less code is better code!
    # config.model MyModel do
    #   # Cross-section field configuration
    #   object_label_method :name     # Name of the method called for pretty printing an *instance* of ModelName
    #   label 'My model'              # Name of ModelName (smartly defaults to ActiveRecord's I18n API)
    #   label_plural 'My models'      # Same, plural
    #   weight -1                     # Navigation priority. Bigger is higher.
    #   parent OtherModel             # Set parent model for navigation. MyModel will be nested below. OtherModel will be on first position of the dropdown
    #   navigation_label              # Sets dropdown entry's name in navigation. Only for parents!
    #   # Section specific configuration:
    #   list do
    #     filters [:id, :name]  # Array of field names which filters should be shown by default in the table header
    #     items_per_page 100    # Override default_items_per_page
    #     sort_by :id           # Sort column (default is primary key)
    #     sort_reverse true     # Sort direction (default is true for primary key, last created first)
    #     # Here goes the fields configuration for the list view
    #   end
    # end

    # Your model's configuration, to help you get started:

    # All fields marked as 'hidden' won't be shown anywhere in the rails_admin unless you mark them as visible. (visible(true))

    config.model Application do
      list do
        field :name
        field :nid do
          label "Civic Commons Node ID"
        end
      end

      edit do
        field :nid do
          label "Civic Commons Node ID"
        end
        field :description
        field :video_embed_code
        field :repository_url
        field :irc_channel
        field :twitter_hashtag
        field :pictures
        field :tasks
      end

      # Hiding these attributes by default since name, creator, short_description
      # license, and civic_commons_description are managed by the job that retrieves
      # data from civic commons
      #     configure :id, :integer 
      #     configure :creator, :string 
      #     configure :short_description, :string 
      #     configure :license, :string 
      #     configure :civic_commons_description, :text   #   # Sections:
      #     configure :deployed_applications, :has_many_association 
      #     configure :participating_brigades, :has_many_association   #   # Found columns:
    end

    config.model Challenge do
      edit do
        field :description
        field :purpose
        field :organization_name
        field :location
        field :success_description
        field :mission
        field :audience
        field :user_story
        field :status do
          partial 'status_dropdown'
          help ''
        end
        field :public_visibility
        field :admin_note
      end
    end
    # My attempt to include managing tags in rails admin
    # If you create a Tag model that inerits the
    # ActsAsTaggableOn::Tag then it'll work but
    # rails_admin does not seem to play nicely with the
    # namespace
    #config.model ActsAsTaggableOn::Tag do
    #  label 'Tag'
    #  label_plural 'Tags'

    #  list do
    #    field :name
    #  end

    #  edit do
    #    field :name
    #  end
    #end

    # config.model Brigade do
    #   # Found associations:
    #     configure :deployed_applications, :has_many_association   #   # Found columns:
    #     configure :id, :integer 
    #     configure :deployed_application_id, :integer 
    #     configure :name, :string 
    #     configure :created_at, :datetime 
    #     configure :updated_at, :datetime 
    #     configure :group_url, :string   #   # Sections:
    #   list do; end
    #   export do; end
    #   show do; end
    #   edit do; end
    #   create do; end
    #   update do; end
    # end
    # config.model DeployedApplication do
    #   # Found associations:
    #     configure :application, :belongs_to_association 
    #     configure :brigade, :has_one_association   #   # Found columns:
    #     configure :id, :integer 
    #     configure :application_id, :integer         # Hidden 
    #     configure :created_at, :datetime 
    #     configure :updated_at, :datetime   #   # Sections:
    #   list do; end
    #   export do; end
    #   show do; end
    #   edit do; end
    #   create do; end
    #   update do; end
    # end
    # config.model Task do
    #   # Found associations:
    #     configure :application, :belongs_to_association   #   # Found columns:
    #     configure :id, :integer 
    #     configure :description, :text 
    #     configure :application_id, :integer         # Hidden   #   # Sections:
    #   list do; end
    #   export do; end
    #   show do; end
    #   edit do; end
    #   create do; end
    #   update do; end
    # end

    # config.model User do
    #  edit do
    #    field :skills
    #  end
    #   # Found associations:
    #     configure :taggings, :has_many_association         # Hidden 
    #     configure :base_tags, :has_many_association         # Hidden 
    #     configure :skills, :has_many_association         # Hidden 
    #     configure :skill_taggings, :has_many_association         # Hidden   #   # Found columns:
    #   # Found columns:
    #     configure :id, :integer 
    #     configure :email, :string 
    #     configure :password, :password         # Hidden 
    #     configure :password_confirmation, :password         # Hidden 
    #     configure :reset_password_token, :string         # Hidden 
    #     configure :reset_password_sent_at, :datetime 
    #     configure :remember_created_at, :datetime 
    #     configure :sign_in_count, :integer 
    #     configure :current_sign_in_at, :datetime 
    #     configure :last_sign_in_at, :datetime 
    #     configure :current_sign_in_ip, :string 
    #     configure :last_sign_in_ip, :string 
    #     configure :created_at, :datetime 
    #     configure :updated_at, :datetime   #   # Sections:
    #   list do; end
    #   export do; end
    #   show do; end
    #   edit do; end
    #   create do; end
    #   update do; end
    # end
  end
end
