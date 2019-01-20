#ifndef __CPUINFO_HPP__
#define __CPUINFO_HPP__

struct CPUInfo {
    uint8_t processor;
    uint8_t usage_rate_integer;
    uint8_t usage_rate_decimal;
    uint64_t running_time_second;
}

class CPUInfoManager {
    public:
        CPUInfoManager();
        
        ~CPUInfoManager();

        bool getCPUInfo();
};

#endif
