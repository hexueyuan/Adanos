#include "sqliteIO.h"

#include <iostream>

int main() {
    sqlite3 *db = connect("../database/test1.db");
    if (db) {
        std::cout << "Connect success" << std::endl;
        disconnect(db);
    } else {
        std::cout << "Connect fail" << std::endl;
    }
    return 0;
}
