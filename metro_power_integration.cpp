#include <iostream>
#include <vector>
#include <cmath>
#include <string>
#include <chrono>
#include <fstream>
#include <sstream>
#include <iomanip>

struct MetroLineState {
    double third_rail_voltage;
    double current_draw_amps;
    double regen_power_kw;
    bool regenerative_braking_active;

    MetroLineState(double v = 750.0, double i = 1200.0, double r = 450.0, bool active = true)
        : third_rail_voltage(v), current_draw_amps(i), regen_power_kw(r), regenerative_braking_active(active) {}
};

class MetroPowerGridIntegration {
private:
    std::ofstream log_file;

public:
    MetroPowerGridIntegration(const std::string& log_name) {
        log_file.open(log_name, std::ios::app);
    }
    ~MetroPowerGridIntegration() { if (log_file.is_open()) log_file.close(); }

    double calculate_available_energy(const MetroLineState& state) {
        double gross_power = (state.third_rail_voltage * state.current_draw_amps) / 1000.0;
        if (state.regenerative_braking_active) {
            gross_power += state.regen_power_kw;
        }
        return gross_power;
    }

    void log_telemetry(const std::string& node_id, double energy_kw, double cloud_load_percentage) {
        auto now = std::chrono::system_clock::now();
        auto in_time_t = std::chrono::system_clock::to_time_t(now);

        std::stringstream ss;
        ss << "[" << std::put_time(std::localtime(&in_time_t), "%Y-%m-%d %H:%M:%S") << "] "
           << "[METRO_GRID_INTEGRATION] Node: " << node_id 
           << " | Available Power: " << energy_kw << " kW"
           << " | Cloud Node Load: " << std::fixed << std::setprecision(2) << cloud_load_percentage << "%";

        std::cout << ss.str() << std::endl;
        if (log_file.is_open()) {
            log_file << ss.str() << "\n";
            log_file.flush();
        }
    }
};

int main() {
    MetroPowerGridIntegration grid_manager("nasa_mission_telemetry.log");
    MetroLineState train_1(750.0, 1200.0, 450.0, true); 

    double available_kw = grid_manager.calculate_available_energy(train_1);
    double allocated_cloud_capacity = (available_kw / 1500.0) * 100.0;

    grid_manager.log_telemetry("ISTANBUL_METRO_LINE_3RD_RAIL", available_kw, allocated_cloud_capacity);

    return 0;
}
