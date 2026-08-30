#include <iostream>
#include <string>
#include <chrono>
#include <fstream>
#include <sstream>
#include <iomanip>

struct MQTTBrokerConfig {
    std::string broker_address;
    int port;
    std::string topic;
};

class MQTTNetworkPublisher {
private:
    std::ofstream log_file;
    MQTTBrokerConfig config;

public:
    MQTTNetworkPublisher(const std::string& log_name, MQTTBrokerConfig cfg) 
        : config(cfg) {
        log_file.open(log_name, std::ios::app);
    }
    ~MQTTNetworkPublisher() { if (log_file.is_open()) log_file.close(); }

    void publish_telemetry(const std::string& payload) {
        auto now = std::chrono::system_clock::now();
        auto in_time_t = std::chrono::system_clock::to_time_t(now);

        std::stringstream ss;
        ss << "[" << std::put_time(std::localtime(&in_time_t), "%Y-%m-%d %H:%M:%S") << "] "
           << "[MQTT_NETWORK] Target: " << config.broker_address << ":" << config.port
           << " | Topic: " << config.topic
           << " | Payload: " << payload;

        std::cout << ss.str() << std::endl;
        if (log_file.is_open()) {
            log_file << ss.str() << "\n";
            log_file.flush();
        }
    }
};

int main() {
    MQTTBrokerConfig cfg = {"127.0.0.1", 1883, "telemetry/cure_earth/data"};
    MQTTNetworkPublisher publisher("nasa_mission_telemetry.log", cfg);

    publisher.publish_telemetry("{\"status\":\"ACTIVE\", \"signal_strength\": \"-68dBm\", \"band\": \"14.5GHz\"}");
    return 0;
}
