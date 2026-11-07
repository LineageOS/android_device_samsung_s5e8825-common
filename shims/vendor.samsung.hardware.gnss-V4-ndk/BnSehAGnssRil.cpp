/*
 * SPDX-FileCopyrightText: The LineageOS Project
 * SPDX-License-Identifier: Apache-2.0
 */

#include <string>

namespace aidl::vendor::samsung::hardware::gnss {
using namespace std;

class BnSehAGnssRil {
    BnSehAGnssRil();
    ~BnSehAGnssRil();
    void createBinder();
    void getInterfaceHash(basic_string<char, char_traits<char>, allocator<char>>*);
    void getInterfaceVersion(int*);
};

BnSehAGnssRil::BnSehAGnssRil() {}

BnSehAGnssRil::~BnSehAGnssRil() {}

void BnSehAGnssRil::createBinder() {}

void BnSehAGnssRil::getInterfaceHash(basic_string<char, char_traits<char>, allocator<char>>*) {}

void BnSehAGnssRil::getInterfaceVersion(int*) {}
}  // namespace aidl::vendor::samsung::hardware::gnss
