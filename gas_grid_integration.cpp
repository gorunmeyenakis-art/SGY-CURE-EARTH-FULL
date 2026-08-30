#include <iostream>
#include <string>
#include <chrono>
#include <fstream>
#include <sstream>
#include <iomanip>

struct GasPipelineTelemetry {
    double pressure_bar;      // Hat basıncı (Bar)
    double flow_rate_m3h;     // Akış debisi (m³/saat)
    double gas_temp_celsius;  // Gaz sıcaklığı (°C)
    bool emergency_valve_shut; // Acil durum vanası kapalı mı?

    GasPipelineTelemetry(double p = 4.2, double f = 1250.0, double t = 18.5, bool shut = false)
        : pressure_bar(p), flow_rate_m3h(f), gas_temp_celsius(t), emergency_valve_shut(shut) {}
};

class GasGridIntegration {
private:
    std::ofstream log_file;

public:
    GasGridIntegration(const std::string& log_name) {
        log_file.open(log_name, std::ios::app);
    }
    ~GasGridIntegration() { if (log_file.is_open()) log_file.close(); }

    void evaluate_and_log(const std::string& station_id, GasPipelineTelemetry& data) {
        // Otomatik Güvenlik Protokolü: Basınç 8.0 Bar eşiğini aşarsa vanayı kapat
        if (data.pressure_bar > 8.0 && !data.emergency_valve_shut) {
            data.emergency_valve_shut = true;
            data.flow_rate_m3h = 0.0;
        }

        auto now = std::chrono::system_clock::now();
        auto in_time_t = std::chrono::system_clock::to_time_t(now);

        std::stringstream ss;
        ss << "[" << std::put_time(std::localtime(&in_time_t), "%Y-%m-%d %H:%M:%S") << "] "
           << "[NATURAL_GAS_GRID] Station: " << station_id 
           << " | Pressure: " << std::fixed << std::setprecision(2) << data.pressure_bar << " Bar"
           << " | Flow: " << data.flow_rate_m3h << " m³/h"
           << " | Temp: " << data.gas_temp_celsius << " °C"
           << " | Valve State: " << (data.emergency_valve_shut ? "SHUT (CRITICAL)" : "OPEN (NOMINAL)");

        std::cout << ss.str() << std::endl;
        if (log_file.is_open()) {
            log_file << ss.str() << "\n";
            log_file.flush();
        }
    }
};

int main() {
    GasGridIntegration gas_manager("nasa_mission_telemetry.log");

    // Nominal Hat Testi
    GasPipelineTelemetry main_station(4.5, 2100.0, 16.2, false);
    gas_manager.evaluate_and_log("IST_GAS_DISTRIBUTION_NODE_01", main_station);

    // Aşırı Basınç (Kritik Durum) Testi
    GasPipelineTelemetry critical_station(9.2, 3400.0, 22.1, false);
    gas_manager.evaluate_and_log("IST_GAS_DISTRIBUTION_NODE_02", critical_station);

    return 0;
}
