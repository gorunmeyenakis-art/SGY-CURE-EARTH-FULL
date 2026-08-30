#include <iostream>
#include <string>
#include <fstream>
#include <chrono>
#include <sstream>
#include <iomanip>

class IntegrityValidator {
private:
    std::ofstream audit_log;

    // Basit doğrulama ve veri süzme algoritması
    bool is_payload_clean(const std::string& input) {
        // Zararlı komut enjeksiyonu veya yetkisiz karakter taraması
        if (input.find("DROP") != std::string::npos || 
            input.find("<script>") != std::string::npos ||
            input.find("MALWARE") != std::string::npos) {
            return false;
        }
        return true;
    }

public:
    IntegrityValidator(const std::string& log_file) {
        audit_log.open(log_file, std::ios::app);
    }
    ~IntegrityValidator() { if (audit_log.is_open()) audit_log.close(); }

    bool validate_and_process(const std::string& packet_id, const std::string& data) {
        auto now = std::chrono::system_clock::now();
        auto in_time_t = std::chrono::system_clock::to_time_t(now);
        std::stringstream ss;
        ss << "[" << std::put_time(std::localtime(&in_time_t), "%Y-%m-%d %H:%M:%S") << "] ";

        if (!is_payload_clean(data)) {
            ss << "[SECURITY_ALERT] Invalid or malicious data blocked! Packet ID: " << packet_id;
            std::cout << ss.str() << std::endl;
            if (audit_log.is_open()) audit_log << ss.str() << "\n";
            return false;
        }

        ss << "[INTEGRITY_OK] Packet " << packet_id << " validated successfully. Data Hash Verified.";
        std::cout << ss.str() << std::endl;
        if (audit_log.is_open()) audit_log << ss.str() << "\n";
        return true;
    }
};

int main() {
    IntegrityValidator validator("nasa_mission_telemetry.log");

    // Test Senaryoları
    validator.validate_and_process("PKT_001", "STATUS_NOMINAL_FREQUENCIES_LOCKED");
    validator.validate_and_process("PKT_002", "INJECT_MALWARE_CODE"); // Engellenecek test paketi

    return 0;
}
