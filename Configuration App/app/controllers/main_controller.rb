class MainController < ApplicationController

    def index
      @current_values = Main.get_current_config_values
      @wifi_ap_array = Main.scan_wifi_networks
    end

    def save_credentials
      ssid = params[:ssid]

      if params[:wifi_key] == ""
        Main.create_wpa_supplicant(ssid, "open")
      else
        Main.create_wpa_supplicant(ssid, params[:wifi_key])
      end

      if File.exist?('/etc/wpa_supplicant/wpa_supplicant.conf')
        Main.set_ap_client_mode
      end
    end

end
