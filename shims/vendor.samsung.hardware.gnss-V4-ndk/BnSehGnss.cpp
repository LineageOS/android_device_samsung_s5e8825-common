/*
 * SPDX-FileCopyrightText: The LineageOS Project
 * SPDX-License-Identifier: Apache-2.0
 */

#include <string>

namespace aidl::vendor::samsung::hardware::gnss {
using namespace std;

class BnSehGnss {
    BnSehGnss();
    ~BnSehGnss();
    void createBinder();
    void getInterfaceHash(basic_string<char, char_traits<char>, allocator<char>>*);
    void getInterfaceVersion(int*);
};

BnSehGnss::BnSehGnss() {}

BnSehGnss::~BnSehGnss() {}

void BnSehGnss::createBinder() {}

void BnSehGnss::getInterfaceHash(basic_string<char, char_traits<char>, allocator<char>>*) {}

void BnSehGnss::getInterfaceVersion(int*) {}

class ISehGnss {
    static const char* descriptor;
};

const char* ISehGnss::descriptor = "vendor.samsung.hardware.gnss.ISehGnss";
}  // namespace aidl::vendor::samsung::hardware::gnss
