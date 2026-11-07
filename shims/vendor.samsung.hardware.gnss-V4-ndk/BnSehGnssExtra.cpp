/*
 * SPDX-FileCopyrightText: The LineageOS Project
 * SPDX-License-Identifier: Apache-2.0
 */

#include <string>

namespace aidl::vendor::samsung::hardware::gnss {
using namespace std;

class BnSehGnssExtra {
    BnSehGnssExtra();
    ~BnSehGnssExtra();
    void createBinder();
    void getInterfaceHash(basic_string<char, char_traits<char>, allocator<char>>*);
    void getInterfaceVersion(int*);
};

BnSehGnssExtra::BnSehGnssExtra() {}

BnSehGnssExtra::~BnSehGnssExtra() {}

void BnSehGnssExtra::createBinder() {}

void BnSehGnssExtra::getInterfaceHash(basic_string<char, char_traits<char>, allocator<char>>*) {}

void BnSehGnssExtra::getInterfaceVersion(int*) {}
}  // namespace aidl::vendor::samsung::hardware::gnss
