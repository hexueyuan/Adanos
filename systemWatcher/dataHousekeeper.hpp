#ifndef __DATAHOUSEKEEPER_HPP__
#define __DATAHOUSEKEEPER_HPP__

#include <string>
/*
*一个基类，所有数据监控器的基类
*包括数据来源和获取一次数据的方法
*/
namespace smows {
class _dataHousekeeper {
    public:
        _dataHousekeeper();
        
        ~_dataHousekeeper();

        bool setFilecoming(std::string filecomingPath);
        std::string getFilecomming();

    private:
        std::string _file_coming;
}

}
#endif
