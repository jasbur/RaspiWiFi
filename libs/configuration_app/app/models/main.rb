class Main < ActiveRecord::Base

	def self.scan_wifi_networks
    ap_list = %x{iwlist scan}.split('Cell')
    ap_array = Array.new

    ap_list.each{|ap_grouping|
      ssid = ''

      ap_grouping.split("\n").each{|line|
        if line.include?('ESSID')
            ssid = line[27..-2]
        end
      }

      unless ssid == ''
        ap_array << ssid
      end
    }

    ap_array
	end

  def self.create_wpa_supplicant(ssid, wifi_key)
		temp_conf_file = File.new('../tmp/wpa_supplicant.conf.tmp', 'w')

		temp_conf_file.puts 'ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev'
		temp_conf_file.puts 'update_config=1'
		temp_conf_file.puts
		temp_conf_file.puts 'network={'
		temp_conf_file.puts '	ssid="' + ssid + '"'

		if wifi_key == 'open'
			temp_conf_file.puts '	key_mgmt=NONE'
		else
			temp_conf_file.puts '	psk="' + wifi_key + '"'
		end

		temp_conf_file.puts '}'

		temp_conf_file.close

		system('cp ../tmp/wpa_supplicant.conf.tmp /etc/wpa_supplicant/wpa_supplicant.conf')
		system('rm ../tmp/wpa_supplicant.conf.tmp')
	end

  def self.set_ap_client_mode
    system ('rm /etc/cron.raspiwifi/aphost_bootstrapper')
    system ('cp /usr/lib/raspiwifi/reset_device/static_files/apclient_bootstrapper /etc/cron.raspiwifi/')
		system ('chmod +x /etc/cron.raspiwifi/apclient_bootstrapper')
    system ('mv /etc/dnsmasq.conf.original /etc/dnsmasq.conf')
    system ('mv /etc/dhcpcd.conf.original /etc/dhcpcd.conf')
    system ('cp /usr/lib/raspiwifi/reset_device/static_files/isc-dhcp-server.apclient /etc/default/isc-dhcp-server')
    system ('reboot')
  end

end
