require 'open-uri'
require 'pi_piper'
include PiPiper

# Watch for the physical reset button to be pressed and start counting after 9 seconds the reset routine will run and reboot
# If the button is lifted at any point befor 9 seconds the loop will abort and nothing will be reset
after :pin => 18, :goes => :high do |pin|
    counter = 0
    term_loop = false

    begin
        sleep 1
        counter = counter + 1

        if counter == 9
            system ('sudo rm -f /etc/wpa_supplicant/wpa_supplicant.conf')
            system ('rm -f /home/pi/user_data/user_credentials')
            system ('rm -f /home/pi/tmp/*')
            system ('sudo cp -r /home/pi/static_files/interfaces.aphost /etc/network/interfaces')
            system ('sudo cp -r /home/pi/static_files/dnsmasq.conf /etc/')
            system ('sudo cp -r /home/pi/static_files/rc.local.aphost /etc/rc.local')
            system ('sudo reboot')
        end

        after :pin => 18, :goes => :low do
            term_loop = true
        end
    end until term_loop == true
end

PiPiper.wait
