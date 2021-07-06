package quokka.home;

import java.util.HashMap;
import java.util.Map;

public class Device {

    public static void main(String[] args) {

        HashMap<String, String> device = new HashMap<>();
        device.put("name", "sbx-n9kv-ao");
        device.put("vendor", "cisco");
        device.put("model", "Nexus90f00 C9300v Chassis");
        device.put("os", "nxos");
        device.put("version", "9.3(3)");
        device.put("ip", "10.1.1.1");

        System.out.println("device: " + device);
        System.out.println("device name: " + device.get("name"));

        System.out.println();
        for (Map.Entry<String, String> item : device.entrySet()) {
            System.out.println(item.getKey() + ":" + item.getValue());
        }
    }
}
