class Main < ActiveRecord::Base

	def self.scan_wifi_networks
    ap_list = %x{sudo iwlist scan}.split('Cell')
    ap_array = Array.new

    ap_list.each{|ap_grouping|
        ap_hash = Hash.new
        encryption_found = false
        ssid = ''
        encryption_type = ''

        ap_grouping.split("\n").each{|line|
          if line.include?('ESSID')
              ssid = line[27..-2]
          end

          if line.include?('WEP')
              encryption_found = true
              encryption_type = 'wep'
          elsif line.include?('WPA Version 1')
              encryption_found = true
              encryption_type = 'WPA'
          elsif line.include?('IEEE 802.11i/WPA2')
              encryption_found = true
              encryption_type = 'WPA2'
          end
        }

        if encryption_found == false
          encryption_type = 'open'
        end

        unless ssid == ''
          ap_hash = {:ssid => ssid, :encryption_type => encryption_type}
          ap_array << ap_hash
        end
    }

    ap_array
	end

	def self.get_current_config_values
    current_values = Array.new

    if File.exist?('/etc/wpa_supplicant/wpa_supplicant.conf')
      wpa_supplicant_file = File.open('/etc/wpa_supplicant/wpa_supplicant.conf', 'r')

      wpa_supplicant_file.each{|line|
        if line.include?('ssid=')
            current_values << line.split('=')[1].chomp[1..-2]
        elsif line.include?('psk=')
            current_values << line.split('=')[1].chomp[1..-2]
        end
      }

      wpa_supplicant_file.close
    else
      current_values << ''
    end

    if File.exist?('/home/pi/user_data/user_credentials')
      user_credential_file = File.open('/home/pi/user_data/user_credentials', 'r')

      user_credential_file.each{|line|
        if line.include?('username=')
            current_values << line.split('=')[1].chomp
        elsif line.include?('password=')
            current_values << line.split('=')[1].chomp
        end
      }

      user_credential_file.close
    else
        current_values << ''
    end

    current_values
	end

  def self.create_wpa_supplicant(user_ssid, encryption_type, user_wifi_key)
		temp_conf_file = File.new('/home/pi/tmp/wpa_supplicant.conf.tmp', 'w')

    if encryption_type == 'WPA2'
      temp_conf_file.puts 'ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev'
      temp_conf_file.puts 'update_config=1'
      temp_conf_file.puts
      temp_conf_file.puts 'network={'
      temp_conf_file.puts '	ssid="' + user_ssid + '"'
      temp_conf_file.puts '	psk="' + user_wifi_key + '"'
      temp_conf_file.puts '	proto=WPA2'
      temp_conf_file.puts '	key_mgmt=WPA-PSK'
      temp_conf_file.puts '}'
    elsif encryption_type == 'WPA'
      temp_conf_file.puts 'ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev'
      temp_conf_file.puts 'update_config=1'
      temp_conf_file.puts
      temp_conf_file.puts 'network={'
      temp_conf_file.puts '	ssid="' + user_ssid + '"'
      temp_conf_file.puts '	proto=WPA RSN'
      temp_conf_file.puts '	key_mgmt=WPA-PSK'
      temp_conf_file.puts '	pairwise=CCMP PSK'
      temp_conf_file.puts '	group=CCMP TKIP'
      temp_conf_file.puts '	psk="' + user_wifi_key + '"'
      temp_conf_file.puts '}'
    end

		temp_conf_file.close

		system('sudo cp -r /home/pi/tmp/wpa_supplicant.conf.tmp /etc/wpa_supplicant/wpa_supplicant.conf')
		system('rm /home/pi/tmp/wpa_supplicant.conf.tmp')
	end

  def self.create_user_credential_file(username, password)
    user_credential_file = File.new('/home/pi/tmp/user_credentials.tmp', 'w')

    user_credential_file.puts 'username=' + username
    user_credential_file.puts 'password=' + password

    user_credential_file.close

    system('cp -r /home/pi/tmp/user_credentials.tmp /home/pi/user_data/user_credentials')
    system('rm /home/pi/tmp/user_credentials.tmp')
  end

  def self.set_ap_client_mode
    system ('sudo cp -r /home/pi/static_files/interfaces.apclient /etc/network/interfaces')
    system ('sudo cp -r /home/pi/static_files/rc.local.apclient /etc/rc.local')
    system ('sudo rm -f /etc/dnsmasq.conf')
    system ('sudo reboot')
  end

  def self.reset_all
    system ('sudo rm -f /etc/wpa_supplicant/wpa_supplicant.conf')
    system ('rm -f /home/pi/user_data/user_credentials')
    system ('rm -f /home/pi/tmp/*')
    system ('sudo cp -r /home/pi/static_files/interfaces.aphost /etc/network/interfaces')
    system ('sudo cp -r /home/pi/static_files/dnsmasq.conf /etc/')
    system ('sudo cp -r /home/pi/static_files/rc.local.aphost /etc/rc.local')
    system ('sudo reboot')
  end

end
