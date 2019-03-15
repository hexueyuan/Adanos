#if defined(__GNUC__)
#pragma GCC diagnostic push
#pragma GCC diagnostic ignored "-Wdeprecated-declarations"
#elif defined(_MSC_VER)
#pragma warning(disable : 4996)
#endif

#include <iostream>
#include <string>
#include <fstream>
#include <sstream>

#include <stdlib.h>
#include <stdio.h>
#include <getopt.h>

#include <sqlite3.h>
#include <json/json.h>

using namespace std;

sqlite3* connect(std::string path) {
    sqlite3* db = NULL;
    
    if (sqlite3_open(path.c_str(), &db)) {
        return NULL;
    } else {
        return db;
    }
}

void disconnect(sqlite3* db) {
    sqlite3_close(db);
}

static int callback(void *NotUsed, int argc, char **argv, char **azColName){
   int i;
   for(i=0; i<argc; i++){
      printf("%s = %s\n", azColName[i], argv[i] ? argv[i] : "NULL");
   }
   printf("\n");
   return 0;
}

bool isValidCmd(Json::Value conf) {
    if (!conf.isMember("table_name") || !conf.isMember("columns") || !conf["columns"].isArray()) {
        return false;
    }
    int size = conf["columns"].size();
    for (int i = 0; i < size; ++i) {
        if (!conf["columns"][i].isMember("column_name") ||
            !conf["columns"][i].isMember("type") ||
            !conf["columns"][i].isMember("key") ||
            !conf["columns"][i].isMember("constraint")) {
                return false;
            }
    }
    return true;
}

int main(int argc, char** argv) {
    // 处理命令行参数
    int opt = 0;
    int save_opt = -1;
    int save_input_index = -1;
    int option_index = 0;
    string db_path;
    const char *optstring = "cdsmi:";

    static struct option long_options[] = {
        {"db", required_argument, NULL, 'b'},
        {"create", no_argument, NULL, 'c'},
        {"delete", no_argument, NULL, 'd'},
        {"search", no_argument, NULL, 's'},
        {"modify", no_argument, NULL, 'm'},
        {"input",  required_argument, NULL, 'i'},
        {0, 0, 0, 0}  // 添加 {0, 0, 0, 0} 是为了防止输入空值
    }; 

    while ((opt = getopt_long(argc, argv, optstring, long_options, &option_index)) != -1) {

        switch (opt) {
            case 'c':
            case 'd':
            case 's':
            case 'm':
                if (save_opt == -1) {
                    save_opt = opt;
                } else {
                    cout << "Invalid usage!" << endl;
                    return 0;
                }
                break;
            case 'i':
                if (save_input_index == -1) {
                    save_input_index = optind - 1;
                } else {
                    cout << "Invalid config input!" << endl;
                    return -1;
                }
                break;
            case 'b':
                db_path = argv[optind - 1];
                break;
            default:
                cout << "Unknown option:'" << (char)opt << "'" << endl;
                return -1;
        }
        
    }

    if (db_path == "") {
        cout << "No database select!" << endl;
        return -1;
    }

    switch (save_opt) {
        case 'c':
            cout << "Create table from " << argv[save_input_index] << endl;
            break; 
        case 'd':
            cout << "Delete table from " << argv[save_input_index] << endl;
            break; 
        case 's':
            cout << "Search table from " << argv[save_input_index] << endl;
            break; 
        case 'm':
            cout << "Modify table from " << argv[save_input_index] << endl;
            break;
        default:
            cout << "Bad option" << endl;
            return -1;
    }

    //处理输入配置
    ifstream inStream;
    inStream.open(argv[save_input_index], ios::out);
    stringstream buffer;
    buffer << inStream.rdbuf();

    string confBuf = buffer.str();
    Json::Reader reader;
    Json::Value conf;
    if (reader.parse(confBuf.c_str(), conf)) {
        Json::Value columnsObj = conf["columns"];
        cout << "Table name: " << conf["table_name"].asString() << endl;
        int size = columnsObj.size();
        for (int i = 0; i < size; ++i) {
            cout << "  " << "column-name: " << columnsObj[i]["column_name"].asString() << \
                 "  type: " << columnsObj[i]["type"] << "  key:" << columnsObj[i]["key"].asString() << \
                 "  constraint: " << columnsObj[i]["contraint"].asString() << endl;
        }
    }
    if (isValidCmd(conf)) {
        cout << "Valid input" << endl;
    } else {
        cout << "Invalid input" << endl;
    }

    //分支函数
    string cmd;
    switch (save_opt) {
        case 'c': {
            cmd += "CREATE TABLE ";
            cmd += conf["table_name"].asString() + "(";
            int size = conf["columns"].size();
            for (int i = 0; i < size; ++i) {
                cmd += conf["columns"][i]["column_name"].asString() + " ";
                cmd += conf["columns"][i]["type"].asString() + " ";
                cmd += conf["columns"][i]["key"].asString() + " ";
                cmd += conf["columns"][i]["constraint"].asString();
                if (i != size - 1) {
                    cmd += ",";
                }
            }
            cmd += ");";
        }
        case 's': {
            cmd += "SELECT ";
            int size = conf["columns"].size();
            for (int i = 0; i < size; ++i) {
                cmd += conf["columns"][i]["column_name"].asString() + " ";
                if (i != size - 1) {
                    cmd += ",";
                }
            }
            cmd += "FROM " + conf["table_name"].asString() + ";";
        }
    }
    cout << cmd << endl;

    sqlite3* db = connect(db_path);
    char* zErrMsg = 0;
    if (db) {
        int rc = sqlite3_exec(db, cmd.c_str(), callback, 0, &zErrMsg);
        if( rc != SQLITE_OK ){
            cout << "SQL error: " << zErrMsg << endl;;
            sqlite3_free(zErrMsg);
        }else{
            cout <<"Records created successfully!" << endl;
        }
    } else {
        cout << "Connect database fail!" << endl;
    }

    disconnect(db);

    return 0;
}