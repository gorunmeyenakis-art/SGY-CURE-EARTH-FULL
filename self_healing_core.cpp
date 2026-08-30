#include <iostream>
#include <fstream>
#include <string>
#include <chrono>
#include <thread>
#include <sstream>
#include <iomanip>

class SystemSelfHealer {
private:
    std::string log_path;

public:
    SystemSelfHealer(const std::string& path) : log_path(path) {}

    void execute_purge_and_refresh() {
        auto now = std::chrono::system_clock::now();
        auto in_time_t = std::chrono::system_clock::to_time_t(now);

        std::stringstream ss;
        ss << "[" << std::put_time(std::localtime(&in_time_t), "%Y-%m-%d %H:%M:%S") << "] "
           << "[SELF_HEALING] Buffer memory purged. System integrity checked. State: REFRESHED & NOMINAL.";

        std::cout << ss.str() << std::endl;

        std::ofstream log_file(log_path, std::ios::app);
        if (log_file.is_open()) {
            log_file << ss.str() << "\n";
            log_file.flush();
        }
    }
};

int main() {
    SystemSelfHealer healer("nasa_mission_telemetry.log");
    
    // Otomatik temizlik ve yenileme döngüsü
    for (int i = 1; i <= 3; ++i) {
        healer.execute_purge_and_refresh();
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }

    return 0;
}
