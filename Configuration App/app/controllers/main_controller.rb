class MainController < ApplicationController

    def index
      @current_values = Main.get_current_config_values
      @wifi_ap_hash = Main.scan_wifi_networks
    end

    def save_credentials
      ssid = params[:ap_info].split('+')[0]
      encryption_type = params[:ap_info].split('+')[1]

      unless ssid.nil? or params[:wifi_key] == ""
        Main.create_wpa_supplicant(ssid, encryption_type, params[:wifi_key])
      end

      if File.exist?('/etc/wpa_supplicant/wpa_supplicant.conf') and File.exist?('/home/pi/user_data/user_credentials')
        Main.set_ap_client_mode
      end
    end

    def reset_all
      Main.reset_all
    end

end
