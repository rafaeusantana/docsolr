# This file is used by Rack-based servers to start the application.

require ::File.expand_path('../config/environment',  __FILE__)

if ENV['RAILS_RELATIVE_URL_ROOT']
	run Rack::URLMap.new(
		  ENV['RAILS_RELATIVE_URL_ROOT'] => Rails.application
	)
else
	run Rails.application
end
