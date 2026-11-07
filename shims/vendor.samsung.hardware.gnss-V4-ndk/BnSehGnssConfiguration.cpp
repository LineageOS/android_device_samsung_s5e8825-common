/*
 * SPDX-FileCopyrightText: The LineageOS Project
 * SPDX-License-Identifier: Apache-2.0
 */

#include <string>

namespace aidl::vendor::samsung::hardware::gnss {
using namespace std;

class BnSehGnssConfiguration {
    BnSehGnssConfiguration();
    ~BnSehGnssConfiguration();
    void createBinder();
    void getInterfaceHash(basic_string<char, char_traits<char>, allocator<char>>*);
    void getInterfaceVersion(int*);
};

BnSehGnssConfiguration::BnSehGnssConfiguration() {}

BnSehGnssConfiguration::~BnSehGnssConfiguration() {}

void BnSehGnssConfiguration::createBinder() {}

void BnSehGnssConfiguration::getInterfaceHash(
        basic_string<char, char_traits<char>, allocator<char>>*) {}

void BnSehGnssConfiguration::getInterfaceVersion(int*) {}
}  // namespace aidl::vendor::samsung::hardware::gnss
